#!/usr/bin/env python3
"""
DIA team-workflow flow driver.

Orchestrates the GitHub-side artefacts (issue, project card, draft PR,
phase tags) for a backlog item as it walks through the V-Model phases.
The backlog truth lives in `_devprocess/context/BACKLOG.md`; this
script keeps the GitHub view in sync.

Subcommands:
    create-issue     Create a GitHub issue for a backlog item.
    tag-phase        Set the `<item-id>/<phase>-done` annotated git tag.
    update-issue     Update issue body checklist and phase label.
    open-draft-pr    Open a draft PR for the item branch.
    ready-for-review Flip the draft PR to ready and tag ready-for-review.
    status           Print state of the item (branch, tags, issue, PR).

All subcommands are idempotent. Re-running on an already-current
state is a no-op with a clear status message.

GitHub integration uses `gh` CLI. If `gh` is not installed or no
GitHub remote is configured, the script falls back to local-only
mode (only the git tag is set; no issue/PR/label updates).

Usage:
    python3 tools/github-integration/flow.py <subcommand> [args]
    python3 tools/github-integration/flow.py status --item FEAT-04-09
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

VALID_PHASES = ("ba", "re", "arch", "code", "test", "audit", "ready-for-review")
ITEM_RE = re.compile(r"^(EPIC-\d{2}|FEAT-\d{2}-\d{2}|FIX-\d{2}-\d{2}-\d{2}|IMP-\d{2}-\d{2}-\d{2})$")


def repo_root() -> Path:
    return Path(subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True
    ).strip())


def run(cmd: list[str], check: bool = True, capture: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=check, text=True, capture_output=capture)


def has_gh() -> bool:
    try:
        run(["gh", "--version"])
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def gh_repo_configured() -> bool:
    if not has_gh():
        return False
    try:
        out = run(["gh", "repo", "view", "--json", "name"]).stdout
        return bool(out.strip())
    except subprocess.CalledProcessError:
        return False


def normalize_item(item: str) -> str:
    item = item.strip().upper()
    if not ITEM_RE.match(item):
        sys.exit(f"ERROR: invalid item id '{item}'. Expected EPIC-NN, FEAT-EE-FF, FIX-EE-FF-NN, or IMP-EE-FF-NN.")
    return item


def item_branch_prefix(item: str) -> str:
    """feature/fix/chore based on item type."""
    if item.startswith(("FEAT-", "EPIC-")):
        return "feature"
    if item.startswith("FIX-"):
        return "fix"
    if item.startswith("IMP-"):
        return "chore"
    return "feature"


def expected_branch(item: str, slug: str = "") -> str:
    prefix = item_branch_prefix(item)
    base = item.lower()
    if slug:
        return f"{prefix}/{base}-{slug}"
    return f"{prefix}/{base}"


def current_branch() -> str:
    return run(["git", "rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()


def branch_matches_item(branch: str, item: str) -> bool:
    item_lower = item.lower()
    return f"/{item_lower}-" in branch or branch.endswith(f"/{item_lower}")


# ---------- Backlog row parsing -----------------------------------------

def backlog_path() -> Path:
    return repo_root() / "_devprocess" / "context" / "BACKLOG.md"


def find_backlog_row(item: str) -> dict | None:
    """Find the row for `item` in BACKLOG.md. Returns dict with parsed
    columns, or None.
    """
    bl = backlog_path()
    if not bl.exists():
        return None
    text = bl.read_text(encoding="utf-8")
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells and cells[0] == item:
            return {"raw": line, "cells": cells}
    return None


def title_for_item(item: str) -> str:
    row = find_backlog_row(item)
    if row and len(row["cells"]) > 2:
        return row["cells"][2]
    return item


def priority_for_item(item: str) -> str:
    row = find_backlog_row(item)
    if not row:
        return "p2"
    raw = row["raw"]
    for p in ("P0", "P1", "P2", "P3"):
        if p in raw:
            return p.lower()
    return "p2"


def type_label(item: str) -> str:
    if item.startswith("FEAT-"):
        return "feature"
    if item.startswith("EPIC-"):
        return "epic"
    if item.startswith("FIX-"):
        return "fix"
    if item.startswith("IMP-"):
        return "improvement"
    return "feature"


# ---------- GitHub issue lookup -----------------------------------------

def find_issue_for_item(item: str) -> dict | None:
    """Search open issues whose title starts with the item id."""
    if not gh_repo_configured():
        return None
    try:
        out = run([
            "gh", "issue", "list",
            "--search", f"{item} in:title",
            "--state", "all",
            "--json", "number,title,url,state",
            "--limit", "5",
        ]).stdout
    except subprocess.CalledProcessError:
        return None
    issues = json.loads(out)
    for issue in issues:
        if issue["title"].startswith(item) or f"[{item}]" in issue["title"]:
            return issue
    return None


# ---------- Subcommand: create-issue ------------------------------------

def cmd_create_issue(args: argparse.Namespace) -> int:
    item = normalize_item(args.item)

    if not gh_repo_configured():
        print(f"[create-issue] gh CLI / GitHub remote not configured -- skipping (local-only mode)")
        return 0

    existing = find_issue_for_item(item)
    if existing:
        print(f"[create-issue] issue exists: {existing['url']}")
        return 0

    title = f"{item}: {title_for_item(item)}"
    body = build_issue_body(item)
    labels = [type_label(item), priority_for_item(item), "phase:planned"]

    cmd = ["gh", "issue", "create", "--title", title, "--body", body]
    for lbl in labels:
        cmd.extend(["--label", lbl])
    try:
        out = run(cmd).stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"[create-issue] gh issue create failed. stderr: {e.stderr}", file=sys.stderr)
        return 1

    print(f"[create-issue] created: {out}")
    write_issue_into_backlog(item, out)
    return 0


def build_issue_body(item: str) -> str:
    title = title_for_item(item)
    epic = ""
    if item.startswith("FEAT-"):
        epic = f"EPIC-{item.split('-')[1]}"
    return f"""**Backlog item:** [{item}](_devprocess/context/BACKLOG.md)
**Type:** {type_label(item).title()}
**Epic:** {epic}
**Priority:** {priority_for_item(item).upper()}

## Description
{title}

## V-Model phases (auto-tracked)
- [ ] BA -- business-analysis
- [ ] RE -- requirements-engineering
- [ ] Architecture
- [ ] Coding
- [ ] Testing
- [ ] Security-Audit
- [ ] Ready for review

The DIA agent updates this checklist as phase tags are set.
Source of truth: `_devprocess/context/BACKLOG.md`. PR: TBD.
"""


def write_issue_into_backlog(item: str, issue_url: str) -> None:
    """Append `Issue: <url>` to the backlog row's Notes column.
    Idempotent: skip if already present.
    """
    bl = backlog_path()
    if not bl.exists():
        return
    text = bl.read_text(encoding="utf-8")
    if issue_url in text:
        return
    new_lines = []
    written = False
    for line in text.splitlines(keepends=True):
        if not written and line.startswith(f"| {item} ") and issue_url not in line:
            stripped = line.rstrip("\n").rstrip()
            if stripped.endswith("|"):
                line = stripped[:-1] + f" Issue: {issue_url} |\n"
            written = True
        new_lines.append(line)
    if written:
        bl.write_text("".join(new_lines), encoding="utf-8")


# ---------- Subcommand: tag-phase ---------------------------------------

PHASE_MESSAGES = {
    "ba": "Business analysis complete: validated, backlog updated.",
    "re": "Requirements engineering complete: feature spec and SCs.",
    "arch": "Architecture complete: ADRs / arc42 / plan-context.",
    "code": "Coding complete: implementation committed, build green.",
    "test": "Testing complete: tests added, coverage check passed.",
    "audit": "Security audit complete: report written, findings filed.",
    "ready-for-review": "All required phases complete; PR ready for review.",
}


def cmd_tag_phase(args: argparse.Namespace) -> int:
    item = normalize_item(args.item)
    phase = args.phase
    if phase not in VALID_PHASES:
        sys.exit(f"ERROR: invalid phase '{phase}'. Valid: {', '.join(VALID_PHASES)}")
    cur = current_branch()
    if not branch_matches_item(cur, item) and cur not in ("main", "master", "dev"):
        print(f"[tag-phase] WARNING: current branch '{cur}' does not match item '{item}'.")
    tag_name = f"{item.lower()}/{phase}-done"
    try:
        existing = run(["git", "tag", "--list", tag_name]).stdout.strip()
    except subprocess.CalledProcessError:
        existing = ""
    if existing:
        print(f"[tag-phase] tag '{tag_name}' already exists -- no-op")
        return 0

    msg = PHASE_MESSAGES.get(phase, f"{phase} complete for {item}")
    try:
        run(["git", "tag", "-a", tag_name, "-m", msg])
    except subprocess.CalledProcessError as e:
        print(f"[tag-phase] git tag failed: {e.stderr}", file=sys.stderr)
        return 1
    print(f"[tag-phase] created annotated tag: {tag_name}")

    # Push tag if a remote is configured.
    try:
        run(["git", "push", "origin", tag_name], check=False)
    except Exception:
        pass

    update_issue_after_tag(item, phase)
    return 0


def update_issue_after_tag(item: str, phase: str) -> None:
    if not gh_repo_configured():
        return
    issue = find_issue_for_item(item)
    if not issue:
        return
    # Update checklist in body
    try:
        out = run(["gh", "issue", "view", str(issue["number"]), "--json", "body"]).stdout
        body = json.loads(out).get("body", "")
    except subprocess.CalledProcessError:
        return
    new_body = tick_checklist(body, phase)
    if new_body != body:
        try:
            run(["gh", "issue", "edit", str(issue["number"]), "--body", new_body])
        except subprocess.CalledProcessError:
            pass
    # Update phase label
    label_map = {
        "ba": "phase:ba",
        "re": "phase:re",
        "arch": "phase:arch",
        "code": "phase:coding",
        "test": "phase:testing",
        "audit": "phase:audit",
        "ready-for-review": "phase:review",
    }
    new_label = label_map.get(phase)
    if new_label:
        # Remove other phase labels, add the new one
        for lbl in label_map.values():
            if lbl != new_label:
                run(["gh", "issue", "edit", str(issue["number"]), "--remove-label", lbl], check=False)
        run(["gh", "issue", "edit", str(issue["number"]), "--add-label", new_label], check=False)


def tick_checklist(body: str, phase: str) -> str:
    pattern_map = {
        "ba": r"- \[ \] BA",
        "re": r"- \[ \] RE",
        "arch": r"- \[ \] Architecture",
        "code": r"- \[ \] Coding",
        "test": r"- \[ \] Testing",
        "audit": r"- \[ \] Security-Audit",
        "ready-for-review": r"- \[ \] Ready for review",
    }
    rx = pattern_map.get(phase)
    if not rx:
        return body
    return re.sub(rx, lambda m: m.group(0).replace("[ ]", "[x]"), body, count=1)


# ---------- Subcommand: open-draft-pr -----------------------------------

def cmd_open_draft_pr(args: argparse.Namespace) -> int:
    item = normalize_item(args.item)
    if not gh_repo_configured():
        print("[open-draft-pr] gh CLI / GitHub remote not configured -- skipping")
        return 0
    cur = current_branch()
    if not branch_matches_item(cur, item):
        print(f"[open-draft-pr] current branch '{cur}' does not match item '{item}'. Refusing.", file=sys.stderr)
        return 1
    # Check existing PR
    try:
        out = run(["gh", "pr", "view", "--json", "url,isDraft,number"], check=False).stdout
        if out.strip():
            data = json.loads(out)
            print(f"[open-draft-pr] PR already exists: {data['url']} (draft={data['isDraft']})")
            return 0
    except subprocess.CalledProcessError:
        pass
    issue = find_issue_for_item(item)
    body = f"Closes #{issue['number']}\n\nWork in progress for `{item}`. The DIA agent updates phase tags as the work progresses." if issue else f"Work in progress for `{item}`."
    title = f"{item}: {title_for_item(item)}"
    try:
        out = run([
            "gh", "pr", "create",
            "--draft",
            "--base", "dev",
            "--title", title,
            "--body", body,
        ]).stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"[open-draft-pr] gh pr create failed: {e.stderr}", file=sys.stderr)
        return 1
    print(f"[open-draft-pr] draft PR created: {out}")
    return 0


# ---------- Subcommand: ready-for-review --------------------------------

def cmd_ready_for_review(args: argparse.Namespace) -> int:
    item = normalize_item(args.item)
    required = ("code-done", "test-done")
    if args.with_audit:
        required = required + ("audit-done",)
    missing = []
    for r in required:
        tag = f"{item.lower()}/{r}"
        out = run(["git", "tag", "--list", tag]).stdout.strip()
        if not out:
            missing.append(tag)
    if missing:
        print(f"[ready-for-review] missing required tags: {', '.join(missing)}", file=sys.stderr)
        return 1
    cmd_tag_phase(argparse.Namespace(item=item, phase="ready-for-review"))
    if gh_repo_configured():
        run(["gh", "pr", "ready"], check=False)
    return 0


# ---------- Subcommand: status ------------------------------------------

def cmd_status(args: argparse.Namespace) -> int:
    item = normalize_item(args.item)
    print(f"=== Status for {item} ===")
    cur = current_branch()
    print(f"Branch (current):       {cur}")
    print(f"Branch matches item:    {branch_matches_item(cur, item)}")
    print()
    print("Phase tags:")
    for phase in VALID_PHASES:
        tag = f"{item.lower()}/{phase}-done"
        out = run(["git", "tag", "--list", tag]).stdout.strip()
        marker = "x" if out else " "
        print(f"  [{marker}] {tag}")
    print()
    if gh_repo_configured():
        issue = find_issue_for_item(item)
        if issue:
            print(f"GitHub issue:           {issue['url']} (state={issue['state']})")
        else:
            print("GitHub issue:           not found")
    else:
        print("GitHub:                 not configured (local-only mode)")
    return 0


# ---------- Argparse ----------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("create-issue", help="Create a GitHub issue for the item")
    p1.add_argument("--item", required=True)
    p1.set_defaults(func=cmd_create_issue)

    p2 = sub.add_parser("tag-phase", help="Set the phase-done tag")
    p2.add_argument("--item", required=True)
    p2.add_argument("--phase", required=True, choices=VALID_PHASES)
    p2.set_defaults(func=cmd_tag_phase)

    p3 = sub.add_parser("open-draft-pr", help="Open a draft PR for the item branch")
    p3.add_argument("--item", required=True)
    p3.set_defaults(func=cmd_open_draft_pr)

    p4 = sub.add_parser("ready-for-review", help="Mark PR ready for review")
    p4.add_argument("--item", required=True)
    p4.add_argument("--with-audit", action="store_true",
                    help="Require audit-done tag in addition to code/test")
    p4.set_defaults(func=cmd_ready_for_review)

    p5 = sub.add_parser("status", help="Print state of the item")
    p5.add_argument("--item", required=True)
    p5.set_defaults(func=cmd_status)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
