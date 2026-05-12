#!/usr/bin/env python3
"""DIA migration -- Phase 5: regenerate _devprocess/context/BACKLOG.md.

Scans every artifact under _devprocess/ and writes a fresh backlog.
Status, phase, refs are derived from frontmatter where possible, and
from heuristics otherwise. The existing backlog (if any) is preserved
as `BACKLOG.md.preMigration` for one-step rollback.

The skill operator can edit a small YAML config for status overrides
before running. Default config path: `dia-migration.yml` in project
root. If absent, only heuristics are used.

Usage:
    python3 build_backlog.py [project_root] [--config path]
"""
from __future__ import annotations
import argparse
import os
import re
import sys
from collections import defaultdict
from pathlib import Path


def get_first_h1(content: str) -> str:
    for line in content.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def strip_self_prefix(title: str, item_id: str) -> str:
    """Drop a leading `<item_id>:` / `[<item_id>]` / `<item_id> -` prefix.

    The BACKLOG Title column must hold the bare title only. flow.py
    builds the GitHub issue title as `<id>: <title>`, so a Title cell
    like `IMP-01-01-08: ensureColumn ...` would yield
    `IMP-01-01-08: IMP-01-01-08: ensureColumn ...` on the issue.
    """
    if not title or not item_id:
        return title
    esc = re.escape(item_id)
    patterns = (
        re.compile(rf"^\s*\[\s*{esc}\s*\]\s*[:\-]?\s*"),
        re.compile(rf"^\s*{esc}\s*[:\-]\s*"),
        re.compile(rf"^\s*{esc}\s*$"),
    )
    cleaned = title
    changed = True
    while changed:
        changed = False
        for p in patterns:
            new = p.sub("", cleaned, count=1)
            if new != cleaned:
                cleaned, changed = new, True
                break
    return cleaned.strip() or title


def ba_ref_to_id(ref: str | list | None) -> str | None:
    """Extract a short BA id (`BA-EPIC-04`, `BA-FEAT-04-02`, ...) from a
    `ba-ref:` value. Returns None when the value is missing or unparseable.
    """
    if not ref:
        return None
    if isinstance(ref, list):
        ref = ref[0] if ref else ""
    if not isinstance(ref, str):
        return None
    name = ref.rsplit("/", 1)[-1]
    m = re.match(
        r"^(BA-(?:EPIC-\d+|FEAT-\d+-\d+|IMP-\d+-\d+-\d+|FIX-\d+-\d+-\d+))",
        name,
    )
    return m.group(1) if m else None


def find_item_ba(adir: Path, kind: str, ee: int, ff: int | None = None,
                 nn: int | None = None) -> Path | None:
    """Locate the matching Item-BA file for a given target item.

    kind is one of 'EPIC', 'FEAT', 'IMP', 'FIX'.
    """
    if not adir.is_dir():
        return None
    if kind == "EPIC":
        pattern = f"BA-EPIC-{ee:02d}-*.md"
    elif kind == "FEAT":
        if ff is None:
            return None
        pattern = f"BA-FEAT-{ee:02d}-{ff:02d}-*.md"
    elif kind in ("IMP", "FIX"):
        if ff is None or nn is None:
            return None
        pattern = f"BA-{kind}-{ee:02d}-{ff:02d}-{nn:02d}-*.md"
    else:
        return None
    matches = sorted(adir.glob(pattern))
    return matches[0] if matches else None


def insert_ba_ref(artefact_path: Path, ba_path: Path) -> bool:
    """Add `ba-ref:` to an artefact's YAML frontmatter if missing.

    Returns True when the file was modified. Idempotent: existing
    `ba-ref:` lines (any value) are left untouched.
    """
    content = artefact_path.read_text(encoding="utf-8")
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    rel_str = os.path.relpath(
        ba_path.resolve(), start=artefact_path.resolve().parent
    ).replace("\\", "/")

    new_line = f"ba-ref: {rel_str}"

    if fm_match:
        fm_body = fm_match.group(1)
        if re.search(r"^ba-ref\s*:", fm_body, re.MULTILINE):
            return False
        new_fm = fm_body + "\n" + new_line
        new_content = (
            "---\n" + new_fm + "\n---\n" + content[fm_match.end():]
        )
    else:
        new_content = "---\n" + new_line + "\n---\n\n" + content

    artefact_path.write_text(new_content, encoding="utf-8")
    return True


def restore_ba_refs(root: Path) -> int:
    """Walk requirements/{epics,features,improvements,fixes} and insert
    `ba-ref:` into each artefact's frontmatter when a matching Item-BA
    file exists in analysis/.

    Idempotent: skips artefacts whose frontmatter already carries a
    ba-ref. Returns the number of modified files.
    """
    devp = root / "_devprocess"
    adir = devp / "analysis"
    modified = 0

    epics_dir = devp / "requirements/epics"
    if epics_dir.is_dir():
        for fp in sorted(epics_dir.glob("EPIC-*.md")):
            m = re.match(r"^EPIC-(\d+)-(?!ba\.md$).+\.md$", fp.name)
            if not m:
                continue
            ee = int(m.group(1))
            ba = find_item_ba(adir, "EPIC", ee)
            if ba and insert_ba_ref(fp, ba):
                modified += 1

    feats_dir = devp / "requirements/features"
    if feats_dir.is_dir():
        for fp in sorted(feats_dir.glob("FEAT-*.md")):
            m = re.match(r"^FEAT-(\d+)-(\d+)[a-z]?-.+\.md$", fp.name)
            if not m:
                continue
            ee, ff = int(m.group(1)), int(m.group(2))
            ba = find_item_ba(adir, "FEAT", ee, ff)
            if ba and insert_ba_ref(fp, ba):
                modified += 1

    for kind, sub in (("IMP", "improvements"), ("FIX", "fixes")):
        d = devp / f"requirements/{sub}"
        if not d.is_dir():
            continue
        for fp in sorted(d.glob(f"{kind}-*.md")):
            m = re.match(rf"^{kind}-(\d+)-(\d+)-(\d+)-.+\.md$", fp.name)
            if not m:
                continue
            ee, ff, nn = (
                int(m.group(1)),
                int(m.group(2)),
                int(m.group(3)),
            )
            ba = find_item_ba(adir, kind, ee, ff, nn)
            if ba and insert_ba_ref(fp, ba):
                modified += 1

    return modified


def parse_frontmatter(content: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not m:
        return {}
    out: dict = {}
    cur_key = None
    for line in m.group(1).split("\n"):
        m2 = re.match(r"^([a-zA-Z0-9_-]+):\s*(.*)$", line)
        if m2:
            cur_key = m2.group(1)
            val = m2.group(2).strip()
            if val.startswith("[") and val.endswith("]"):
                val = [x.strip().strip("'\"") for x in val[1:-1].split(",") if x.strip()]
            out[cur_key] = val
        elif cur_key and line.strip().startswith("-"):
            v = line.strip()[1:].strip()
            if not isinstance(out[cur_key], list):
                out[cur_key] = []
            out[cur_key].append(v)
    return out


def collect(root: Path, overrides: dict) -> list[dict]:
    art: list[dict] = []
    devp = root / "_devprocess"
    if not devp.is_dir():
        return art

    def add(**kw):
        # Single choke point: the Title column never carries an id
        # prefix, whatever the per-type heuristics produced above.
        if kw.get("title") and kw.get("id"):
            kw["title"] = strip_self_prefix(kw["title"], kw["id"])
        art.append(kw)

    # EPICs
    for fp in sorted((devp / "requirements/epics").glob("EPIC-*.md")) if (devp / "requirements/epics").is_dir() else []:
        if fp.name.endswith("-ba.md"):
            # legacy mini-BA (should have been moved by flatten_analysis)
            continue
        m = re.match(r"^EPIC-(\d+)-(.+)\.md$", fp.name)
        if not m:
            continue
        en = int(m.group(1))
        slug = m.group(2)
        epic_id = f"EPIC-{en:02d}"
        content = fp.read_text(encoding="utf-8")
        title = get_first_h1(content) or slug.replace("-", " ").title()
        title = re.sub(r"^EPIC[\s-]*\d+:\s*", "", title, flags=re.IGNORECASE)
        title = re.sub(r"^Epic:\s*", "", title)
        ov = overrides.get(epic_id, {})
        status = ov.get("status", "Active")
        phase = ov.get("phase", "Building")
        fm = parse_frontmatter(content)
        ba_id = ba_ref_to_id(fm.get("ba-ref"))
        refs = [ba_id] if ba_id else []
        add(id=epic_id, type="Epic", title=title, status=status, phase=phase,
            epic=epic_id, epic_num=en, refs=refs, source="BA",
            commit="", claim="", last_change="", notes="",
            file=str(fp.relative_to(root)))

    # FEATs (and FEATURE leftovers)
    feats_dir = devp / "requirements/features"
    if feats_dir.is_dir():
        for fp in sorted(feats_dir.glob("FEAT-*.md")) + sorted(feats_dir.glob("FEATURE-*.md")):
            m = re.match(r"^(?:FEAT|FEATURE)-(\d+)(?:-(\d+))?([a-z]?)-(.+)\.md$", fp.name)
            if not m:
                continue
            if m.group(2):
                ee, ff = int(m.group(1)), int(m.group(2))
            else:
                num = m.group(1)
                if len(num) >= 4:
                    ee, ff = int(num[:2]), int(num[2:4])
                else:
                    ee, ff = 0, int(num)
            suffix = m.group(3) or ""
            slug = m.group(4)
            feat_id = f"FEAT-{ee:02d}-{ff:02d}{suffix}"
            epic_id = f"EPIC-{ee:02d}"
            content = fp.read_text(encoding="utf-8")
            title = get_first_h1(content) or slug.replace("-", " ").title()
            title = re.sub(r"^(?:FEATURE|FEAT)[:\s-]*\d*-?\d*(?:(?<=\d)[a-z])?[:\s-]*", "", title, flags=re.IGNORECASE)
            ov = overrides.get(feat_id, {})
            status = ov.get("status", "Done")
            phase = ov.get("phase", "Released")
            fm = parse_frontmatter(content)
            ba_id = ba_ref_to_id(fm.get("ba-ref"))
            refs = [epic_id] + ([ba_id] if ba_id else [])
            add(id=feat_id, type="Feature", title=title[:80], status=status, phase=phase,
                epic=epic_id, epic_num=ee, refs=refs, source="BA",
                commit="", claim="", last_change="", notes=ov.get("notes", ""),
                file=str(fp.relative_to(root)))

    # FIX
    fixes_dir = devp / "requirements/fixes"
    if fixes_dir.is_dir():
        for fp in sorted(fixes_dir.glob("FIX-*.md")):
            m = re.match(r"^FIX-(\d{2})-(\d{2})-(\d{2})-(.+)\.md$", fp.name)
            if not m:
                continue
            ee, ff, nn, slug = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4)
            fid = f"FIX-{ee:02d}-{ff:02d}-{nn:02d}"
            feat_id = f"FEAT-{ee:02d}-{ff:02d}"
            epic_id = f"EPIC-{ee:02d}"
            content = fp.read_text(encoding="utf-8")
            title = get_first_h1(content) or slug.replace("-", " ").title()
            title = re.sub(r"^(BUG|FIX)[\s-]*\d+\s*[:\-]?\s*", "", title, flags=re.IGNORECASE)
            cl = content.lower()[:500]
            prio = "P0" if "p0" in cl else ("P1" if "p1" in cl else "P2")
            ov = overrides.get(fid, {})
            status = ov.get("status", "Done")
            phase = ov.get("phase", "Released")
            fm = parse_frontmatter(content)
            ba_id = ba_ref_to_id(fm.get("ba-ref"))
            refs = [feat_id, epic_id] + ([ba_id] if ba_id else [])
            add(id=fid, type="Fix", title=title[:80], status=status, phase=phase,
                epic=epic_id, epic_num=ee, refs=refs, source="BUG",
                commit="", claim="", last_change="", notes=prio,
                file=str(fp.relative_to(root)))

    # IMP
    imp_dir = devp / "requirements/improvements"
    if imp_dir.is_dir():
        for fp in sorted(imp_dir.glob("IMP-*.md")):
            m = re.match(r"^IMP-(\d{2})-(\d{2})-(\d{2})-(.+)\.md$", fp.name)
            if not m:
                continue
            ee, ff, nn, slug = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4)
            iid = f"IMP-{ee:02d}-{ff:02d}-{nn:02d}"
            feat_id = f"FEAT-{ee:02d}-{ff:02d}"
            epic_id = f"EPIC-{ee:02d}"
            content = fp.read_text(encoding="utf-8")
            title = get_first_h1(content) or slug.replace("-", " ").title()
            ov = overrides.get(iid, {})
            status = ov.get("status", "Planned")
            phase = ov.get("phase", "Building")
            fm = parse_frontmatter(content)
            ba_id = ba_ref_to_id(fm.get("ba-ref"))
            refs = [feat_id, epic_id] + ([ba_id] if ba_id else [])
            add(id=iid, type="Improvement", title=title[:80], status=status, phase=phase,
                epic=epic_id, epic_num=ee, refs=refs, source="USER",
                commit="", claim="", last_change="", notes="",
                file=str(fp.relative_to(root)))

    # ADRs (cross-cutting; no epic)
    adr_dir = devp / "architecture"
    if adr_dir.is_dir():
        for fp in sorted(adr_dir.glob("ADR-*.md")):
            m = re.match(r"^ADR-(\d+)-(.+)\.md$", fp.name)
            if not m:
                continue
            n = int(m.group(1))
            adr_id = f"ADR-{n:02d}"
            content = fp.read_text(encoding="utf-8")
            title = get_first_h1(content) or m.group(2).replace("-", " ").title()
            title = re.sub(r"^ADRs?[\s\-:]+\d*\s*[:\-]?\s*", "", title)
            ov = overrides.get(adr_id, {})
            status = ov.get("status", "Accepted")
            phase = ov.get("phase", "Released")
            related = []
            fm = parse_frontmatter(content)
            for k in ("related", "supersedes", "superseded-by", "feature-refs", "adr-refs"):
                v = fm.get(k)
                if isinstance(v, list):
                    for it in v:
                        rid = re.search(r"(ADR-\d+|FEAT-\d+-\d+|PLAN-\d+|EPIC-\d+)", it)
                        if rid:
                            related.append(rid.group(1))
            seen = set()
            related = [r for r in related if not (r in seen or seen.add(r))]
            add(id=adr_id, type="ADR", title=title[:80], status=status, phase=phase,
                epic="", epic_num=-1, refs=related[:4], source="ARCH",
                commit="", claim="", last_change="", notes="",
                file=str(fp.relative_to(root)))

    # PLANs
    plan_dir = devp / "implementation/plans"
    if plan_dir.is_dir():
        for fp in sorted(plan_dir.glob("PLAN-*.md")):
            m = re.match(r"^PLAN-(\d+)-(.+)\.md$", fp.name)
            if not m:
                continue
            n = int(m.group(1))
            plan_id = f"PLAN-{n:02d}"
            content = fp.read_text(encoding="utf-8")
            title = get_first_h1(content) or m.group(2).replace("-", " ").title()
            title = re.sub(r"^PLAN[\s-]*\d*\s*[:\-]?\s*", "", title)
            ov = overrides.get(plan_id, {})
            status = ov.get("status", "Draft")
            phase = ov.get("phase", "Building")
            related = []
            fm = parse_frontmatter(content)
            for k in ("related", "feature-refs", "adr-refs", "epic"):
                v = fm.get(k)
                items = v if isinstance(v, list) else ([v] if isinstance(v, str) else [])
                for it in items:
                    rid = re.search(r"(ADR-\d+|FEAT-\d+-\d+|EPIC-\d+|FEATURE-\d+)", it)
                    if rid:
                        related.append(rid.group(1))
            seen = set()
            related = [r for r in related if not (r in seen or seen.add(r))]
            add(id=plan_id, type="Plan", title=title[:80], status=status, phase=phase,
                epic="", epic_num=-1, refs=related[:4], source="ARCH",
                commit="", claim="", last_change="", notes="",
                file=str(fp.relative_to(root)))

    return art


def render(art: list[dict], project_name: str) -> str:
    by_epic: dict[str, list[dict]] = defaultdict(list)
    standalone: list[dict] = []
    epic_meta: dict[str, dict] = {}
    for a in art:
        if a["type"] == "Epic":
            epic_meta[a["id"]] = a
        elif a.get("epic"):
            by_epic[a["epic"]].append(a)
        else:
            standalone.append(a)

    counts = {"status": defaultdict(int), "phase": defaultdict(int), "type": defaultdict(int)}
    for a in art:
        counts["status"][a["status"]] += 1
        counts["phase"][a["phase"]] += 1
        counts["type"][a["type"]] += 1

    out = [f"# Backlog {project_name}",
           "",
           "> Single source of truth for state and the artifact relation graph.",
           "> Status fields live HERE, not in artifact frontmatter.",
           "",
           "Last update: by /dia-migration",
           "",
           "---",
           "",
           "## Dashboard",
           "",
           "| Status | Count | | Phase | Count | | Type | Count |",
           "|---|---|-|---|---|-|---|---|"]
    statuses = ("Planned", "Active", "Review", "Done", "Waiting", "Deferred",
                "Wont Fix", "Superseded", "Deprecated", "Accepted", "Proposed", "Draft", "Open")
    phases = ("Released", "Building", "Planned", "Candidates")
    types_l = ("Epic", "Feature", "Fix", "Improvement", "ADR", "Plan")
    n = max(len([s for s in statuses if counts['status'].get(s)]),
            len(phases), len(types_l))
    for i in range(n):
        s_filt = [s for s in statuses if counts['status'].get(s)]
        s = f"{s_filt[i]} | {counts['status'][s_filt[i]]}" if i < len(s_filt) else " | "
        p = f"{phases[i]} | {counts['phase'].get(phases[i], 0)}" if i < len(phases) else " | "
        t = f"{types_l[i]} | {counts['type'].get(types_l[i], 0)}" if i < len(types_l) else " | "
        out.append(f"| {s} | {p} | {t} |")
    out.append("")
    out.append(f"Total artifacts: {len(art)}")
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Active Epics")
    out.append("")

    for epic_id in sorted(by_epic.keys()):
        meta = epic_meta.get(epic_id)
        if not meta:
            continue
        out.append(f"### {epic_id}: {meta['title']}")
        out.append("")
        out.append(f"Source: `{meta['file']}`")
        out.append(f"Phase: {meta['phase']} | Status: {meta['status']}")
        out.append("")
        out.append("| ID | Type | Title | Status | Phase | Refs | Source | Commit | Claim | Last change | Notes |")
        out.append("|---|---|---|---|---|---|---|---|---|---|---|")
        order = {"Feature": 0, "Fix": 1, "Improvement": 2, "Plan": 3, "ADR": 4}
        for a in sorted(by_epic[epic_id], key=lambda a: (order.get(a["type"], 5), a["id"])):
            refs = ", ".join(a["refs"]) if a["refs"] else ""
            out.append(f"| {a['id']} | {a['type']} | {a['title']} | {a['status']} | {a['phase']} | {refs} | {a['source']} | {a.get('commit','')} | {a.get('claim','')} | {a.get('last_change','')} | {a.get('notes','')} |")
        out.append("")

    if standalone:
        out.append("## Cross-cutting (ADRs, Plans, no Epic)")
        out.append("")
        out.append("| ID | Type | Title | Status | Phase | Refs | Source | Commit | Claim | Last change | Notes |")
        out.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for a in sorted(standalone, key=lambda a: a["id"]):
            refs = ", ".join(a["refs"]) if a["refs"] else ""
            out.append(f"| {a['id']} | {a['type']} | {a['title']} | {a['status']} | {a['phase']} | {refs} | {a['source']} |  |  | {a.get('last_change','')} | {a.get('notes','')} |")
        out.append("")
    return "\n".join(out) + "\n"


def load_overrides(path: Path | None) -> dict:
    if not path or not path.is_file():
        return {}
    try:
        import yaml  # type: ignore
    except Exception:
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", nargs="?", default=".")
    parser.add_argument("--config", default="dia-migration.yml")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    cfg = root / args.config
    overrides = load_overrides(cfg)
    ba_ref_count = restore_ba_refs(root)
    if ba_ref_count:
        print(f"Restored ba-ref: in {ba_ref_count} artefact frontmatters")
    art = collect(root, overrides)
    print(f"Collected {len(art)} artifacts")
    backlog_path = root / "_devprocess/context/BACKLOG.md"
    if backlog_path.is_file():
        backup = backlog_path.with_suffix(".md.preMigration")
        backup.write_text(backlog_path.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"Backed up previous backlog to {backup.relative_to(root)}")
    backlog_path.parent.mkdir(parents=True, exist_ok=True)
    backlog_path.write_text(render(art, root.name), encoding="utf-8")
    print(f"Wrote {backlog_path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
