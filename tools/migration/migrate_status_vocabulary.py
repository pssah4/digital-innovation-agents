#!/usr/bin/env python3
"""
DIA migration step: status vocabulary alignment.

Migrates backlog Status column values from the legacy DIA vocabulary to
the GitHub-aligned vocabulary. After this step, BACKLOG.md and GitHub
Project boards share a single status set, so flow.py sync-status can
mirror 1:1 without translation.

Mapping:
    Planned   -> Ready
    Active    -> In Progress
    Review    -> In Review
    Done      -> Done           (unchanged)
    Waiting   -> Backlog
    Deferred  -> Backlog

The script edits only the Status column (index 3 by the BACKLOG template
schema, accounting for the leading empty cell from the markdown table
delimiter). Other columns and the table layout are preserved.

Idempotent. A second run finds zero rows to migrate.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


STATUS_MAP = {
    "Planned": "Ready",
    "Active": "In Progress",
    "Review": "In Review",
    "Done": "Done",
    "Waiting": "Backlog",
    "Deferred": "Backlog",
}

# Status column is the 4th data cell (1-indexed) per BACKLOG-TEMPLATE.md:
# ID | Type | Title | Status | Phase | Prio | Refs | Source | Commit |
# Claim | Last change | Notes
# In a parsed split('|') of "| a | b | c |" we get ['', 'a', 'b', 'c', '']
# so column index 4 in the resulting list is the Status column.
STATUS_COLUMN_INDEX = 4

# A row is a data row if it starts with a recognised item id pattern.
ITEM_ID_RE = re.compile(
    r"^(EPIC-\d{2}|FEAT-\d{2}-\d{2}|FIX-\d{2}-\d{2}-\d{2}|IMP-\d{2}-\d{2}-\d{2}|ADR-\d{2}|PLAN-\d{2}|BL-\d+)"
)


def find_backlog(repo_root: Path) -> Path | None:
    candidate = repo_root / "_devprocess" / "context" / "BACKLOG.md"
    return candidate if candidate.exists() else None


def is_data_row(line: str) -> bool:
    if not line.startswith("|"):
        return False
    # Skip header and separator rows.
    if "---" in line:
        return False
    cells = [c.strip() for c in line.strip("\n").split("|")]
    if len(cells) < 6:
        return False
    return bool(ITEM_ID_RE.match(cells[1])) if len(cells) > 1 else False


def migrate_row(line: str) -> tuple[str, str | None, str | None]:
    """Return (new_line, old_status, new_status) tuple.

    If the row is not a data row or the status is already in the new
    vocabulary, returns (line, None, None).
    """
    if not is_data_row(line):
        return line, None, None
    cells = line.rstrip("\n").split("|")
    if len(cells) <= STATUS_COLUMN_INDEX:
        return line, None, None
    old_value = cells[STATUS_COLUMN_INDEX].strip()
    if old_value not in STATUS_MAP:
        return line, None, None
    new_value = STATUS_MAP[old_value]
    if new_value == old_value:
        return line, None, None
    # Preserve leading and trailing whitespace style.
    cells[STATUS_COLUMN_INDEX] = f" {new_value} "
    new_line = "|".join(cells) + ("\n" if line.endswith("\n") else "")
    return new_line, old_value, new_value


def migrate_backlog(path: Path, dry_run: bool = False) -> dict:
    """Run the migration on BACKLOG.md. Returns a summary dict."""
    text = path.read_text(encoding="utf-8")
    new_lines: list[str] = []
    counters: dict[str, int] = {}
    for raw in text.splitlines(keepends=True):
        new_line, old, new = migrate_row(raw)
        if old is not None and new is not None and old != new:
            key = f"{old} -> {new}"
            counters[key] = counters.get(key, 0) + 1
        new_lines.append(new_line)
    new_text = "".join(new_lines)
    changed = new_text != text
    if changed and not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return {
        "path": str(path),
        "changed": changed,
        "dry_run": dry_run,
        "rows_changed": sum(counters.values()),
        "by_mapping": counters,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="migrate BACKLOG.md status vocabulary to GitHub-aligned set",
    )
    parser.add_argument(
        "--repo-root", default=".",
        help="repo root containing _devprocess/context/BACKLOG.md (default: cwd)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="report changes without writing",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    backlog = find_backlog(repo_root)
    if not backlog:
        print(json.dumps({
            "error": "BACKLOG.md not found",
            "expected_at": str(repo_root / "_devprocess" / "context" / "BACKLOG.md"),
        }, indent=2))
        return 1
    summary = migrate_backlog(backlog, dry_run=args.dry_run)
    print(json.dumps(summary, indent=2))
    return 0 if not summary.get("error") else 1


if __name__ == "__main__":
    sys.exit(main())
