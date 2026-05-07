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

# Subcommands that require GitHub to be reachable in mode = "github-sync".
# tag-phase and status work locally (only set git tags / read tags), so
# they remain available in git-only mode.
GITHUB_REQUIRED_ACTIONS = (
    "create-issue",
    "update-issue",
    "open-draft-pr",
    "ready-for-review",
    "sync-status",
    "promote-to-epic",
)


def repo_root() -> Path:
    return Path(subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True
    ).strip())


def read_dia_mode() -> str:
    """Read mode from .dia/config.toml. Default git-only when missing.

    The default keeps existing setups (without /dia-setup) working as
    before: local hooks and merge scripts remain active, GitHub sync
    requires explicit github-sync mode.
    """
    try:
        cfg = repo_root() / ".dia" / "config.toml"
    except subprocess.CalledProcessError:
        return "git-only"
    if not cfg.exists():
        return "git-only"
    text = cfg.read_text(encoding="utf-8")
    try:
        import tomllib  # type: ignore[import-not-found]

        data = tomllib.loads(text)
        mode = data.get("mode", "git-only")
        if mode in ("off", "git-only", "github-sync"):
            return mode
    except ModuleNotFoundError:
        match = re.search(r'mode\s*=\s*"([^"]+)"', text)
        if match and match.group(1) in ("off", "git-only", "github-sync"):
            return match.group(1)
    return "git-only"


def read_dia_github_config() -> dict:
    """Read [github] section from .dia/config.toml. Returns {} on missing."""
    try:
        cfg = repo_root() / ".dia" / "config.toml"
    except subprocess.CalledProcessError:
        return {}
    if not cfg.exists():
        return {}
    text = cfg.read_text(encoding="utf-8")
    try:
        import tomllib  # type: ignore[import-not-found]

        data = tomllib.loads(text)
        gh = data.get("github", {})
        return gh if isinstance(gh, dict) else {}
    except ModuleNotFoundError:
        # Minimal scan: extract project_number and repo and status_field
        out: dict = {}
        for key in ("project_number", "repo", "status_field"):
            m = re.search(rf'{key}\s*=\s*("([^"]*)"|(\d+))', text)
            if m:
                out[key] = m.group(2) if m.group(2) is not None else int(m.group(3))
        return out


def mode_active_or_skip(action: str) -> bool:
    """Return True if the action may proceed under the current mode.

    Prints a clear no-op message and returns False otherwise.
    """
    mode = read_dia_mode()
    if action in GITHUB_REQUIRED_ACTIONS and mode != "github-sync":
        print(f"[{action}] mode={mode}, skipping (set mode=github-sync via /dia-setup to enable)")
        return False
    if mode == "off":
        print(f"[{action}] mode=off, skipping (run /dia-setup to change)")
        return False
    return True


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

    if not mode_active_or_skip("create-issue"):
        return 0
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
    # tag-phase always sets the local git tag; only the GitHub-side
    # update is mode-gated below in update_issue_after_tag.
    if read_dia_mode() == "off":
        print("[tag-phase] mode=off, skipping (run /dia-setup to change)")
        return 0
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
    if read_dia_mode() != "github-sync":
        return
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
    if not mode_active_or_skip("open-draft-pr"):
        return 0
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
    if not mode_active_or_skip("ready-for-review"):
        return 0
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


# ---------- Subcommand: sync-status -------------------------------------

# Status passes through unchanged. BACKLOG and GitHub share one
# vocabulary: Backlog, Ready, In Progress, In Review, Done.
# Legacy BACKLOG values from before the stage-3 migration still
# resolve correctly via the legacy table below; once a project has
# run `tools/migration/migrate_status_vocabulary.py`, these entries
# never trigger.
ALLOWED_STATUSES = ("Backlog", "Ready", "In Progress", "In Review", "Done")
LEGACY_STATUS_MAPPING = {
    "Planned": "Ready",
    "Active": "In Progress",
    "Review": "In Review",
    "Done": "Done",
    "Waiting": "Backlog",
    "Deferred": "Backlog",
}


def parse_backlog_columns(row: dict) -> dict:
    """Return a {column_name: value} view of a backlog row.

    The schema lives in skills/requirements-engineering/templates/
    BACKLOG-TEMPLATE.md. Column order:
    ID | Type | Title | Status | Phase | Prio | Refs | Source |
    Commit | Claim | Last change | Notes
    """
    columns = ("id", "type", "title", "status", "phase", "prio",
               "refs", "source", "commit", "claim", "last_change", "notes")
    cells = row.get("cells", [])
    out: dict = {}
    for index, name in enumerate(columns):
        out[name] = cells[index] if index < len(cells) else ""
    return out


def map_status_to_github(backlog_status: str) -> str | None:
    """Return the GitHub status for a BACKLOG status, or None if unknown.

    Pre-stage-3 BACKLOG values are translated via LEGACY_STATUS_MAPPING.
    Already-migrated values pass through unchanged.
    """
    s = backlog_status.strip()
    if s in ALLOWED_STATUSES:
        return s
    if s in LEGACY_STATUS_MAPPING:
        return LEGACY_STATUS_MAPPING[s]
    return None


def github_issue_assignee(issue_number: int) -> str:
    """Return the first assignee login or empty string."""
    try:
        out = run([
            "gh", "issue", "view", str(issue_number),
            "--json", "assignees",
        ]).stdout
    except subprocess.CalledProcessError:
        return ""
    data = json.loads(out)
    assignees = data.get("assignees") or []
    if not assignees:
        return ""
    return assignees[0].get("login", "")


def write_claim_into_backlog(item: str, claim: str) -> bool:
    """Update Claim column for the given item. Returns True if changed."""
    bl = backlog_path()
    if not bl.exists():
        return False
    text = bl.read_text(encoding="utf-8")
    new_lines: list[str] = []
    changed = False
    for raw_line in text.splitlines(keepends=True):
        if not raw_line.startswith(f"| {item} "):
            new_lines.append(raw_line)
            continue
        cells = [c for c in raw_line.rstrip("\n").split("|")]
        # cells[0] is leading empty string before first |, cells[-1] is trailing
        # column count: cells[1..n-1] are real columns (12 columns).
        # claim is at index 10 in this list (1-indexed = 10).
        if len(cells) < 12:
            new_lines.append(raw_line)
            continue
        old = cells[10].strip()
        if old == claim:
            new_lines.append(raw_line)
            continue
        # Preserve leading and trailing space style by minimal substitution.
        cells[10] = f" {claim} "
        new_line = "|".join(cells) + ("\n" if raw_line.endswith("\n") else "")
        new_lines.append(new_line)
        changed = True
    if changed:
        bl.write_text("".join(new_lines), encoding="utf-8")
    return changed


def update_project_status_field(issue_number: int, github_status: str) -> bool:
    """Update the Status field on the configured GitHub Project.

    Requires `[github] project_number = N` (and ideally
    status_field = "Status") in .dia/config.toml. Returns True if the
    project was touched, False if not configured.
    """
    cfg = read_dia_github_config()
    project_number = cfg.get("project_number")
    if not project_number:
        return False
    field_name = cfg.get("status_field", "Status")
    # gh project item-edit requires the project owner; we resolve via
    # gh repo view -> nameWithOwner, then take the owner part.
    try:
        repo_owner = json.loads(run([
            "gh", "repo", "view", "--json", "owner",
        ]).stdout)["owner"]["login"]
    except (subprocess.CalledProcessError, KeyError, json.JSONDecodeError):
        print("[sync-status] could not resolve repo owner; project field skipped",
              file=sys.stderr)
        return False
    # gh project list resolves ProjectV2 IDs by number.
    try:
        out = run([
            "gh", "project", "field-list", str(project_number),
            "--owner", repo_owner, "--format", "json",
        ]).stdout
    except subprocess.CalledProcessError:
        print("[sync-status] gh project field-list failed; project field skipped",
              file=sys.stderr)
        return False
    fields = json.loads(out).get("fields", [])
    target_field = next((f for f in fields if f.get("name") == field_name), None)
    if not target_field:
        print(f"[sync-status] project field '{field_name}' not found; project field skipped")
        return False
    option_id = next(
        (o["id"] for o in target_field.get("options", [])
         if o.get("name") == github_status),
        None,
    )
    if not option_id:
        print(f"[sync-status] project field option '{github_status}' not found")
        return False
    # Resolve item id (project item id) for the given issue.
    try:
        items = json.loads(run([
            "gh", "project", "item-list", str(project_number),
            "--owner", repo_owner, "--format", "json",
        ]).stdout).get("items", [])
    except subprocess.CalledProcessError:
        return False
    matching = next(
        (i for i in items if i.get("content", {}).get("number") == issue_number),
        None,
    )
    if not matching:
        print(f"[sync-status] issue #{issue_number} not in project {project_number}")
        return False
    item_id = matching.get("id")
    project_id = matching.get("projectId") or target_field.get("projectId")
    if not (item_id and project_id):
        return False
    try:
        run([
            "gh", "project", "item-edit",
            "--project-id", project_id,
            "--id", item_id,
            "--field-id", target_field["id"],
            "--single-select-option-id", option_id,
        ])
        return True
    except subprocess.CalledProcessError as e:
        print(f"[sync-status] item-edit failed: {e.stderr}", file=sys.stderr)
        return False


def cmd_sync_status(args: argparse.Namespace) -> int:
    item = normalize_item(args.item)
    if not mode_active_or_skip("sync-status"):
        return 0
    if not gh_repo_configured():
        print("[sync-status] gh CLI / GitHub remote not configured -- skipping")
        return 0
    row = find_backlog_row(item)
    if not row:
        print(f"[sync-status] backlog row not found for {item}")
        return 1
    cols = parse_backlog_columns(row)
    backlog_status = cols.get("status", "").strip()
    if not backlog_status:
        print(f"[sync-status] no Status value for {item} in backlog")
        return 1
    github_status = map_status_to_github(backlog_status)
    if not github_status:
        print(f"[sync-status] unknown backlog status '{backlog_status}'; no GitHub mapping")
        return 1
    issue = find_issue_for_item(item)
    if not issue:
        print(f"[sync-status] no GitHub issue found for {item}")
        return 0
    issue_number = int(issue["number"])

    # Open / closed transition by Done. The check uses the mapped
    # value so legacy backlogs still close on Done correctly.
    target_state = "closed" if github_status == "Done" else "open"
    if issue["state"].lower() != target_state:
        verb = "close" if target_state == "closed" else "reopen"
        try:
            run(["gh", "issue", verb, str(issue_number)])
            print(f"[sync-status] issue #{issue_number} {verb}d (status={backlog_status})")
        except subprocess.CalledProcessError as e:
            print(f"[sync-status] gh issue {verb} failed: {e.stderr}", file=sys.stderr)

    # Project field, if configured.
    if update_project_status_field(issue_number, github_status):
        print(f"[sync-status] project field set to '{github_status}'")
    else:
        print(f"[sync-status] project field not configured; mirrored only via issue state")

    # Claim from assignee back to backlog.
    assignee = github_issue_assignee(issue_number)
    if assignee:
        from datetime import date
        claim = f"{assignee} @ {date.today().isoformat()}"
        if write_claim_into_backlog(item, claim):
            print(f"[sync-status] claim updated in backlog: {claim}")
    return 0


# ---------- Subcommand: promote-to-epic ---------------------------------

def cmd_promote_to_epic(args: argparse.Namespace) -> int:
    item = normalize_item(args.item)
    if not item.startswith("EPIC-"):
        print(f"[promote-to-epic] item must be an EPIC, got {item}", file=sys.stderr)
        return 1
    if not mode_active_or_skip("promote-to-epic"):
        return 0
    if not gh_repo_configured():
        print("[promote-to-epic] gh CLI / GitHub remote not configured -- skipping")
        return 0
    epic_nn = item.split("-", 1)[1]  # "01"
    title = title_for_item(item)
    new_title = f"{item}: {title}"

    parent_issue: dict | None = None
    if args.parent_issue:
        try:
            out = run([
                "gh", "issue", "view", str(args.parent_issue),
                "--json", "number,title,url,state,body",
            ]).stdout
            parent_issue = json.loads(out)
        except subprocess.CalledProcessError as e:
            print(f"[promote-to-epic] parent-issue lookup failed: {e.stderr}", file=sys.stderr)
            return 1
    else:
        parent_issue = find_issue_for_item(item)
    if not parent_issue:
        print(f"[promote-to-epic] no parent issue found; create one first or pass --parent-issue")
        return 1
    parent_number = int(parent_issue["number"])

    # Rename parent if needed.
    if parent_issue.get("title") != new_title:
        try:
            run(["gh", "issue", "edit", str(parent_number), "--title", new_title])
            print(f"[promote-to-epic] parent #{parent_number} retitled to '{new_title}'")
        except subprocess.CalledProcessError as e:
            print(f"[promote-to-epic] retitle failed: {e.stderr}", file=sys.stderr)

    # Ensure epic label.
    run(["gh", "issue", "edit", str(parent_number), "--add-label", "epic"], check=False)

    # Find sub-items in backlog.
    sub_items = find_backlog_sub_items(epic_nn)
    print(f"[promote-to-epic] found {len(sub_items)} sub-items for {item}")

    # Create sub-issues if missing.
    sub_refs: list[tuple[str, dict]] = []
    for sub in sub_items:
        existing = find_issue_for_item(sub)
        if existing:
            sub_refs.append((sub, existing))
            continue
        sub_args = argparse.Namespace(item=sub)
        cmd_create_issue(sub_args)
        re_lookup = find_issue_for_item(sub)
        if re_lookup:
            sub_refs.append((sub, re_lookup))

    # Update parent body with tasklist.
    new_body = render_epic_body(parent_issue.get("body") or "", item, sub_refs)
    if new_body and new_body != (parent_issue.get("body") or ""):
        try:
            run(["gh", "issue", "edit", str(parent_number), "--body", new_body])
            print(f"[promote-to-epic] parent body updated with {len(sub_refs)} sub-issues")
        except subprocess.CalledProcessError as e:
            print(f"[promote-to-epic] body update failed: {e.stderr}", file=sys.stderr)

    # Branch rename if applicable.
    if args.rename_branch:
        cur = current_branch()
        target = f"feature/epic-{epic_nn.lower()}-{slugify(title)}"
        if cur == target:
            print(f"[promote-to-epic] branch already '{cur}'")
        elif cur not in ("main", "master", "dev", "develop") and not branch_matches_item(cur, item):
            try:
                run(["git", "branch", "-m", cur, target])
                print(f"[promote-to-epic] branch renamed '{cur}' -> '{target}'")
            except subprocess.CalledProcessError as e:
                print(f"[promote-to-epic] branch rename failed: {e.stderr}", file=sys.stderr)

    return 0


def find_backlog_sub_items(epic_nn: str) -> list[str]:
    """Return ordered list of FEAT and IMP IDs that belong to EPIC-NN."""
    bl = backlog_path()
    if not bl.exists():
        return []
    feat_re = re.compile(rf"^\| (FEAT-{epic_nn}-\d{{2}}) ")
    imp_re = re.compile(rf"^\| (IMP-{epic_nn}-\d{{2}}-\d{{2}}) ")
    out: list[str] = []
    for line in bl.read_text(encoding="utf-8").splitlines():
        m = feat_re.match(line) or imp_re.match(line)
        if m:
            out.append(m.group(1))
    return out


def render_epic_body(existing: str, epic_id: str, sub_refs: list[tuple[str, dict]]) -> str:
    """Insert or replace a 'Sub-Issues' section in the parent body."""
    section_header = "## Sub-Issues"
    lines: list[str] = [section_header, ""]
    for sub_id, issue in sub_refs:
        check = "x" if issue.get("state", "OPEN").lower() == "closed" else " "
        title = issue.get("title", sub_id)
        lines.append(f"- [{check}] #{issue['number']} {title}")
    section = "\n".join(lines) + "\n"

    # Replace existing section if present.
    if section_header in existing:
        before, _, rest = existing.partition(section_header)
        # rest may contain the previous list and possibly other content.
        # We replace until the next "## " heading or end of string.
        next_heading = re.search(r"\n## ", rest)
        if next_heading:
            tail = rest[next_heading.start():]
        else:
            tail = ""
        return before + section + tail
    sep = "\n\n" if existing and not existing.endswith("\n\n") else ""
    return existing + sep + section


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "untitled"


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

    p6 = sub.add_parser(
        "sync-status",
        help="Sync backlog Status and Claim with the GitHub issue and project",
    )
    p6.add_argument("--item", required=True)
    p6.set_defaults(func=cmd_sync_status)

    p7 = sub.add_parser(
        "promote-to-epic",
        help="Rename the parent issue, create sub-issues, write tasklist, optionally rename branch",
    )
    p7.add_argument("--item", required=True, help="EPIC-NN")
    p7.add_argument("--parent-issue", type=int, default=None,
                    help="explicit GitHub issue number for the parent")
    p7.add_argument("--rename-branch", action="store_true",
                    help="rename the current feature branch to feature/epic-NN-<slug>")
    p7.set_defaults(func=cmd_promote_to_epic)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
