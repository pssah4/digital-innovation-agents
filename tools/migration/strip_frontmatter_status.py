#!/usr/bin/env python3
"""DIA migration -- Phase 2a: strip status fields from artifact YAML frontmatter.

Removes top-level keys `status`, `phase`, `last_updated`, `last-updated`,
`lastUpdated` from the frontmatter of every artifact file under
`_devprocess/`. Multi-line values are removed entirely.

Idempotent. Run twice -> second run reports zero changes.

Usage:
    python3 strip_frontmatter_status.py [project_root]
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

STRIP_KEYS = {"status", "phase", "last_updated", "last-updated", "lastupdated"}
TARGET_PATTERNS = [
    "_devprocess/requirements/features/FEAT*.md",
    "_devprocess/requirements/features/FEATURE*.md",
    "_devprocess/requirements/epics/EPIC-*.md",
    "_devprocess/architecture/ADR-*.md",
    "_devprocess/implementation/plans/PLAN-*.md",
    "_devprocess/context/fixes/*.md",
    "_devprocess/context/improvements/*.md",
    "_devprocess/requirements/fixes/*.md",
    "_devprocess/requirements/improvements/*.md",
]
FM = re.compile(r"^---\s*$")


def strip(content: str) -> tuple[str, list[str]]:
    lines = content.split("\n")
    if len(lines) < 2 or not FM.match(lines[0]):
        return content, []
    end = None
    for i in range(1, len(lines)):
        if FM.match(lines[i]):
            end = i
            break
    if end is None:
        return content, []
    fm_lines = lines[1:end]
    body_lines = lines[end:]
    new_fm: list[str] = []
    removed: list[str] = []
    skip = False
    for line in fm_lines:
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:", line)
        if m:
            key = m.group(1).lower().replace("_", "")
            if key in {k.replace("_", "").replace("-", "") for k in STRIP_KEYS}:
                removed.append(line.strip())
                skip = True
                continue
            skip = False
            new_fm.append(line)
        elif skip and (line.startswith(" ") or line.startswith("\t") or line.strip().startswith("-")):
            removed.append(line.strip())
            continue
        else:
            skip = False
            new_fm.append(line)
    if not removed:
        return content, []
    return "---\n" + "\n".join(new_fm) + "\n" + "\n".join(body_lines), removed


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    total = changed = removed_total = 0
    samples: list[tuple[str, list[str]]] = []
    for pattern in TARGET_PATTERNS:
        for fp in root.glob(pattern):
            if not fp.is_file():
                continue
            total += 1
            content = fp.read_text(encoding="utf-8")
            new, removed = strip(content)
            if removed:
                changed += 1
                removed_total += len(removed)
                fp.write_text(new, encoding="utf-8")
                if len(samples) < 5:
                    samples.append((str(fp.relative_to(root)), removed))
    print(f"Files scanned: {total}")
    print(f"Files modified: {changed}")
    print(f"Total fields removed: {removed_total}")
    if samples:
        print("\nSample removals:")
        for fp, rems in samples:
            print(f"  {fp}")
            for r in rems:
                print(f"    - {r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
