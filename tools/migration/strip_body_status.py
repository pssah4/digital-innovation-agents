#!/usr/bin/env python3
"""DIA migration -- Phase 2b: strip body-level status declarations.

Removes lines like `**Status:** Implemented`, `> Status: Akzeptiert`,
`Status: Implemented`, `**Last Updated:** ...` from the first 25 body
lines of every artifact file. Frontmatter is left intact (Phase 2a
handles that).

Idempotent.

Usage:
    python3 strip_body_status.py [project_root]
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

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

STATUS_PATTERNS = [
    re.compile(r"^\s*\*\*Status:\*\*\s+.+$", re.IGNORECASE),
    re.compile(r"^\s*>\s*\*\*Status:\*\*\s+.+$", re.IGNORECASE),
    re.compile(r"^\s*>\s*Status:\s+.+$", re.IGNORECASE),
    re.compile(
        r"^\s*Status:\s+(Implemented|Akzeptiert|Accepted|Planned|Geplant|Draft|Done|Active|Review|In Progress|Deprecated|Superseded|Proposed|Vorgeschlagen).*$",
        re.IGNORECASE,
    ),
]
LASTUPDATED_PATTERNS = [
    re.compile(r"^\s*\*\*Last\s+(Updated|Modified):\*\*\s+.+$", re.IGNORECASE),
    re.compile(r"^\s*\*\*Letztes Update:\*\*\s+.+$", re.IGNORECASE),
    re.compile(r"^\s*>\s*\*?\*?Last\s+(Updated|Modified):\*?\*?\s+.+$", re.IGNORECASE),
]
FM = re.compile(r"^---\s*$")


def strip(content: str) -> tuple[str, int]:
    lines = content.split("\n")
    body_start = 0
    if lines and FM.match(lines[0]):
        for i in range(1, len(lines)):
            if FM.match(lines[i]):
                body_start = i + 1
                break
    cutoff = body_start + 25
    new: list[str] = []
    removed = 0
    for i, line in enumerate(lines):
        if body_start <= i < cutoff:
            matched = False
            for p in STATUS_PATTERNS + LASTUPDATED_PATTERNS:
                if p.match(line):
                    removed += 1
                    matched = True
                    break
            if matched:
                continue
        new.append(line)
    return "\n".join(new) if removed else content, removed


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    total = changed = removed_total = 0
    samples: list[tuple[str, int]] = []
    for pattern in TARGET_PATTERNS:
        for fp in root.glob(pattern):
            if not fp.is_file():
                continue
            total += 1
            content = fp.read_text(encoding="utf-8")
            new, removed = strip(content)
            if removed:
                changed += 1
                removed_total += removed
                fp.write_text(new, encoding="utf-8")
                if len(samples) < 5:
                    samples.append((str(fp.relative_to(root)), removed))
    print(f"Files scanned: {total}")
    print(f"Files modified: {changed}")
    print(f"Total status/last-updated lines removed: {removed_total}")
    if samples:
        print("\nSample changes:")
        for fp, n in samples:
            print(f"  {fp}: -{n} lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
