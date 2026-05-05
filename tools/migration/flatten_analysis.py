#!/usr/bin/env python3
"""DIA migration -- Phase 4: flatten analysis/ to four prefixes.

Reduces _devprocess/analysis/ to {BA-, EXPLORE-, RESEARCH-, AUDIT-}.
Renames CODEBASE-/DESIGN-/SECURITY-/SPIKE- and one-off prefixes
(FINDING-, ROOT-CAUSE-, GAP-ANALYSE-, SOLUTION-PROPOSAL-, SCAFFOLD-,
MOBILE-, STANDALONE-, TEMPLATE-, REVIEW-, ANALYSIS-, HANDOFF-) to
RESEARCH-NN-{originalprefix-slug}, preserving the old prefix in the
slug for traceability.

Moves analysis/security/AUDIT-* to analysis/ root.
Removes analysis/security/ and analysis/archive/ if empty after moves.

Idempotent.

Usage:
    python3 flatten_analysis.py [project_root]
"""
from __future__ import annotations
import re
import shutil
import sys
from pathlib import Path

CONVERT_PREFIXES = (
    "CODEBASE", "DESIGN", "SECURITY", "SPIKE",
    "FINDING", "ROOT-CAUSE", "GAP-ANALYSE", "SOLUTION-PROPOSAL",
    "SCAFFOLD", "MOBILE", "STANDALONE", "TEMPLATE", "REVIEW", "ANALYSIS",
)


def next_research_num(adir: Path) -> int:
    nums = []
    for fp in adir.glob("RESEARCH-*.md"):
        m = re.match(r"RESEARCH-(\d+)", fp.name)
        if m:
            nums.append(int(m.group(1)))
    return (max(nums) + 1) if nums else 1


def relocate_legacy_epic_ba(root: Path, adir: Path) -> int:
    """Move legacy mini-BA files (`EPIC-{nn}-ba.md`) from
    `_devprocess/requirements/epics/` to
    `_devprocess/analysis/BA-EPIC-{nn}-{slug}.md`. Slug is taken from
    the sibling EPIC-{nn}-{slug}.md file. Returns the number of files
    moved.
    """
    epics_dir = root / "_devprocess/requirements/epics"
    if not epics_dir.is_dir():
        return 0
    moved = 0
    for fp in sorted(epics_dir.glob("EPIC-*-ba.md")):
        m = re.match(r"^EPIC-(\d+)-ba\.md$", fp.name)
        if not m:
            continue
        nn_raw = m.group(1)
        nn = int(nn_raw)
        siblings = list(epics_dir.glob(f"EPIC-{nn_raw}-*.md")) + list(
            epics_dir.glob(f"EPIC-{nn:02d}-*.md")
        )
        slug = None
        for sib in siblings:
            sm = re.match(rf"^EPIC-(?:{nn_raw}|{nn:02d})-(.+)\.md$", sib.name)
            if sm and sm.group(1) != "ba":
                slug = sm.group(1)
                break
        if slug is None:
            slug = "untitled"
            print(
                f"  WARN no sibling EPIC-{nn:02d}-*.md for {fp.name}, "
                f"using slug 'untitled'"
            )
        target = adir / f"BA-EPIC-{nn:02d}-{slug}.md"
        if target.exists():
            print(
                f"  SKIP target exists: {target.relative_to(root)} "
                f"(legacy {fp.relative_to(root)} not moved)"
            )
            continue
        adir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(fp), str(target))
        print(f"  moved {fp.relative_to(root)} -> {target.relative_to(root)}")
        moved += 1
    return moved


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    adir = root / "_devprocess/analysis"
    if not adir.is_dir():
        print("No _devprocess/analysis/ found, nothing to flatten")
        # Still try to move legacy mini-BAs into the (about-to-exist)
        # analysis dir, otherwise the user keeps them next to the EPIC.
        if (root / "_devprocess/requirements/epics").is_dir() and any(
            (root / "_devprocess/requirements/epics").glob("EPIC-*-ba.md")
        ):
            adir.mkdir(parents=True, exist_ok=True)
            relocate_legacy_epic_ba(root, adir)
        return 0

    relocated = relocate_legacy_epic_ba(root, adir)
    if relocated:
        print(f"  Relocated {relocated} legacy EPIC-*-ba.md files to analysis/")

    sec = adir / "security"
    if sec.is_dir():
        for fp in sorted(sec.glob("AUDIT-*.md")):
            target = adir / fp.name
            if target.exists():
                continue
            shutil.move(str(fp), str(target))
            print(f"  moved {fp.relative_to(root)} -> {target.relative_to(root)}")
        for fp in sorted(sec.glob("*.md")):
            new_n = next_research_num(adir)
            slug = fp.stem
            new_name = f"RESEARCH-{new_n:02d}-{slug.lower().replace(' ', '-')}.md"
            target = adir / new_name
            shutil.move(str(fp), str(target))
            print(f"  moved {fp.relative_to(root)} -> {target.relative_to(root)}")
        try:
            sec.rmdir()
        except OSError:
            pass

    archive = adir / "archive"
    if archive.is_dir():
        for fp in sorted(archive.iterdir()):
            print(f"  WARNING: archive content remains: {fp.relative_to(root)}")
        try:
            shutil.rmtree(archive)
            print(f"  removed {archive.relative_to(root)}")
        except OSError:
            pass

    next_n = next_research_num(adir)
    converted = 0
    for prefix in CONVERT_PREFIXES:
        for fp in sorted(adir.glob(f"{prefix}-*.md")):
            m = re.match(rf"{prefix}-(\d+)-(.+)\.md", fp.name)
            if not m:
                m2 = re.match(rf"{prefix}-(.+)\.md", fp.name)
                if not m2:
                    continue
                slug = m2.group(1)
            else:
                slug = m.group(2)
            new_slug = f"{prefix.lower()}-{slug}"
            new_name = f"RESEARCH-{next_n:02d}-{new_slug}.md"
            target = adir / new_name
            fp.rename(target)
            print(f"  renamed {fp.name} -> {target.name}")
            next_n += 1
            converted += 1

    print(f"\nFlatten complete. Converted {converted} files to RESEARCH-NN.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
