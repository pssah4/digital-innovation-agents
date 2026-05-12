#!/usr/bin/env python3
"""
DIA team-workflow flow driver.

Orchestrates the GitHub-side artefacts (issue, project card, draft PR,
phase tags) for a backlog item as it walks through the V-Model phases.
The backlog truth lives in `_devprocess/context/BACKLOG.md`; this
script keeps the GitHub view in sync.

Subcommands:
    create-issue        Create a GitHub issue for a backlog item.
    tag-phase           Set the `<item-id>/<phase>-done` annotated git tag.
    sync-status         Mirror BACKLOG Status to issue and project.
    sync-project-status Bulk-sync BACKLOG Status to the project board.
    promote-to-epic     Rename parent, create sub-issues, tasklist.
    preflight           Read-only checks before a GitHub bulk sync.
    initial-sync        Bulk-onboard an existing backlog onto GitHub.
    validate-fix        Hotfix-scoped consistency check.
    open-draft-pr       Open a draft PR for the item branch.
    ready-for-review    Flip the draft PR to ready and tag ready-for-review.
    status              Print state of the item (branch, tags, issue, PR).

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

VALID_PHASES = ("ba", "re", "arch", "code", "test", "sec", "ready-for-review")
# `sec` is the canonical name for the security phase. `audit` is the
# legacy v3 name, kept as a tolerated alias for repos that already
# carry `<id>/audit-done` tags from earlier runs. New tags use `sec`.
PHASE_ALIASES = {"audit": "sec"}
ITEM_RE = re.compile(r"^(EPIC-\d{2}|FEAT-\d{2}-\d{2}|FIX-\d{2}-\d{2}-\d{2}|IMP-\d{2}-\d{2}-\d{2})$")

# Subcommands that require GitHub to be reachable in mode = "github-sync".
# tag-phase and status work locally (only set git tags / read tags), so
# they remain available in git-only mode.
GITHUB_REQUIRED_ACTIONS = (
    "create-issue",
    "open-draft-pr",
    "ready-for-review",
    "sync-status",
    "sync-project-status",
    "promote-to-epic",
    "apply-renumber",
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
        value = _toml_string_fallback("mode", text)
        if value in ("off", "git-only", "github-sync"):
            return value
    return "git-only"


# TOML allows both `key = "value"` (basic) and `key = 'value'` (literal).
# /dia-setup writes double quotes, but the template explicitly invites
# hand edits. The fallback parsers below need to match both shapes.


def _toml_string_fallback(key: str, text: str) -> str | None:
    """Find a top-level `key = "value"` or `key = 'value'` line.

    Lightweight, regex-only, used when tomllib is unavailable
    (Python < 3.11). Returns the captured string or None.
    """
    pattern = re.compile(
        rf'^[ \t]*{re.escape(key)}\s*=\s*(?:"([^"]*)"|\'([^\']*)\')',
        re.MULTILINE,
    )
    match = pattern.search(text)
    if not match:
        return None
    return match.group(1) if match.group(1) is not None else match.group(2)


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
        # Minimal regex scan for systems without tomllib (Python < 3.11).
        # Reads the keys flow.py actually consumes; do not extend this
        # list without also extending the consumers. Accepts both
        # double-quoted and single-quoted TOML strings; project_number
        # is read as an integer literal.
        out: dict = {}
        for key in ("status_field", "project_owner"):
            value = _toml_string_fallback(key, text)
            if value is not None:
                out[key] = value
        m = re.search(
            rf'^[ \t]*project_number\s*=\s*(\d+)',
            text, re.MULTILINE,
        )
        if m:
            out["project_number"] = int(m.group(1))
        return out


def read_source_branch() -> str:
    """Return the project's source / target branch for feature PRs.

    Read from `.dia/config.toml -> source_branch`. Default `develop`,
    matching the team-workflow contract.
    """
    try:
        cfg = repo_root() / ".dia" / "config.toml"
    except subprocess.CalledProcessError:
        return "develop"
    if not cfg.exists():
        return "develop"
    text = cfg.read_text(encoding="utf-8")
    try:
        import tomllib  # type: ignore[import-not-found]

        data = tomllib.loads(text)
        sb = data.get("source_branch", "develop")
        return str(sb) if sb else "develop"
    except ModuleNotFoundError:
        value = _toml_string_fallback("source_branch", text)
        return value if value else "develop"


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


def _strip_id_prefix(title: str, item: str) -> str:
    """Drop a leading `ID:` / `[ID]` / `ID -` prefix from a title.

    Defensive: the BACKLOG Title column must hold the bare title, but
    /reverse-engineering and /dia-migration have been observed writing
    `IMP-01-01-08: ensureColumn...` into it, which flow.py would then
    expand into `IMP-01-01-08: IMP-01-01-08: ensureColumn...` on the
    GitHub issue. Strip one or more such prefixes here as a backstop;
    the writer skills carry the real fix. A bare title that merely
    starts with the id text (no `:` / `-` / `[]` marker) is left alone.
    """
    if not title:
        return title
    esc = re.escape(item)
    patterns = (
        re.compile(rf"^\s*\[\s*{esc}\s*\]\s*[:\-]?\s*"),  # [ID] rest  /  [ID]: rest
        re.compile(rf"^\s*{esc}\s*[:\-]\s*"),              # ID: rest   /  ID - rest
        re.compile(rf"^\s*{esc}\s*$"),                     # ID  (alone)
    )
    cleaned = title
    changed = True
    while changed:
        changed = False
        for p in patterns:
            stripped = p.sub("", cleaned, count=1)
            if stripped != cleaned:
                cleaned, changed = stripped, True
                break
    return cleaned.strip() or item


def title_for_item(item: str) -> str:
    row = find_backlog_row(item)
    if row and len(row["cells"]) > 2:
        return _strip_id_prefix(row["cells"][2], item)
    if item.startswith("EPIC-"):
        bl = backlog_path()
        if bl.exists():
            text = bl.read_text(encoding="utf-8")
            m = re.search(
                rf"^### {re.escape(item)}:\s*(.+?)$",
                text,
                flags=re.MULTILINE,
            )
            if m:
                return _strip_id_prefix(m.group(1).strip(), item)
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


def detail_file_dir(item: str) -> Path | None:
    """Return the requirements/{epics|features|fixes|improvements} dir
    for an item id, or None when the type has no detail file convention.
    """
    base = repo_root() / "_devprocess" / "requirements"
    if item.startswith("EPIC-"):
        return base / "epics"
    if item.startswith("FEAT-"):
        return base / "features"
    if item.startswith("FIX-"):
        return base / "fixes"
    if item.startswith("IMP-"):
        return base / "improvements"
    return None


def find_detail_file(item: str) -> Path | None:
    """Locate the detail file for an item. Slug is unknown, so we glob.

    Convention: `_devprocess/requirements/{type}/{ID}-{slug}.md`.
    Returns the first match (the convention guarantees uniqueness)
    or None if no file exists.
    """
    d = detail_file_dir(item)
    if d is None or not d.exists():
        return None
    for path in sorted(d.glob(f"{item}-*.md")):
        return path
    return None


def read_detail_body(path: Path) -> str:
    """Return the markdown body of a detail file, frontmatter stripped.

    Strips a leading HTML comment block (template instructions) and the
    YAML frontmatter delimited by `---`. Returns the remaining body
    with normalised trailing whitespace.
    """
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^<!--.*?-->\s*", "", text, count=1, flags=re.DOTALL)
    if text.startswith("---"):
        m = re.match(r"^---\n.*?\n---\n", text, flags=re.DOTALL)
        if m:
            text = text[m.end():]
    return text.strip() + "\n"


# ---------- GitHub issue lookup -----------------------------------------

def find_issue_for_item(item: str, include_body: bool = False) -> dict | None:
    """Search open issues whose title starts with the item id.

    When include_body is True, the returned dict carries the issue
    body. Cheaper to skip the body when callers only need number /
    title / url / state.
    """
    if not gh_repo_configured():
        return None
    fields = "number,title,url,state"
    if include_body:
        fields += ",body"
    try:
        out = run([
            "gh", "issue", "list",
            "--search", f"{item} in:title",
            "--state", "all",
            "--json", fields,
            "--limit", "5",
        ]).stdout
    except subprocess.CalledProcessError:
        return None
    issues = json.loads(out)
    for issue in issues:
        if issue["title"].startswith(item) or f"[{item}]" in issue["title"]:
            return issue
    return None


def find_raw_issue_by_title(title: str) -> dict | None:
    """Find a raw issue (still pre-EPIC) by approximate title match.

    Used by promote-to-epic to locate the original intake issue
    before its title was rewritten to `EPIC-NN: {slug}`. We compare
    the BACKLOG title against issue titles after stripping any
    leading `EPIC-NN: ` prefix.
    """
    if not gh_repo_configured():
        return None
    needle = title.strip().lower()
    if not needle:
        return None
    # Use GitHub search on the title text. Fetch a small batch and
    # filter client-side to be robust against ranking differences.
    try:
        out = run([
            "gh", "issue", "list",
            "--search", f"{title} in:title",
            "--state", "all",
            "--json", "number,title,url,state,body",
            "--limit", "10",
        ]).stdout
    except subprocess.CalledProcessError:
        return None
    candidates = json.loads(out)
    for issue in candidates:
        candidate_title = issue.get("title", "")
        normalised = re.sub(r"^EPIC-\d{2}:\s*", "", candidate_title).strip().lower()
        if normalised == needle:
            return issue
    # Loose fallback: substring match, but only when it is unambiguous.
    # A short epic title that merely happens to be a substring of an
    # unrelated issue must not cause that issue to be retitled. Require
    # a minimum needle length and a >= 0.6 length-overlap ratio, and
    # pick the best match rather than the first.
    if len(needle) < 8:
        return None
    best: dict | None = None
    best_ratio = 0.0
    for issue in candidates:
        candidate_title = issue.get("title", "")
        normalised = re.sub(r"^EPIC-\d{2}:\s*", "", candidate_title).strip().lower()
        if not normalised:
            continue
        if needle in normalised or normalised in needle:
            ratio = min(len(needle), len(normalised)) / max(len(needle), len(normalised))
            if ratio > best_ratio:
                best, best_ratio = issue, ratio
    return best if best_ratio >= 0.6 else None


# ---------- GitHub sub-issue linking ------------------------------------

def gh_repo_slug() -> str | None:
    """Return `owner/repo` for the current gh-configured remote."""
    try:
        out = run([
            "gh", "repo", "view", "--json", "nameWithOwner",
        ]).stdout
        data = json.loads(out)
        return data.get("nameWithOwner")
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return None


def issue_database_id(issue_number: int) -> int | None:
    """Resolve issue number -> issue database id (REST `id` field).

    GitHub's sub_issues endpoint requires the database id, not the
    issue number, so we fetch it via the REST API.
    """
    slug = gh_repo_slug()
    if not slug:
        return None
    try:
        out = run([
            "gh", "api", f"repos/{slug}/issues/{issue_number}",
            "--jq", ".id",
        ]).stdout.strip()
        return int(out) if out else None
    except (subprocess.CalledProcessError, ValueError):
        return None


def link_sub_issue(parent_number: int, child_number: int) -> bool:
    """Attach `child_number` as a GitHub sub-issue of `parent_number`.

    Idempotent: if the relation already exists, returns True. Returns
    False on unrecoverable errors (and prints to stderr).
    """
    slug = gh_repo_slug()
    child_id = issue_database_id(child_number)
    if not slug or child_id is None:
        return False
    try:
        run([
            "gh", "api", "-X", "POST",
            f"repos/{slug}/issues/{parent_number}/sub_issues",
            "-F", f"sub_issue_id={child_id}",
        ])
        return True
    except subprocess.CalledProcessError as e:
        stderr = (e.stderr or "").lower()
        if "already" in stderr or "sub-issue" in stderr:
            return True
        print(
            f"[link-sub-issue] failed: parent #{parent_number}, "
            f"child #{child_number}: {e.stderr}",
            file=sys.stderr,
        )
        return False


# ---------- Subcommand: create-issue ------------------------------------

def _issue_number_from_url(url: str) -> int | None:
    """Parse the trailing issue number out of a GitHub issue URL."""
    m = re.search(r"/issues/(\d+)\b", url or "")
    return int(m.group(1)) if m else None


def create_issue_for_item(item: str) -> dict | None:
    """Create the GitHub issue for `item`; return a minimal issue dict.

    Returns {"number", "url", "title", "state"} on success, None on
    failure. The caller must have checked that no issue exists yet.

    Returning the freshly created issue lets callers (promote-to-epic,
    initial-sync) skip a re-lookup via `gh issue list --search`, whose
    index lags creation by a few seconds -- the cause of partial
    sub-issue linking on a first bulk run.
    """
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
        return None
    print(f"[create-issue] created: {out}")
    write_issue_into_backlog(item, out)
    add_issue_to_project(out)
    number = _issue_number_from_url(out)
    if number is None:
        # URL did not parse; callers can still re-lookup by id later.
        return None
    return {"number": number, "url": out, "title": title, "state": "OPEN"}


def cmd_create_issue(args: argparse.Namespace) -> int:
    item = normalize_item(args.item)

    if not mode_active_or_skip("create-issue"):
        return 0
    if not gh_repo_configured():
        print(f"[create-issue] gh CLI / GitHub remote not configured -- skipping (local-only mode)")
        return 0

    update_body = bool(getattr(args, "update_body", False))

    existing = find_issue_for_item(item)
    if existing:
        if not update_body:
            print(f"[create-issue] issue exists: {existing['url']}")
            return 0
        try:
            run([
                "gh", "issue", "edit", str(existing["number"]),
                "--body", build_issue_body(item),
            ])
            print(f"[create-issue] body updated: {existing['url']}")
        except subprocess.CalledProcessError as e:
            print(f"[create-issue] body update failed: {e.stderr}", file=sys.stderr)
            return 1
        # Retro-sync: pre-existing issues frequently never made it onto
        # the project board. add_issue_to_project is idempotent.
        add_issue_to_project(existing["url"])
        return 0

    return 0 if create_issue_for_item(item) else 1


def add_issue_to_project(issue_url: str) -> None:
    """Add the freshly created issue to the configured GitHub Project.

    Reads `[github] project_number` from .dia/config.toml. If absent,
    silently does nothing. Idempotent: a second add is a no-op on
    GitHub's side.
    """
    cfg = read_dia_github_config()
    project_number = cfg.get("project_number")
    if not project_number:
        return
    try:
        repo_owner = json.loads(run([
            "gh", "repo", "view", "--json", "owner",
        ]).stdout)["owner"]["login"]
    except (subprocess.CalledProcessError, KeyError, json.JSONDecodeError):
        return
    try:
        run([
            "gh", "project", "item-add", str(project_number),
            "--owner", repo_owner, "--url", issue_url,
        ], check=False)
        print(f"[create-issue] added to project {project_number}")
        # The per-run item-list cache no longer reflects the board.
        try:
            _invalidate_project_item_cache(int(project_number))
        except (TypeError, ValueError):
            _invalidate_project_item_cache()
    except subprocess.CalledProcessError:
        pass


BACKLOG_POINTER = (
    "> Source of truth: "
    "[`_devprocess/context/BACKLOG.md`](_devprocess/context/BACKLOG.md) "
    "-- status, phase, claim live there.\n"
)


# Markers that flag a detail file as a still-unfilled reverse-engineering
# / pre-BA skeleton. Pushing such a body to GitHub looks like a broken
# epic, so build_issue_body substitutes a short, honest stub instead and
# the next sync (after /business-analysis filled the file) replaces it.
_SKELETON_MARKERS = (
    "[needs user input",
    "[needs input]",
    "> **status**: anticipated",
    "anticipated (not yet validated)",
    "needs-validation: true",
    "**note**: skelett",
    "kommt aus /business-analysis",
    "kommen aus /business-analysis",
    "/business-analysis will fill this in",
    "awaiting validation in /business-analysis",
)


def _looks_like_skeleton(body: str) -> bool:
    """True if the detail body still carries unfilled-skeleton markers."""
    low = (body or "").lower()
    return any(marker in low for marker in _SKELETON_MARKERS)


def _skeleton_stub_body(item: str) -> str:
    kind = type_label(item)
    title = title_for_item(item)
    return (
        f"# {item}: {title}\n\n"
        f"> The {kind} detail file under `_devprocess/requirements/` is "
        f"still a reverse-engineering skeleton. Run `/business-analysis` "
        f"(then `/requirements-engineering`) to fill in the real scope, "
        f"hypothesis, and success criteria. The next `create-issue` / "
        f"`promote-to-epic` run pushes the completed content here.\n"
    )


def build_issue_body(item: str) -> str:
    """Build the GitHub issue body for a backlog item.

    The body mirrors the artefact's detail file under
    `_devprocess/requirements/`. Status, phase, priority are NOT
    duplicated -- they live in the BACKLOG row and on GitHub via labels
    and the project board. When no detail file exists yet (typical
    during retro-sync of legacy projects), or when the detail file is
    still a reverse-engineering skeleton, the body degrades to a short
    stub.
    """
    detail = find_detail_file(item)
    if detail is not None:
        body = read_detail_body(detail)
        if _looks_like_skeleton(body):
            return BACKLOG_POINTER + "\n" + _skeleton_stub_body(item)
        return BACKLOG_POINTER + "\n" + body
    title = title_for_item(item)
    return (
        BACKLOG_POINTER
        + f"\n# {item}: {title}\n\n"
        + "_No detail file under `_devprocess/requirements/` yet._\n"
    )


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
    "sec": "Security audit complete: report written, findings filed.",
    "ready-for-review": "All required phases complete; PR ready for review.",
}


def cmd_tag_phase(args: argparse.Namespace) -> int:
    item = normalize_item(args.item)
    phase = args.phase
    if phase in PHASE_ALIASES:
        canonical = PHASE_ALIASES[phase]
        print(f"[tag-phase] phase '{phase}' is deprecated; using '{canonical}'")
        phase = canonical
    if phase not in VALID_PHASES:
        sys.exit(f"ERROR: invalid phase '{phase}'. Valid: {', '.join(VALID_PHASES)}")
    # tag-phase always sets the local git tag; only the GitHub-side
    # update is mode-gated below in update_issue_after_tag.
    if read_dia_mode() == "off":
        print("[tag-phase] mode=off, skipping (run /dia-setup to change)")
        return 0
    cur = current_branch()
    if not branch_matches_item(cur, item) and cur not in ("main", "master", "dev", "develop"):
        print(f"[tag-phase] WARNING: current branch '{cur}' does not match item '{item}'.")
    # Phase-end tags carry the "-done" suffix to mark a completed phase.
    # ready-for-review is not a phase but a release-readiness marker, so
    # it lives at <id>/ready-for-review without the suffix per the
    # team-workflow contract.
    if phase == "ready-for-review":
        tag_name = f"{item.lower()}/ready-for-review"
    else:
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
    # Update phase label. The full label set includes the initial
    # "phase:planned" label set by create-issue, so it lands here
    # too and gets removed when any real phase tag is set.
    label_map = {
        "ba": "phase:ba",
        "re": "phase:re",
        "arch": "phase:arch",
        "code": "phase:coding",
        "test": "phase:testing",
        "sec": "phase:sec",
        "ready-for-review": "phase:review",
    }
    all_phase_labels = set(label_map.values()) | {"phase:planned"}
    new_label = label_map.get(phase)
    if new_label:
        for lbl in all_phase_labels:
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
        "sec": r"- \[ \] Security-Audit",
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
            "--base", read_source_branch(),
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
    if args.with_sec:
        required = required + ("sec-done",)
    missing = []
    for r in required:
        tag = f"{item.lower()}/{r}"
        out = run(["git", "tag", "--list", tag]).stdout.strip()
        if not out:
            # Backwards compat: accept legacy `audit-done` for `sec-done`.
            if r == "sec-done":
                legacy = f"{item.lower()}/audit-done"
                if run(["git", "tag", "--list", legacy]).stdout.strip():
                    continue
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
        # Preserve leading and trailing space style by minimal
        # substitution. For an empty claim, leave a single space so
        # the column structure stays a valid Markdown table.
        cells[10] = f" {claim} " if claim else " "
        new_line = "|".join(cells) + ("\n" if raw_line.endswith("\n") else "")
        new_lines.append(new_line)
        changed = True
    if changed:
        bl.write_text("".join(new_lines), encoding="utf-8")
    return changed


# Per-run caches for GitHub Project metadata. field-list and item-list
# do not depend on the issue under sync, so caching them within one
# process is the difference between O(items) and O(1) GraphQL scans
# during a bulk onboarding -- promote-to-epic touches every sub-item of
# an epic in one run, and initial-sync touches the whole backlog.
_PROJECT_FIELD_CACHE: dict[int, tuple[list, str]] = {}
_PROJECT_ITEM_CACHE: dict[int, list] = {}


def _invalidate_project_item_cache(project_number: int | None = None) -> None:
    """Drop the cached project item-list.

    Call after the board membership changed (item-add). Without an
    argument, clears every cached project.
    """
    if project_number is None:
        _PROJECT_ITEM_CACHE.clear()
    else:
        _PROJECT_ITEM_CACHE.pop(project_number, None)


def _project_fields(project_number: int, project_owner: str) -> list | None:
    """Return the project's fields (cached per run), or None on failure."""
    cached = _PROJECT_FIELD_CACHE.get(project_number)
    if cached:
        return cached[0]
    try:
        out = run([
            "gh", "project", "field-list", str(project_number),
            "--owner", project_owner, "--format", "json", "--limit", "200",
        ]).stdout
    except subprocess.CalledProcessError:
        return None
    fields = json.loads(out).get("fields", [])
    _PROJECT_FIELD_CACHE[project_number] = (fields, project_owner)
    return fields


def _project_items(project_number: int, project_owner: str) -> list | None:
    """Return the project's items (cached per run), or None on failure.

    One `gh project item-list --limit 1000` per project per run. The
    cache is invalidated by _invalidate_project_item_cache whenever an
    issue is added to the board.
    """
    cached = _PROJECT_ITEM_CACHE.get(project_number)
    if cached is not None:
        return cached
    try:
        items = json.loads(run([
            "gh", "project", "item-list", str(project_number),
            "--owner", project_owner, "--format", "json", "--limit", "1000",
        ]).stdout).get("items", [])
    except subprocess.CalledProcessError:
        return None
    _PROJECT_ITEM_CACHE[project_number] = items
    return items


def _resolve_project_owner(cfg: dict) -> str | None:
    """Resolve the GitHub login that owns the configured project.

    Priority: explicit cfg.project_owner > repo owner login.
    """
    explicit = cfg.get("project_owner")
    if explicit:
        return str(explicit)
    try:
        return json.loads(run([
            "gh", "repo", "view", "--json", "owner",
        ]).stdout)["owner"]["login"]
    except (subprocess.CalledProcessError, KeyError, json.JSONDecodeError):
        return None


# Reasons update_project_status_field can decline to touch the board.
# Each is reported verbatim so a failed sync is never silently
# misattributed to "not configured".
_PROJECT_SKIP_REASONS = {
    "not_configured": "no [github] project_number in .dia/config.toml",
    "bad_project_number": "project_number in .dia/config.toml is not an integer",
    "owner_unresolved": "could not resolve the project owner login",
    "field_list_failed": "gh project field-list failed (auth scope? rate limit?)",
    "field_missing": "the configured Status field does not exist on the project",
    "option_missing": "the project Status field has no matching option for this status",
    "item_list_failed": "gh project item-list failed (auth scope? rate limit?)",
    "issue_not_in_project": "the issue is not a card on the project board",
    "item_ids_missing": "could not resolve the project item / project id",
    "item_edit_failed": "gh project item-edit failed",
}


def update_project_status_field(
    issue_number: int, github_status: str,
) -> tuple[bool, str | None]:
    """Update the Status field on the configured GitHub Project.

    Requires `[github] project_number = N` (and ideally
    status_field = "Status") in .dia/config.toml. The field name and
    option name are matched case-insensitively so a backlog value like
    "In Progress" maps onto GitHub's built-in "In progress" option.

    Returns (True, None) on success, (False, reason) otherwise, where
    reason is a key of _PROJECT_SKIP_REASONS. Callers turn the reason
    into a single accurate log line.
    """
    cfg = read_dia_github_config()
    project_number = cfg.get("project_number")
    if not project_number:
        return False, "not_configured"
    try:
        project_number = int(project_number)
    except (TypeError, ValueError):
        return False, "bad_project_number"
    field_name = cfg.get("status_field", "Status")
    project_owner = _resolve_project_owner(cfg)
    if not project_owner:
        return False, "owner_unresolved"

    fields = _project_fields(project_number, project_owner)
    if fields is None:
        return False, "field_list_failed"
    target_field = next(
        (f for f in fields
         if str(f.get("name", "")).strip().casefold()
         == field_name.strip().casefold()),
        None,
    )
    if not target_field:
        return False, "field_missing"
    option_id = next(
        (o["id"] for o in target_field.get("options", [])
         if str(o.get("name", "")).strip().casefold()
         == github_status.strip().casefold()),
        None,
    )
    if not option_id:
        return False, "option_missing"

    items = _project_items(project_number, project_owner)
    if items is None:
        return False, "item_list_failed"
    matching = next(
        (i for i in items if i.get("content", {}).get("number") == issue_number),
        None,
    )
    if not matching:
        return False, "issue_not_in_project"
    item_id = matching.get("id")
    project_id = matching.get("projectId") or target_field.get("projectId")
    if not (item_id and project_id):
        return False, "item_ids_missing"
    try:
        run([
            "gh", "project", "item-edit",
            "--project-id", project_id,
            "--id", item_id,
            "--field-id", target_field["id"],
            "--single-select-option-id", option_id,
        ])
        return True, None
    except subprocess.CalledProcessError as e:
        print(f"[sync-status] item-edit failed: {e.stderr}", file=sys.stderr)
        return False, "item_edit_failed"


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

    # Project field, if configured. One accurate log line: either the
    # field was set, or the precise reason it was skipped (so a
    # rate-limited or mis-scoped run is never reported as
    # "not configured").
    ok, reason = update_project_status_field(issue_number, github_status)
    if ok:
        print(f"[sync-status] project field set to '{github_status}'")
    elif reason == "not_configured":
        print("[sync-status] project field not configured; mirrored only via issue state")
    else:
        detail = _PROJECT_SKIP_REASONS.get(reason or "", reason or "unknown")
        print(f"[sync-status] project field skipped: reason={reason} ({detail})")

    # Claim from assignee back to backlog. Three cases:
    #   1. Item is Done -> always clear the Claim (work is finished).
    #   2. No assignee on GitHub -> clear the Claim (item is unowned).
    #   3. Assignee present -> mirror to Claim with today's date.
    assignee = github_issue_assignee(issue_number)
    if backlog_status == "Done" or not assignee:
        if write_claim_into_backlog(item, ""):
            reason = "status=Done" if backlog_status == "Done" else "no assignee"
            print(f"[sync-status] claim cleared in backlog ({reason})")
    else:
        from datetime import date
        claim = f"{assignee} @ {date.today().isoformat()}"
        if write_claim_into_backlog(item, claim):
            print(f"[sync-status] claim updated in backlog: {claim}")
    return 0


# ---------- Subcommand: promote-to-epic ---------------------------------

def _resolve_parent_epic_issue(item: str, title: str, parent_issue_arg: int | None) -> dict | None:
    """Locate the GitHub issue that becomes the epic parent."""
    if parent_issue_arg:
        try:
            out = run([
                "gh", "issue", "view", str(parent_issue_arg),
                "--json", "number,title,url,state,body",
            ]).stdout
            return json.loads(out)
        except subprocess.CalledProcessError as e:
            print(f"[promote-to-epic] parent-issue lookup failed: {e.stderr}", file=sys.stderr)
            return None
    parent = find_issue_for_item(item, include_body=True)
    if parent:
        return parent
    # Raw-Issue case: the parent issue still has the original raw title
    # (no EPIC-NN prefix). Try to match by the BACKLOG title instead.
    return find_raw_issue_by_title(title)


def _promote_to_epic_dry_run(item: str, parent_issue_arg: int | None) -> int:
    """Print what `promote-to-epic` would do, without any API mutation.

    Uses only read-only lookups. Handy before a bulk onboarding so the
    operator sees the blast radius first.
    """
    title = title_for_item(item)
    print(f"[promote-to-epic --dry-run] EPIC {item}: {title}")
    parent = _resolve_parent_epic_issue(item, title, parent_issue_arg)
    if parent:
        cur_title = parent.get("title", "")
        new_title = f"{item}: {title}"
        if cur_title != new_title:
            print(f"  parent issue #{parent['number']}: retitle '{cur_title}' -> '{new_title}'")
        else:
            print(f"  parent issue #{parent['number']}: title already '{new_title}'")
    else:
        print("  parent issue: NOT FOUND -- would fail (pass --parent-issue <NN>)")
    detail = find_detail_file(item)
    if detail is not None and _looks_like_skeleton(read_detail_body(detail)):
        print("  epic body: detail file is still a skeleton -> would push a stub body")
    elif detail is not None:
        print(f"  epic body: would refresh from {detail.relative_to(repo_root())}")
    else:
        print("  epic body: no detail file -> would push a backlog-pointer stub")
    epic_nn = item.split("-", 1)[1]
    subs = find_backlog_sub_items(epic_nn)
    print(f"  {len(subs)} sub-item(s) in BACKLOG: {', '.join(subs) or '(none)'}")
    to_create = to_relink = 0
    for sub in subs:
        ex = find_issue_for_item(sub)
        if ex:
            print(f"    {sub}: issue #{ex['number']} exists -> would (re)link + refresh body")
            to_relink += 1
        else:
            print(f"    {sub}: no issue -> would create + link")
            to_create += 1
    print(f"  summary: create {to_create}, relink {to_relink}, "
          f"status-sync {len(subs) + 1} item(s)")
    return 0


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

    if bool(getattr(args, "dry_run", False)):
        return _promote_to_epic_dry_run(item, args.parent_issue)

    epic_nn = item.split("-", 1)[1]  # "01"
    title = title_for_item(item)
    new_title = f"{item}: {title}"

    parent_issue = _resolve_parent_epic_issue(item, title, args.parent_issue)
    if not parent_issue:
        print(
            f"[promote-to-epic] no parent issue found for {item}.\n"
            f"  Tried EPIC-id title prefix and BACKLOG title match.\n"
            f"  Pass --parent-issue <NN> to point at the raw issue."
        )
        return 1
    parent_number = int(parent_issue["number"])
    # The epic body and sub-issue bodies are mirrored from the detail
    # files by default -- the detail file is the source of truth and
    # mirroring is the whole point. --no-sync-bodies opts out.
    sync_bodies = bool(getattr(args, "sync_bodies", True))

    # Rename parent if needed.
    if parent_issue.get("title") != new_title:
        try:
            run(["gh", "issue", "edit", str(parent_number), "--title", new_title])
            print(f"[promote-to-epic] parent #{parent_number} retitled to '{new_title}'")
        except subprocess.CalledProcessError as e:
            print(f"[promote-to-epic] retitle failed: {e.stderr}", file=sys.stderr)

    # Ensure epic label.
    run(["gh", "issue", "edit", str(parent_number), "--add-label", "epic"], check=False)

    # Make sure the parent epic itself lands on the GitHub Project. The
    # board-add for sub-items happens through create_issue_for_item
    # below; the parent was previously the only thing that got renamed
    # in place without ever being added to the project.
    if parent_issue.get("url"):
        add_issue_to_project(parent_issue["url"])

    # Refresh the epic body from the detail file. build_issue_body
    # already swaps a still-skeleton detail file for a short stub; warn
    # so the operator knows /business-analysis still owes content.
    if sync_bodies:
        detail = find_detail_file(item)
        if detail is not None and _looks_like_skeleton(read_detail_body(detail)):
            print(f"[promote-to-epic] note: {item} detail file is still a "
                  f"reverse-engineering skeleton; pushing a stub body. "
                  f"Run /business-analysis to fill it in.")
        epic_body = build_issue_body(item)
        try:
            run(["gh", "issue", "edit", str(parent_number),
                 "--body", epic_body])
            print(f"[promote-to-epic] epic body refreshed from detail file")
            parent_issue["body"] = epic_body
        except subprocess.CalledProcessError as e:
            print(f"[promote-to-epic] epic body refresh failed: {e.stderr}",
                  file=sys.stderr)

    # Find sub-items in backlog.
    sub_items = find_backlog_sub_items(epic_nn)
    print(f"[promote-to-epic] found {len(sub_items)} sub-items for {item}")

    # Create sub-issues if missing; refresh existing ones when
    # sync_bodies is set. Use the create-time return value rather than
    # a re-lookup so a lagging search index never drops a fresh issue.
    sub_refs: list[tuple[str, dict]] = []
    for sub in sub_items:
        existing = find_issue_for_item(sub)
        if existing:
            sub_refs.append((sub, existing))
            if sync_bodies:
                cmd_create_issue(argparse.Namespace(
                    item=sub, update_body=True,
                ))
            continue
        created = create_issue_for_item(sub) or find_issue_for_item(sub)
        if created:
            sub_refs.append((sub, created))
        else:
            print(f"[promote-to-epic] WARNING: could not create or locate "
                  f"issue for {sub}; it will be missing from the tasklist",
                  file=sys.stderr)

    # Establish the real GitHub parent-child relation. Idempotent:
    # re-linking an already-linked sub-issue is a no-op.
    for sub_id, issue in sub_refs:
        if link_sub_issue(parent_number, int(issue["number"])):
            print(f"[promote-to-epic] linked {sub_id} (#{issue['number']}) "
                  f"as sub-issue of #{parent_number}")

    # Update parent body: refresh the Sub-Issues marker block. Content
    # outside the markers (the epic description) is preserved verbatim.
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

    # Mirror BACKLOG Status to the project board for the epic and every
    # sub-item we just touched. The per-run item-list cache keeps this
    # to one project scan instead of one per item.
    cmd_sync_status(argparse.Namespace(item=item))
    for sub_id, _ in sub_refs:
        cmd_sync_status(argparse.Namespace(item=sub_id))

    return 0


def find_backlog_sub_items(epic_nn: str) -> list[str]:
    """Return ordered list of FEAT, FIX, and IMP IDs that belong to EPIC-NN."""
    bl = backlog_path()
    if not bl.exists():
        return []
    feat_re = re.compile(rf"^\| (FEAT-{epic_nn}-\d{{2}}) ")
    fix_re = re.compile(rf"^\| (FIX-{epic_nn}-\d{{2}}-\d{{2}}) ")
    imp_re = re.compile(rf"^\| (IMP-{epic_nn}-\d{{2}}-\d{{2}}) ")
    out: list[str] = []
    for line in bl.read_text(encoding="utf-8").splitlines():
        m = feat_re.match(line) or fix_re.match(line) or imp_re.match(line)
        if m:
            out.append(m.group(1))
    return out


_SUBISSUES_BEGIN = "<!-- DIA:sub-issues -->"
_SUBISSUES_END = "<!-- /DIA:sub-issues -->"


def _join_body_parts(*parts: str) -> str:
    """Join non-empty body fragments with a blank line, trailing newline."""
    kept = [p.strip("\n") for p in parts if p and p.strip("\n")]
    return "\n\n".join(kept) + "\n" if kept else ""


def render_epic_body(existing: str, epic_id: str, sub_refs: list[tuple[str, dict]]) -> str:
    """Return the epic body with an up-to-date Sub-Issues tasklist.

    The tasklist lives inside `<!-- DIA:sub-issues -->` /
    `<!-- /DIA:sub-issues -->` markers appended to the end of the body.
    Everything outside the markers (the epic description from the detail
    file) is preserved verbatim, so a re-run can never overwrite it --
    the failure mode where a second `promote-to-epic` left only the
    tasklist behind.

    Migration: an older body with a bare `## Sub-Issues` section (no
    markers) has that section replaced by the marker block.
    """
    lines: list[str] = ["## Sub-Issues", ""]
    for sub_id, issue in sub_refs:
        check = "x" if str(issue.get("state", "OPEN")).lower() == "closed" else " "
        title = issue.get("title", sub_id)
        lines.append(f"- [{check}] #{issue['number']} {title}")
    block = _SUBISSUES_BEGIN + "\n" + "\n".join(lines) + "\n" + _SUBISSUES_END
    body = existing or ""

    # 1. Marker block already present -> replace it in place, keep the
    #    surrounding description untouched.
    if _SUBISSUES_BEGIN in body and _SUBISSUES_END in body:
        head, _, rest = body.partition(_SUBISSUES_BEGIN)
        _, _, tail = rest.partition(_SUBISSUES_END)
        return _join_body_parts(head, block, tail)

    # 2. Legacy bare "## Sub-Issues" section -> replace it with the
    #    marker block (one-time migration). Keep any heading section
    #    that follows it.
    legacy_header = "## Sub-Issues"
    if legacy_header in body:
        before, _, rest = body.partition(legacy_header)
        next_heading = re.search(r"\n#{1,6} ", rest)
        tail = rest[next_heading.start():] if next_heading else ""
        return _join_body_parts(before, block, tail)

    # 3. No tasklist yet -> append the marker block to the body.
    return _join_body_parts(body, block)


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "untitled"


# ---------- Subcommand: apply-renumber ----------------------------------

def cmd_apply_renumber(args: argparse.Namespace) -> int:
    """Apply a renumber plan to GitHub issue titles and parent bodies.

    Reads the JSON plan written by `tools/renumber-for-merge.py
    --plan-out FILE`, then performs two passes:

      1. **Body sync.** For every Epic that owns at least one
         renamed sub-item (FEAT, IMP, FIX) or that was itself
         renamed, fetch the parent issue body, rewrite every
         old id occurrence (with word boundaries) to the new id,
         and save the body. This catches the Sub-Issues tasklist
         and any other id mention.
      2. **Title sync.** For every (old_id -> new_id) pair in the
         plan (epics, feats, imps, fixes), rename the matching
         GitHub issue title from "OLD-NN: slug" to "NEW-NN: slug".

    Body sync runs first because find_issue_for_item resolves by
    the title prefix; the alt id is the title we still see at that
    point. After the title sync, the new id becomes the lookup key.

    Idempotent. Mode-aware (no-op outside `github-sync`).
    """
    if not mode_active_or_skip("apply-renumber"):
        return 0
    if not gh_repo_configured():
        print("[apply-renumber] gh CLI / GitHub remote not configured -- skipping")
        return 0
    plan_path = Path(args.plan)
    if not plan_path.exists():
        print(f"[apply-renumber] plan file not found: {plan_path}", file=sys.stderr)
        return 1
    try:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[apply-renumber] plan file is not valid JSON: {e}", file=sys.stderr)
        return 1
    mapping = plan.get("mapping", {})
    pairs: list[tuple[str, str]] = []
    epic_map: dict[str, str] = {}
    sub_maps: dict[str, dict[str, str]] = {}
    for category in ("epics", "feats", "imps", "fixes"):
        cat_map = mapping.get(category, {})
        if isinstance(cat_map, dict):
            for old, new in cat_map.items():
                pairs.append((old, new))
            if category == "epics":
                epic_map = cat_map
            else:
                sub_maps[category] = cat_map
    if not pairs:
        print("[apply-renumber] mapping is empty, nothing to do")
        return 0

    # Validate every id pair against the canonical ITEM_RE before any
    # gh issue edit fires. A hand-edited or tampered plan file could
    # otherwise pass arbitrary strings as GitHub issue titles. ITEM_RE
    # accepts only EPIC-NN, FEAT-EE-FF, IMP-EE-FF-NN, FIX-EE-FF-NN.
    invalid: list[tuple[str, str]] = [
        (old, new) for old, new in pairs
        if not (ITEM_RE.match(old) and ITEM_RE.match(new))
    ]
    if invalid:
        print(
            "[apply-renumber] plan rejects invalid id pairs:",
            file=sys.stderr,
        )
        for old, new in invalid:
            print(f"  {old} -> {new}", file=sys.stderr)
        return 2

    # Build a flat old->new lookup for body substitution.
    flat_map: dict[str, str] = {}
    for category in ("epics", "feats", "imps", "fixes"):
        cat_map = mapping.get(category, {})
        if isinstance(cat_map, dict):
            flat_map.update(cat_map)

    changes: list[dict] = []

    # ----- Pass 1: body sync for affected epics ----------------------
    affected_epics = collect_affected_epics(epic_map, sub_maps)
    for old_epic_id in affected_epics:
        epic_issue = find_issue_for_item(old_epic_id, include_body=True)
        if not epic_issue:
            changes.append({"epic": old_epic_id, "status": "no-issue"})
            continue
        old_body = epic_issue.get("body") or ""
        new_body = rewrite_ids_in_text(old_body, flat_map)
        if new_body == old_body:
            changes.append({"epic": old_epic_id, "issue": epic_issue["number"], "status": "body-unchanged"})
            continue
        try:
            run([
                "gh", "issue", "edit", str(epic_issue["number"]),
                "--body", new_body,
            ])
            changes.append({
                "epic": old_epic_id,
                "issue": epic_issue["number"],
                "status": "body-rewritten",
            })
        except subprocess.CalledProcessError as e:
            changes.append({
                "epic": old_epic_id,
                "issue": epic_issue["number"],
                "status": f"body-failed: {e.stderr}",
            })

    # ----- Pass 2: title sync ----------------------------------------
    for old, new in pairs:
        issue = find_issue_for_item(old)
        if not issue:
            changes.append({"old": old, "new": new, "status": "no-issue"})
            continue
        old_title = issue.get("title", "")
        # Preserve the slug after the colon: "OLD-NN: slug" -> "NEW-NN: slug"
        suffix = ""
        if ": " in old_title:
            suffix = old_title.split(": ", 1)[1]
        new_title = f"{new}: {suffix}" if suffix else new
        if old_title == new_title:
            changes.append({"old": old, "new": new, "status": "unchanged"})
            continue
        try:
            run([
                "gh", "issue", "edit", str(issue["number"]),
                "--title", new_title,
            ])
            changes.append({
                "old": old, "new": new,
                "issue": issue["number"],
                "status": "renamed",
            })
        except subprocess.CalledProcessError as e:
            changes.append({
                "old": old, "new": new,
                "issue": issue["number"],
                "status": f"failed: {e.stderr}",
            })
    print(json.dumps({"plan": str(plan_path), "changes": changes}, indent=2))
    failed = any("failed" in c["status"] for c in changes)
    return 1 if failed else 0


def collect_affected_epics(
    epic_map: dict[str, str],
    sub_maps: dict[str, dict[str, str]],
) -> list[str]:
    """Return the OLD epic ids that need a body rewrite.

    An epic is "affected" if its own id was renamed (in epic_map),
    or if any of its sub-items (feats, imps, fixes) was renamed.
    The OLD epic id is what we look up on GitHub, because the title
    has not been rewritten yet at that point.
    """
    epic_old_ids: set[str] = set()
    for old_epic in epic_map.keys():
        epic_old_ids.add(old_epic)
    # If a sub-item was renamed but the epic itself was not, the
    # epic prefix in the OLD id matches what is still on GitHub.
    # Example: FEAT-05-01 -> FEAT-05-02 means EPIC-05 still owns it.
    for cat_map in sub_maps.values():
        for old_sub in cat_map.keys():
            parts = old_sub.split("-")
            # FEAT-EE-FF or IMP-EE-FF-NN or FIX-EE-FF-NN
            if len(parts) >= 2 and parts[1].isdigit():
                epic_old_ids.add(f"EPIC-{parts[1]}")
    # Stable order for deterministic output / tests
    return sorted(epic_old_ids)


def rewrite_ids_in_text(text: str, mapping: dict[str, str]) -> str:
    """Replace old artefact ids with new ones using word boundaries.

    Sorts keys by descending length so longer ids (e.g. FIX-EE-FF-NN)
    are substituted before any contained shorter id (e.g. FEAT-EE-FF
    that overlaps with the prefix). The boundary check ensures we do
    not match an id that is a prefix of a longer id.
    """
    if not mapping or not text:
        return text
    # Sort by descending length to avoid prefix overlap.
    keys = sorted(mapping.keys(), key=len, reverse=True)
    pattern = re.compile(
        r"(?<![A-Za-z0-9-])(" + "|".join(re.escape(k) for k in keys) + r")(?![0-9-])"
    )

    def replace(match: re.Match) -> str:
        return mapping[match.group(1)]

    return pattern.sub(replace, text)


# ---------- Subcommand: sync-project-status -----------------------------

def list_all_backlog_items() -> list[str]:
    """Return every actionable backlog item id (EPIC, FEAT, IMP, FIX) in
    document order. Epic ids picked up from both the `### EPIC-NN:`
    headings and any table rows that name them.
    """
    bl = backlog_path()
    if not bl.exists():
        return []
    text = bl.read_text(encoding="utf-8")
    out: list[str] = []
    seen: set[str] = set()
    row_re = re.compile(r"^\|\s*((?:EPIC|FEAT|FIX|IMP)-\d{2}(?:-\d{2}){0,2})\s*\|")
    head_re = re.compile(r"^###\s+(EPIC-\d{2})", re.MULTILINE)
    for line in text.splitlines():
        m = row_re.match(line)
        if m and m.group(1) not in seen:
            seen.add(m.group(1))
            out.append(m.group(1))
    for m in head_re.finditer(text):
        if m.group(1) not in seen:
            seen.add(m.group(1))
            out.append(m.group(1))
    return out


def cmd_sync_project_status(args: argparse.Namespace) -> int:
    """Bulk-mirror BACKLOG Status onto the GitHub Project status field.

    Three scope modes (mutually exclusive):
      --item ID    sync exactly one backlog item.
      --epic ID    sync the epic and every FEAT/IMP/FIX it owns.
      --all        sync every actionable backlog item (EPIC/FEAT/IMP/FIX).

    Each item is run through cmd_sync_status, which already covers the
    GitHub status field, the issue open/close state, and the Claim
    column. This subcommand exists so users can backfill an existing
    project board after promote-to-epic ran without status sync.
    """
    if not mode_active_or_skip("sync-status"):
        return 0
    if not gh_repo_configured():
        print("[sync-project-status] gh CLI / GitHub remote not configured -- skipping")
        return 0

    items: list[str] = []
    if args.item:
        items.append(normalize_item(args.item))
    elif args.epic:
        epic = normalize_item(args.epic)
        if not epic.startswith("EPIC-"):
            print(f"[sync-project-status] --epic must be EPIC-NN, got {epic}", file=sys.stderr)
            return 1
        items.append(epic)
        epic_nn = epic.split("-", 1)[1]
        items.extend(find_backlog_sub_items(epic_nn))
    elif args.all:
        items = list_all_backlog_items()
    else:
        print("[sync-project-status] one of --item, --epic, --all is required", file=sys.stderr)
        return 1

    if not items:
        print("[sync-project-status] no items to sync")
        return 0

    print(f"[sync-project-status] syncing {len(items)} item(s)")
    failed = 0
    for item in items:
        rc = cmd_sync_status(argparse.Namespace(item=item))
        if rc != 0:
            failed += 1
    ok = len(items) - failed
    print(f"[sync-project-status] done: {ok} synced, {failed} failed")
    return 0 if failed == 0 else 1


# ---------- Subcommand: validate-fix ------------------------------------

FIX_ID_RE = re.compile(r"^FIX-\d{2}-\d{2}-\d{2}$")


def cmd_validate_fix(args: argparse.Namespace) -> int:
    """Hotfix-scoped consistency check for a FIX row.

    Hotfixes skip the V-Model phases, so /consistency-check mode A
    has no natural trigger for them. validate-fix performs the
    minimum set of checks that the standard flow would have done:
      - the FIX row exists in BACKLOG.md with correct id and refs
      - at least one commit on the current branch cites the FIX id
      - no FIXME(stub) referencing this id exists without a row

    Mode-aware: the local checks always run. The GitHub-side issue
    presence check only runs in mode = "github-sync".
    """
    item = normalize_item(args.item)
    if not FIX_ID_RE.match(item):
        print(f"[validate-fix] only FIX-EE-FF-NN ids are supported, got {item}",
              file=sys.stderr)
        return 1
    findings: list[str] = []

    # 1. Backlog row presence + refs sanity.
    row = find_backlog_row(item)
    if not row:
        findings.append(f"missing BACKLOG row for {item}")
    else:
        cols = parse_backlog_columns(row)
        refs = cols.get("refs", "")
        feat_pattern = "FEAT-" + "-".join(item.split("-")[1:3])  # FEAT-EE-FF
        if feat_pattern not in refs:
            findings.append(
                f"BACKLOG row for {item} does not reference parent {feat_pattern} in Refs"
            )

    # 2. Commit on current branch cites the FIX id.
    try:
        log_out = run([
            "git", "log", "--format=%s%n%b", "--no-merges", "-50",
        ]).stdout
    except subprocess.CalledProcessError:
        log_out = ""
    if item not in log_out:
        findings.append(
            f"no commit on the current branch cites {item} in subject or body"
        )

    # 3. Stub markers without a row.
    try:
        grep_out = run([
            "git", "grep", "-n", "-E", "FIXME\\(stub\\)",
        ], check=False).stdout
    except subprocess.CalledProcessError:
        grep_out = ""
    for line in grep_out.splitlines():
        match = re.search(r"FIX-\d{2}-\d{2}-\d{2}", line)
        if match:
            stub_id = match.group(0)
            if stub_id == item and not row:
                findings.append(
                    f"FIXME(stub) cites {item} but the BACKLOG row is missing"
                )

    # 4. Optional GitHub-side check.
    if read_dia_mode() == "github-sync" and gh_repo_configured():
        issue = find_issue_for_item(item)
        if not issue:
            findings.append(f"no GitHub issue found for {item}")

    if findings:
        print(json.dumps({"item": item, "ok": False, "findings": findings}, indent=2))
        return 1
    print(json.dumps({"item": item, "ok": True, "findings": []}, indent=2))
    return 0


# ---------- Subcommand: status ------------------------------------------

def cmd_status(args: argparse.Namespace) -> int:
    item = normalize_item(args.item)
    # Read-only command, but the three-modes contract pins it to
    # git-only and github-sync. In off the plugin pretends not to be
    # installed, so even the read-only status output stays silent.
    if read_dia_mode() == "off":
        print("[status] mode=off, skipping (run /dia-setup to change)")
        return 0
    print(f"=== Status for {item} ===")
    cur = current_branch()
    print(f"Branch (current):       {cur}")
    print(f"Branch matches item:    {branch_matches_item(cur, item)}")
    print()
    print("Phase tags:")
    for phase in VALID_PHASES:
        # ready-for-review is not a phase, see cmd_tag_phase.
        if phase == "ready-for-review":
            tag = f"{item.lower()}/ready-for-review"
        else:
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


# ---------- Subcommands: preflight + initial-sync -----------------------

_BACKLOG_ROW_RE = re.compile(r"^\|\s*((?:EPIC|FEAT|FIX|IMP)-\d{2}(?:-\d{2}){0,2})\s*\|")


def parse_all_backlog_rows() -> list[dict]:
    """Return every actionable backlog row as parsed columns.

    Each dict carries the column names from parse_backlog_columns plus
    a `raw` key with the original line. One read of BACKLOG.md.
    """
    bl = backlog_path()
    if not bl.exists():
        return []
    rows: list[dict] = []
    for line in bl.read_text(encoding="utf-8").splitlines():
        if not _BACKLOG_ROW_RE.match(line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        cols = parse_backlog_columns({"cells": cells})
        cols["raw"] = line
        rows.append(cols)
    return rows


def _graphql_rate_remaining() -> int | None:
    """GraphQL points remaining for the gh token, or None if unknown."""
    try:
        out = run([
            "gh", "api", "rate_limit",
            "--jq", ".resources.graphql.remaining",
        ]).stdout.strip()
        return int(out) if out else None
    except (subprocess.CalledProcessError, ValueError):
        return None


def cmd_preflight(args: argparse.Namespace) -> int:
    """Read-only validation before a GitHub bulk sync.

    Checks gh reachability, the workflow mode, project reachability and
    whether its Status options cover the backlog vocabulary, that the
    repo labels create-issue needs exist, that the BACKLOG Title column
    carries no doubled id prefix, a small sample of issue states against
    the backlog, and whether the GraphQL rate budget covers a full sync.

    Exits 1 on blockers; warnings alone exit 0 unless --strict.
    """
    strict = bool(getattr(args, "strict", False))
    blockers: list[str] = []
    warnings: list[str] = []
    notes: list[str] = []

    if not has_gh():
        print("[preflight] gh CLI not installed -- nothing to check (local-only mode)")
        return 0
    if not gh_repo_configured():
        print("[preflight] no GitHub remote configured -- nothing to check (local-only mode)")
        return 0
    mode = read_dia_mode()
    if mode != "github-sync":
        warnings.append(
            f"mode is '{mode}' in .dia/config.toml; create-issue / promote-to-epic "
            f"/ sync-status stay no-ops until mode = 'github-sync'"
        )

    cfg = read_dia_github_config()
    project_number = cfg.get("project_number")
    project_owner = _resolve_project_owner(cfg)
    project_options: list[str] = []

    if project_number:
        try:
            pn: int | None = int(project_number)
        except (TypeError, ValueError):
            blockers.append(f"project_number = {project_number!r} in .dia/config.toml is not an integer")
            pn = None
        if pn is not None and not project_owner:
            blockers.append("could not resolve the project owner login (set [github] project_owner)")
        elif pn is not None:
            try:
                run(["gh", "project", "view", str(pn), "--owner", project_owner, "--format", "json"])
                notes.append(f"project #{pn} reachable (owner {project_owner})")
            except subprocess.CalledProcessError as e:
                err = (e.stderr or "").lower()
                if "scope" in err or "auth refresh" in err:
                    blockers.append(f"project #{pn}: token missing the 'project' scope -- run `gh auth refresh -s project`")
                else:
                    blockers.append(f"project #{pn} not reachable as {project_owner}: {(e.stderr or '').strip()}")
            fields = _project_fields(pn, project_owner)
            if fields is None:
                blockers.append("gh project field-list failed (auth scope? rate limit?)")
            else:
                field_name = cfg.get("status_field", "Status")
                tf = next(
                    (f for f in fields
                     if str(f.get("name", "")).strip().casefold() == field_name.strip().casefold()),
                    None,
                )
                if not tf:
                    blockers.append(f"project has no '{field_name}' field")
                else:
                    project_options = [str(o.get("name", "")) for o in tf.get("options", [])]
                    notes.append(f"project Status options: {', '.join(project_options) or '(none)'}")
    else:
        warnings.append("no [github] project_number in .dia/config.toml; status mirroring runs via issue open/close only")

    rows = parse_all_backlog_rows()
    if not rows:
        warnings.append("BACKLOG.md has no actionable rows")

    # Status vocabulary vs project options.
    for s in sorted({r.get("status", "").strip() for r in rows if r.get("status", "").strip()}):
        gh_status = map_status_to_github(s)
        if gh_status is None:
            blockers.append(f"BACKLOG status '{s}' has no GitHub mapping (allowed: {', '.join(ALLOWED_STATUSES)})")
        elif project_options and not any(o.strip().casefold() == gh_status.strip().casefold() for o in project_options):
            blockers.append(
                f"BACKLOG status '{s}' maps to '{gh_status}', which is not an option on the project "
                f"Status field (has: {', '.join(project_options)})"
            )

    # Required labels.
    needed_labels: set[str] = {"phase:planned", "epic"}
    for r in rows:
        needed_labels.add(type_label(r["id"]))
        for p in ("P0", "P1", "P2", "P3"):
            if p in r.get("raw", ""):
                needed_labels.add(p.lower())
    try:
        out = run(["gh", "label", "list", "--limit", "300", "--json", "name"]).stdout
        existing_labels = {str(x.get("name", "")).casefold() for x in json.loads(out)}
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        existing_labels = set()
        warnings.append("could not list repo labels (gh label list failed)")
    if existing_labels:
        missing = sorted(l for l in needed_labels if l.casefold() not in existing_labels)
        if missing:
            blockers.append("missing repo labels (gh issue create will fail): " + ", ".join(missing))
            for l in missing:
                notes.append(f"  fix: gh label create {l}")

    # Title column: doubled id prefix.
    bad_titles = [r["id"] for r in rows if _strip_id_prefix(r.get("title", ""), r["id"]) != r.get("title", "").strip()]
    if bad_titles:
        sample = ", ".join(bad_titles[:10]) + (" ..." if len(bad_titles) > 10 else "")
        warnings.append(
            f"{len(bad_titles)} BACKLOG row(s) carry an id prefix in the Title column; flow.py strips "
            f"it defensively but the writer skill should not emit it: {sample}"
        )

    # Sample issue-state drift (<= 5 items that already link an issue).
    sampled = 0
    for r in rows:
        if sampled >= 5:
            break
        m = re.search(r"https://github\.com/[^\s)\]]+/issues/(\d+)", r.get("notes", ""))
        if not m:
            continue
        sampled += 1
        num = int(m.group(1))
        try:
            st = json.loads(run(["gh", "issue", "view", str(num), "--json", "state"]).stdout).get("state", "").lower()
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            continue
        gh_status = map_status_to_github(r.get("status", "").strip()) or ""
        if (gh_status == "Done") != (st == "closed"):
            warnings.append(f"{r['id']}: BACKLOG status '{r.get('status', '')}' but issue #{num} is {st}")

    # GraphQL rate budget.
    n_epics = len([i for i in list_all_backlog_items() if i.startswith("EPIC-")])
    n_subs = len([r for r in rows if not r["id"].startswith("EPIC-")])
    estimate = n_epics * 8 + n_subs * 5 + 20
    remaining = _graphql_rate_remaining()
    if remaining is not None:
        notes.append(
            f"GraphQL budget: ~{remaining} points left; a full sync of {n_epics} epic(s) "
            f"+ {n_subs} sub-item(s) is roughly ~{estimate} calls"
        )
        if remaining < estimate:
            warnings.append(
                f"GraphQL budget (~{remaining}) is below the rough estimate (~{estimate}); "
                f"run initial-sync in batches or wait for the hourly reset"
            )

    print("=== flow.py preflight ===")
    for n in notes:
        print(f"  - {n}")
    for w in warnings:
        print(f"  WARN: {w}")
    for b in blockers:
        print(f"  BLOCKER: {b}")
    if not blockers and not warnings:
        print("  all checks passed")
    if blockers:
        print(f"\n{len(blockers)} blocker(s) -- fix before running initial-sync / promote-to-epic.")
        return 1
    if warnings and strict:
        print(f"\n{len(warnings)} warning(s) and --strict -- treating as failure.")
        return 1
    if warnings:
        print(f"\n{len(warnings)} warning(s) -- review, then proceed.")
    return 0


def cmd_initial_sync(args: argparse.Namespace) -> int:
    """Bulk-onboard an existing backlog onto GitHub in one pass.

    flow.py is built for the incremental Handoff Ritual (one item per
    phase transition). A fresh /reverse-engineering or /dia-migration
    leaves a backlog with dozens of items that never went through that
    ritual. initial-sync walks the whole backlog once:

      1. preflight (skippable with --skip-preflight)
      2. per epic: create the epic issue if missing, then promote-to-epic
         (sub-issues created + linked, bodies mirrored, status synced)
      3. per standalone item (FEAT/FIX/IMP with no matching EPIC row):
         create-issue + sync-status

    Idempotent and resumable: re-running skips items that already have an
    issue. --dry-run prints the plan without touching GitHub. The per-run
    project caches keep the GraphQL cost to a couple of project scans.
    """
    if not mode_active_or_skip("promote-to-epic"):
        return 0
    if not gh_repo_configured():
        print("[initial-sync] gh CLI / GitHub remote not configured -- skipping")
        return 0

    dry = bool(getattr(args, "dry_run", False))
    rows = parse_all_backlog_rows()
    if not rows:
        print("[initial-sync] BACKLOG.md has no actionable rows")
        return 0

    if not dry and not bool(getattr(args, "skip_preflight", False)):
        rc = cmd_preflight(argparse.Namespace(strict=False))
        if rc != 0:
            print("[initial-sync] preflight reported blockers -- aborting. "
                  "Fix them, or re-run with --skip-preflight to override.")
            return 1
        print()

    # Epics live as `### EPIC-NN:` headings (and sometimes also as a
    # table row); list_all_backlog_items picks up both forms.
    epics = [i for i in list_all_backlog_items() if i.startswith("EPIC-")]
    epic_nums = {e.split("-", 1)[1] for e in epics}
    sub_rows = [r["id"] for r in rows if not r["id"].startswith("EPIC-")]
    standalone = [
        rid for rid in sub_rows
        if len(rid.split("-")) > 1 and rid.split("-")[1] not in epic_nums
    ]
    epic_bound = len(sub_rows) - len(standalone)
    print(f"[initial-sync] {len(epics)} epic(s), {epic_bound} epic-bound sub-item(s), "
          f"{len(standalone)} standalone item(s)")

    if dry:
        for e in epics:
            _promote_to_epic_dry_run(e, None)
        for s in standalone:
            ex = find_issue_for_item(s)
            print(f"[initial-sync --dry-run] standalone {s}: "
                  + (f"issue #{ex['number']} exists -> would refresh body + status"
                     if ex else "no issue -> would create + status-sync"))
        return 0

    failed = 0
    for e in epics:
        created_epic = None
        if not find_issue_for_item(e) and not find_raw_issue_by_title(title_for_item(e)):
            created_epic = create_issue_for_item(e)
            if not created_epic:
                print(f"[initial-sync] WARNING: could not create epic issue for {e}; skipping",
                      file=sys.stderr)
                failed += 1
                continue
        rc = cmd_promote_to_epic(argparse.Namespace(
            item=e,
            parent_issue=created_epic["number"] if created_epic else None,
            rename_branch=False, sync_bodies=True, dry_run=False,
        ))
        if rc != 0:
            failed += 1
    for s in standalone:
        rc1 = cmd_create_issue(argparse.Namespace(item=s, update_body=True))
        rc2 = cmd_sync_status(argparse.Namespace(item=s))
        if rc1 != 0 or rc2 != 0:
            failed += 1

    total = len(epics) + len(standalone)
    print(f"[initial-sync] done: {total} top-level item(s) processed, {failed} with errors")
    return 0 if failed == 0 else 1


# ---------- Argparse ----------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("create-issue", help="Create a GitHub issue for the item")
    p1.add_argument("--item", required=True)
    p1.add_argument(
        "--update-body", action="store_true",
        help="If the issue already exists, overwrite its body with the "
             "current detail-file content (retro-sync).",
    )
    p1.set_defaults(func=cmd_create_issue)

    p2 = sub.add_parser("tag-phase", help="Set the phase-done tag")
    p2.add_argument("--item", required=True)
    p2.add_argument(
        "--phase", required=True,
        choices=VALID_PHASES + tuple(PHASE_ALIASES.keys()),
    )
    p2.set_defaults(func=cmd_tag_phase)

    p3 = sub.add_parser("open-draft-pr", help="Open a draft PR for the item branch")
    p3.add_argument("--item", required=True)
    p3.set_defaults(func=cmd_open_draft_pr)

    p4 = sub.add_parser("ready-for-review", help="Mark PR ready for review")
    p4.add_argument("--item", required=True)
    p4.add_argument("--with-sec", "--with-audit", action="store_true",
                    dest="with_sec",
                    help="Require sec-done tag in addition to code/test (legacy --with-audit accepted)")
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
    p7.add_argument(
        "--sync-bodies", dest="sync_bodies", action="store_true", default=True,
        help="Mirror epic and sub-issue bodies from the detail files (default).",
    )
    p7.add_argument(
        "--no-sync-bodies", dest="sync_bodies", action="store_false",
        help="Do not touch epic / sub-issue bodies (only titles, links, tasklist).",
    )
    p7.add_argument(
        "--dry-run", dest="dry_run", action="store_true",
        help="Print what would happen (read-only lookups only); make no changes.",
    )
    p7.set_defaults(func=cmd_promote_to_epic, sync_bodies=True, dry_run=False)

    p8 = sub.add_parser(
        "validate-fix",
        help="Hotfix-scoped consistency check: BACKLOG row, commit cite, stub markers, optional GitHub issue",
    )
    p8.add_argument("--item", required=True, help="FIX-EE-FF-NN")
    p8.set_defaults(func=cmd_validate_fix)

    p9 = sub.add_parser(
        "apply-renumber",
        help="Apply a renumber plan (from renumber-for-merge.py --plan-out) to GitHub issue titles",
    )
    p9.add_argument("--plan", required=True,
                    help="path to the JSON plan file written by renumber-for-merge.py")
    p9.set_defaults(func=cmd_apply_renumber)

    p10 = sub.add_parser(
        "sync-project-status",
        help="Bulk-mirror BACKLOG Status to the GitHub Project status field for one item, an epic and its sub-items, or every backlog item.",
    )
    p10_group = p10.add_mutually_exclusive_group(required=True)
    p10_group.add_argument("--item", help="single backlog item id (EPIC-NN, FEAT-EE-FF, IMP-EE-FF-NN, FIX-EE-FF-NN)")
    p10_group.add_argument("--epic", help="EPIC-NN -- sync the epic plus all its FEAT/IMP/FIX sub-items")
    p10_group.add_argument("--all", action="store_true",
                           help="sync every actionable backlog item")
    p10.set_defaults(func=cmd_sync_project_status)

    p11 = sub.add_parser(
        "preflight",
        help="Read-only validation before a GitHub bulk sync (project reachable, "
             "labels exist, status vocabulary matches, title schema, rate budget).",
    )
    p11.add_argument("--strict", action="store_true",
                     help="treat warnings as failures (exit 1)")
    p11.set_defaults(func=cmd_preflight, strict=False)

    p12 = sub.add_parser(
        "initial-sync",
        help="Bulk-onboard an existing backlog onto GitHub: epics + sub-issues + "
             "standalone items in one resumable pass (runs preflight first).",
    )
    p12.add_argument("--dry-run", dest="dry_run", action="store_true",
                     help="print the plan; make no changes")
    p12.add_argument("--skip-preflight", dest="skip_preflight", action="store_true",
                     help="do not run preflight before syncing")
    p12.set_defaults(func=cmd_initial_sync, dry_run=False, skip_preflight=False)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
