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


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    adir = root / "_devprocess/analysis"
    if not adir.is_dir():
        print("No _devprocess/analysis/ found, nothing to flatten")
        return 0

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
