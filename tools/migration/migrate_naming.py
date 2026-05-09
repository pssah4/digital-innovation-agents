#!/usr/bin/env python3
"""DIA migration -- Phase 3: filename migration to v2 ID schemas.

Renames artifact files and updates references in `_devprocess/`,
`src/ARCHITECTURE.map`, and source / test / doc trees. Three passes:

Pass 1: file renames + reference replacement using the rename map.
Pass 2: catch-all regex sweep for IDs that have no corresponding file
        (legacy in-prose references like EPIC-023 that was never
        materialized).
Pass 3: source-tree sweep over `src/`, `tests/`, `docs/` (configurable)
        so that code comments and out-of-_devprocess docs stop pointing
        at legacy `FEATURE-NNNN` ids.

Plus a thematic-sanity warning: when a `FEATURE-EE0F -> FEAT-EE-FF`
rename collides with an existing FEAT-EE-FF row that already names a
different feature, the rename is skipped and the conflict is surfaced.

Idempotent. Run on a clean v2 repo -> zero changes.

Skips `_devprocess/context/HANDOFFS.md` (append-only audit log)
to preserve historical IDs as written.

Usage:
    python3 migrate_naming.py [project_root]
"""
from __future__ import annotations
import re
import sys
from pathlib import Path


FEAT_BACKLOG_ROW_RE = re.compile(
    r"^\|\s*(FEAT-\d{2}-\d{2}[a-z]?)\s*\|[^|]+\|\s*([^|]+?)\s*\|"
)


def parse_existing_feat_titles(root: Path) -> dict[str, str]:
    """Map FEAT-EE-FF -> title from existing BACKLOG.md rows.

    Used by the thematic-sanity warning. Empty when BACKLOG.md is
    absent or no FEAT rows exist yet.
    """
    bl = root / "_devprocess" / "context" / "BACKLOG.md"
    if not bl.is_file():
        return {}
    out: dict[str, str] = {}
    for line in bl.read_text(encoding="utf-8").splitlines():
        m = FEAT_BACKLOG_ROW_RE.match(line)
        if not m:
            continue
        out[m.group(1)] = m.group(2).strip()
    return out


def slug_to_title(slug: str) -> str:
    """Approximate reverse of slugification for fuzzy title compare."""
    return re.sub(r"[-_]+", " ", slug).strip().lower()


def title_match(slug_a: str, title_b: str) -> bool:
    """Loose title comparison: token overlap of >= 50% counts as match.

    Both inputs are normalised (lowercase, non-alphanumerics stripped)
    and split into token sets. The cheap heuristic catches obvious
    matches (`agent-sidebar-view` vs `Agent Sidebar View`) without
    flagging cosmetic differences.
    """
    a_tokens = {t for t in re.split(r"[^a-z0-9]+", slug_to_title(slug_a)) if t}
    b_tokens = {t for t in re.split(r"[^a-z0-9]+", title_b.strip().lower()) if t}
    if not a_tokens or not b_tokens:
        return False
    overlap = a_tokens & b_tokens
    return len(overlap) >= max(1, min(len(a_tokens), len(b_tokens)) // 2)


def collect_renames(
    root: Path,
) -> tuple[list[tuple[Path, Path]], dict[str, str], list[tuple[str, str, str, str]]]:
    renames: list[tuple[Path, Path]] = []
    id_remap: dict[str, str] = {}
    existing_titles = parse_existing_feat_titles(root)
    skipped: list[tuple[str, str, str, str]] = []

    def add(old_fp: Path, new_name: str, old_id: str, new_id: str) -> None:
        renames.append((old_fp, old_fp.parent / new_name))
        id_remap[old_id] = new_id

    def add_feature_safe(
        old_fp: Path, new_name: str, old_id: str, new_id: str, source_slug: str,
    ) -> None:
        """Like add(), but skips the rename when new_id already names a
        thematically different feature in the BACKLOG.

        The legacy `FEATURE-EE0F -> FEAT-EE-FF` mapping is purely
        positional. When two unrelated features share the same numeric
        prefix (collision after EE/FF reshape), silently overwriting
        loses the original feature. We surface the conflict instead.
        """
        existing = existing_titles.get(new_id)
        if existing and not title_match(source_slug, existing):
            skipped.append((old_id, new_id, source_slug, existing))
            return
        add(old_fp, new_name, old_id, new_id)

    devp = root / "_devprocess"
    if not devp.is_dir():
        return renames, id_remap

    # EPICs
    for fp in (devp / "requirements/epics").glob("EPIC-*.md") if (devp / "requirements/epics").is_dir() else []:
        m = re.match(r"^EPIC-(\d+)-(.+)\.md$", fp.name)
        if not m:
            continue
        n = int(m.group(1))
        slug = m.group(2)
        new_name = f"EPIC-{n:02d}-{slug}.md"
        if fp.name != new_name:
            add(fp, new_name, f"EPIC-{m.group(1)}", f"EPIC-{n:02d}")
        id_remap[f"EPIC-{n:03d}"] = f"EPIC-{n:02d}"

    # FEATUREs and FEATs
    feats_dir = devp / "requirements/features"
    if feats_dir.is_dir():
        for fp in feats_dir.glob("FEATURE-*.md"):
            m = re.match(r"^FEATURE-(\d+)([a-z]?)-(.+)\.md$", fp.name)
            if not m:
                continue
            num = m.group(1)
            suffix = m.group(2) or ""
            slug = m.group(3)
            if len(num) == 4:
                ee, ff = int(num[:2]), int(num[2:])
            elif len(num) == 3:
                ee, ff = int(num[0]), int(num[1:])
            else:
                ee, ff = 0, int(num)
            new_name = f"FEAT-{ee:02d}-{ff:02d}{suffix}-{slug}.md"
            add_feature_safe(
                fp, new_name,
                f"FEATURE-{num}{suffix}",
                f"FEAT-{ee:02d}-{ff:02d}{suffix}",
                slug,
            )

    # FIXes
    fixes_dir = devp / "requirements/fixes"
    if fixes_dir.is_dir():
        for fp in fixes_dir.glob("FIX-*.md"):
            m = re.match(r"^FIX-(\d{4})-(\d{2})-(.+)\.md$", fp.name)
            if not m:
                continue
            eeff, nn, slug = m.group(1), m.group(2), m.group(3)
            new_name = f"FIX-{eeff[:2]}-{eeff[2:]}-{nn}-{slug}.md"
            if fp.name != new_name:
                add(fp, new_name, f"FIX-{eeff}-{nn}", f"FIX-{eeff[:2]}-{eeff[2:]}-{nn}")

    # IMPs
    imps_dir = devp / "requirements/improvements"
    if imps_dir.is_dir():
        for fp in imps_dir.glob("IMP-*.md"):
            m = re.match(r"^IMP-(\d{4})-(\d{2})-(.+)\.md$", fp.name)
            if not m:
                continue
            eeff, nn, slug = m.group(1), m.group(2), m.group(3)
            new_name = f"IMP-{eeff[:2]}-{eeff[2:]}-{nn}-{slug}.md"
            if fp.name != new_name:
                add(fp, new_name, f"IMP-{eeff}-{nn}", f"IMP-{eeff[:2]}-{eeff[2:]}-{nn}")

    # ADRs
    adr_dir = devp / "architecture"
    if adr_dir.is_dir():
        for fp in adr_dir.glob("ADR-*.md"):
            m = re.match(r"^ADR-(\d+)-(.+)\.md$", fp.name)
            if not m:
                continue
            n = int(m.group(1))
            slug = m.group(2)
            new_name = f"ADR-{n:02d}-{slug}.md"
            if fp.name != new_name:
                add(fp, new_name, f"ADR-{m.group(1)}", f"ADR-{n:02d}")
            id_remap[f"ADR-{n:03d}"] = f"ADR-{n:02d}"

    # PLANs
    plan_dir = devp / "implementation/plans"
    if plan_dir.is_dir():
        for fp in plan_dir.glob("PLAN-*.md"):
            m = re.match(r"^PLAN-(\d+)-(.+)\.md$", fp.name)
            if not m:
                continue
            n = int(m.group(1))
            slug = m.group(2)
            new_name = f"PLAN-{n:02d}-{slug}.md"
            if fp.name != new_name:
                add(fp, new_name, f"PLAN-{m.group(1)}", f"PLAN-{n:02d}")
            id_remap[f"PLAN-{n:03d}"] = f"PLAN-{n:02d}"

    # EXPLOREs, RESEARCHes (no leading-zero variants since v3)
    analysis = devp / "analysis"
    if analysis.is_dir():
        for prefix in ("EXPLORE", "RESEARCH"):
            for fp in analysis.glob(f"{prefix}-*.md"):
                m = re.match(rf"^{prefix}-(\d+)-(.+)\.md$", fp.name)
                if not m:
                    continue
                n = int(m.group(1))
                slug = m.group(2)
                new_name = f"{prefix}-{n:02d}-{slug}.md"
                if fp.name != new_name:
                    add(fp, new_name, f"{prefix}-{m.group(1)}", f"{prefix}-{n:02d}")
                id_remap[f"{prefix}-{n:03d}"] = f"{prefix}-{n:02d}"

        # Item-BAs (Project-BA, BA-EPIC, BA-FEAT, BA-IMP, BA-FIX).
        # Project-BA `BA-{shortname}.md` is left alone (no numeric ID).
        # Legacy generic `BA-NNN-{slug}.md` cannot be auto-mapped to an
        # Item-BA target without item context, so we warn instead of
        # renaming.
        for fp in analysis.glob("BA-EPIC-*.md"):
            m = re.match(r"^BA-EPIC-(\d+)-(.+)\.md$", fp.name)
            if not m:
                continue
            n = int(m.group(1))
            slug = m.group(2)
            new_name = f"BA-EPIC-{n:02d}-{slug}.md"
            if fp.name != new_name:
                add(fp, new_name, f"BA-EPIC-{m.group(1)}", f"BA-EPIC-{n:02d}")
            id_remap[f"BA-EPIC-{n:03d}"] = f"BA-EPIC-{n:02d}"

        for fp in analysis.glob("BA-FEAT-*.md"):
            m = re.match(r"^BA-FEAT-(\d+)([a-z]?)-(\d+)-(.+)\.md$", fp.name)
            if not m:
                continue
            ee, suffix, ff, slug = (
                int(m.group(1)),
                m.group(2) or "",
                int(m.group(3)),
                m.group(4),
            )
            new_name = f"BA-FEAT-{ee:02d}-{ff:02d}{suffix}-{slug}.md"
            if fp.name != new_name:
                add(
                    fp,
                    new_name,
                    f"BA-FEAT-{m.group(1)}{suffix}-{m.group(3)}",
                    f"BA-FEAT-{ee:02d}-{ff:02d}{suffix}",
                )

        for prefix in ("BA-IMP", "BA-FIX"):
            for fp in analysis.glob(f"{prefix}-*.md"):
                m = re.match(
                    rf"^{prefix}-(\d+)-(\d+)-(\d+)-(.+)\.md$", fp.name
                )
                if not m:
                    continue
                ee, ff, nn, slug = (
                    int(m.group(1)),
                    int(m.group(2)),
                    int(m.group(3)),
                    m.group(4),
                )
                new_name = f"{prefix}-{ee:02d}-{ff:02d}-{nn:02d}-{slug}.md"
                if fp.name != new_name:
                    add(
                        fp,
                        new_name,
                        f"{prefix}-{m.group(1)}-{m.group(2)}-{m.group(3)}",
                        f"{prefix}-{ee:02d}-{ff:02d}-{nn:02d}",
                    )

    return renames, id_remap, skipped


def warn_legacy_generic_ba(root: Path) -> None:
    """Surface ambiguous legacy BA files that can not be auto-promoted.

    A `BA-NNN-{slug}.md` file in `analysis/` is either an old generic
    item-BA (no item type encoded) or a project-BA with a numeric prefix
    that pre-dates the v3 naming. We do not guess; we list them so the
    user can rename manually based on the file's content.
    """
    analysis = root / "_devprocess" / "analysis"
    if not analysis.is_dir():
        return
    legacy = []
    for fp in analysis.glob("BA-*.md"):
        if re.match(
            r"^BA-(EPIC|FEAT|IMP|FIX)-",
            fp.name,
        ):
            continue
        if re.match(r"^BA-\d+-.+\.md$", fp.name):
            legacy.append(fp.name)
    if legacy:
        print(
            "WARN legacy generic BA files (manual decision required, "
            "no auto-rename):"
        )
        for name in legacy:
            print(f"  - {name}")
        print(
            "  Rename to BA-{PROJECT}.md (Project-BA) or to "
            "BA-EPIC-NN-{slug}.md / BA-FEAT-EE-FF-{slug}.md / "
            "BA-IMP-EE-FF-NN-{slug}.md / BA-FIX-EE-FF-NN-{slug}.md "
            "based on the file's actual scope."
        )


def apply_replacements_pass1(content: str, sorted_remap: list[tuple[str, str]]) -> str:
    for old, new in sorted_remap:
        pattern = re.compile(r"(?<![A-Z0-9-])" + re.escape(old) + r"(?![\dA-Z])")
        content = pattern.sub(new, content)
    return content


def apply_replacements_pass2(content: str) -> str:
    """Catch-all sweep for legacy IDs that have no corresponding file."""
    def feat_4digit(m: re.Match[str]) -> str:
        num = m.group(1)
        suffix = m.group(2) or ""
        if len(num) == 4:
            return f"FEAT-{int(num[:2]):02d}-{int(num[2:]):02d}{suffix}"
        if len(num) == 3:
            return f"FEAT-{int(num[0]):02d}-{int(num[1:]):02d}{suffix}"
        return m.group(0)

    content = re.sub(r"\bFEATURE-(\d{3,4})([a-z]?)\b", feat_4digit, content)
    content = re.sub(r"\bFEATURE-(\d{2,3})-(\d{2,3})\b",
                     lambda m: f"FEAT-{int(m.group(1)):02d}-{int(m.group(2)):02d}",
                     content)
    content = re.sub(r"\bEPIC-(\d{3})\b",
                     lambda m: f"EPIC-{int(m.group(1)):02d}", content)
    content = re.sub(r"\bADR-(\d{3})\b",
                     lambda m: f"ADR-{int(m.group(1)):02d}", content)
    content = re.sub(r"\bPLAN-(\d{3})\b",
                     lambda m: f"PLAN-{int(m.group(1)):02d}", content)
    content = re.sub(r"\bBA-EPIC-(\d{3})\b",
                     lambda m: f"BA-EPIC-{int(m.group(1)):02d}", content)
    content = re.sub(r"\bBA-FEAT-(\d{2,3})-(\d{2,3})\b",
                     lambda m: f"BA-FEAT-{int(m.group(1)):02d}-{int(m.group(2)):02d}",
                     content)
    content = re.sub(r"\bBA-IMP-(\d{2,3})-(\d{2,3})-(\d{2,3})\b",
                     lambda m: f"BA-IMP-{int(m.group(1)):02d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}",
                     content)
    content = re.sub(r"\bBA-FIX-(\d{2,3})-(\d{2,3})-(\d{2,3})\b",
                     lambda m: f"BA-FIX-{int(m.group(1)):02d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}",
                     content)
    content = re.sub(r"\bEXPLORE-(\d{3})\b",
                     lambda m: f"EXPLORE-{int(m.group(1)):02d}", content)
    content = re.sub(r"\bRESEARCH-(\d{3})\b",
                     lambda m: f"RESEARCH-{int(m.group(1)):02d}", content)
    return content


SOURCE_TREE_DIRS = ("src", "tests", "test", "docs", "lib", "app")
SOURCE_TREE_EXTENSIONS = (
    ".ts", ".tsx", ".js", ".jsx", ".py", ".go", ".rs",
    ".java", ".kt", ".swift", ".cs", ".rb", ".sh", ".md",
)


def collect_source_tree_targets(root: Path) -> list[Path]:
    """Files under src/, tests/, docs/, etc. that may carry legacy
    `FEATURE-NNNN`-style IDs in code comments or out-of-_devprocess
    docs. Excludes hidden dirs and common build artefact roots.
    """
    out: list[Path] = []
    excluded = {".git", "node_modules", "dist", "build", ".venv", "venv", "__pycache__"}
    for top in SOURCE_TREE_DIRS:
        base = root / top
        if not base.is_dir():
            continue
        for fp in base.rglob("*"):
            if not fp.is_file():
                continue
            if any(part in excluded for part in fp.parts):
                continue
            if fp.suffix.lower() not in SOURCE_TREE_EXTENSIONS:
                continue
            out.append(fp)
    return out


def report_thematic_conflicts(skipped: list[tuple[str, str, str, str]]) -> None:
    if not skipped:
        return
    print()
    print(
        "WARN thematic-mismatch (renames skipped, manual decision required):"
    )
    for old_id, new_id, source_slug, existing_title in skipped:
        print(f"  - {old_id} -> {new_id}")
        print(f"    Source slug:    {source_slug}")
        print(f"    Existing title: {existing_title}")
    print(
        "  These pairs share a numeric prefix but appear to describe different "
        "features. Renumber the source feature to a new unused FEAT-EE-FF "
        "(under the correct epic) and rerun, or remove the existing row first."
    )


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()

    warn_legacy_generic_ba(root)

    renames, id_remap, skipped = collect_renames(root)
    sorted_remap = sorted(id_remap.items(), key=lambda x: -len(x[0]))

    print(f"Rename plan: {len(renames)} files")
    print(f"ID-remap entries: {len(id_remap)}")

    targets = list((root / "_devprocess").rglob("*.md")) if (root / "_devprocess").is_dir() else []
    arch_map = root / "src/ARCHITECTURE.map"
    if arch_map.is_file():
        targets.append(arch_map)

    skip = {root / "_devprocess/context/HANDOFFS.md"}

    pass1_count = 0
    for fp in targets:
        if fp in skip or not fp.is_file():
            continue
        original = fp.read_text(encoding="utf-8")
        updated = apply_replacements_pass1(original, sorted_remap)
        if updated != original:
            fp.write_text(updated, encoding="utf-8")
            pass1_count += 1
    print(f"Pass 1 (file-backed renames) updated {pass1_count} files")

    for old, new in renames:
        if old.exists():
            old.rename(new)
    print(f"Renamed {len(renames)} files")

    pass2_count = 0
    for fp in targets:
        if fp in skip or not fp.is_file():
            continue
        if not fp.exists():  # may have been renamed
            continue
        original = fp.read_text(encoding="utf-8")
        updated = apply_replacements_pass2(original)
        if updated != original:
            fp.write_text(updated, encoding="utf-8")
            pass2_count += 1
    print(f"Pass 2 (catch-all sweep) updated {pass2_count} files")

    # Pass 3: source tree (src/, tests/, docs/, ...). Code comments
    # and out-of-_devprocess docs were untouched before; legacy
    # `FEATURE-NNNN` markers used to survive the migration silently.
    pass3_count = 0
    pass3_files: list[str] = []
    for fp in collect_source_tree_targets(root):
        try:
            original = fp.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        updated = apply_replacements_pass1(original, sorted_remap)
        updated = apply_replacements_pass2(updated)
        if updated != original:
            fp.write_text(updated, encoding="utf-8")
            pass3_count += 1
            try:
                pass3_files.append(str(fp.relative_to(root)))
            except ValueError:
                pass3_files.append(str(fp))
    print(f"Pass 3 (source-tree sweep) updated {pass3_count} files")
    for path in pass3_files[:50]:
        print(f"  - {path}")
    if len(pass3_files) > 50:
        print(f"  ... and {len(pass3_files) - 50} more")

    report_thematic_conflicts(skipped)

    return 0


if __name__ == "__main__":
    sys.exit(main())
