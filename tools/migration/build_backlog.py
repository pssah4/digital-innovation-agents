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
import re
import sys
from collections import defaultdict
from pathlib import Path


def get_first_h1(content: str) -> str:
    for line in content.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    return ""


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
        art.append(kw)

    # EPICs
    for fp in sorted((devp / "requirements/epics").glob("EPIC-*.md")) if (devp / "requirements/epics").is_dir() else []:
        m = re.match(r"^EPIC-(\d+)-(.+)\.md$", fp.name)
        if not m:
            continue
        en = int(m.group(1))
        slug = m.group(2)
        epic_id = f"EPIC-{en:02d}"
        title = get_first_h1(fp.read_text(encoding="utf-8")) or slug.replace("-", " ").title()
        title = re.sub(r"^EPIC[\s-]*\d+:\s*", "", title, flags=re.IGNORECASE)
        title = re.sub(r"^Epic:\s*", "", title)
        ov = overrides.get(epic_id, {})
        status = ov.get("status", "Active")
        phase = ov.get("phase", "Building")
        add(id=epic_id, type="Epic", title=title, status=status, phase=phase,
            epic=epic_id, epic_num=en, refs=[], source="BA",
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
            title = get_first_h1(fp.read_text(encoding="utf-8")) or slug.replace("-", " ").title()
            title = re.sub(r"^(?:FEATURE|FEAT)[:\s-]*\d*-?\d*(?:(?<=\d)[a-z])?[:\s-]*", "", title, flags=re.IGNORECASE)
            ov = overrides.get(feat_id, {})
            status = ov.get("status", "Done")
            phase = ov.get("phase", "Released")
            add(id=feat_id, type="Feature", title=title[:80], status=status, phase=phase,
                epic=epic_id, epic_num=ee, refs=[epic_id], source="BA",
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
            add(id=fid, type="Fix", title=title[:80], status=status, phase=phase,
                epic=epic_id, epic_num=ee, refs=[feat_id, epic_id], source="BUG",
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
            title = get_first_h1(fp.read_text(encoding="utf-8")) or slug.replace("-", " ").title()
            ov = overrides.get(iid, {})
            status = ov.get("status", "Planned")
            phase = ov.get("phase", "Building")
            add(id=iid, type="Improvement", title=title[:80], status=status, phase=phase,
                epic=epic_id, epic_num=ee, refs=[feat_id, epic_id], source="USER",
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
