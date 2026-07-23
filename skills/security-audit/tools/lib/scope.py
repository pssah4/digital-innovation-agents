"""Scope resolution for the security-audit scan.

The auditor asks WHAT to audit before running. Each scope maps to a
deterministic git query that yields the list of files in scope:

    full     all tracked files                     git ls-files
    working  uncommitted changes + untracked       git diff HEAD + ls-files -o
    commit   the last commit                        git diff HEAD~1..HEAD
    staged   only staged changes                    git diff --cached
    branch   branch vs merge-base with a base ref   git diff <merge-base>..HEAD
    range    a free commit range A..B               git diff A..B

Hard rule against scope blindness (enforced by the caller, documented
here): a diff scope narrows only WHERE findings are reported, never the
reachability context. Scanners still parse the full tree; they just
attribute findings to files in this list. Deleted files are filtered out
(nothing for a scanner to read).
"""
from __future__ import annotations
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

DIFF_SCOPES = ("working", "commit", "staged", "branch", "range")
ALL_SCOPES = ("full",) + DIFF_SCOPES


@dataclass
class ScopeResult:
    scope: str
    files: list          # repo-relative paths, existing in the working tree
    detail: str          # human-readable description of what was resolved


def _git(root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=root, text=True
    )


def _existing(root: Path, paths) -> list:
    """Keep only paths that still exist in the working tree, de-duped and
    sorted. A diff can name a deleted file; a scanner cannot read it.
    """
    seen = set()
    out = []
    for p in paths:
        p = p.strip()
        if not p or p in seen:
            continue
        if (root / p).is_file():
            seen.add(p)
            out.append(p)
    return sorted(out)


def _lines(text: str):
    return [ln for ln in text.splitlines() if ln.strip()]


def resolve_scope(
    root: Path,
    scope: str,
    base: str = "main",
    rng: Optional[str] = None,
) -> ScopeResult:
    """Resolve `scope` to a concrete file list via git.

    base: reference branch for `branch` scope (default "main").
    rng:  "A..B" commit range for `range` scope.
    """
    if scope == "full":
        files = _existing(root, _lines(_git(root, "ls-files")))
        return ScopeResult("full", files, "all tracked files")

    if scope == "working":
        changed = _lines(_git(root, "diff", "--name-only", "HEAD"))
        untracked = _lines(_git(root, "ls-files", "--others", "--exclude-standard"))
        files = _existing(root, changed + untracked)
        return ScopeResult("working", files, "uncommitted changes + untracked")

    if scope == "staged":
        files = _existing(root, _lines(_git(root, "diff", "--cached", "--name-only")))
        return ScopeResult("staged", files, "staged changes")

    if scope == "commit":
        # HEAD~1..HEAD; on a root commit with no parent, fall back to the
        # files introduced by HEAD itself.
        try:
            names = _git(root, "diff", "--name-only", "HEAD~1..HEAD")
        except subprocess.CalledProcessError:
            names = _git(root, "show", "--name-only", "--pretty=format:", "HEAD")
        files = _existing(root, _lines(names))
        return ScopeResult("commit", files, "last commit (HEAD~1..HEAD)")

    if scope == "branch":
        merge_base = _git(root, "merge-base", base, "HEAD").strip()
        names = _git(root, "diff", "--name-only", f"{merge_base}..HEAD")
        files = _existing(root, _lines(names))
        return ScopeResult(
            "branch", files, f"branch vs merge-base({base}) {merge_base[:8]}"
        )

    if scope == "range":
        if not rng or ".." not in rng:
            raise ValueError("range scope requires rng='A..B'")
        names = _git(root, "diff", "--name-only", rng)
        files = _existing(root, _lines(names))
        return ScopeResult("range", files, f"commit range {rng}")

    raise ValueError(
        f"unknown scope '{scope}'; expected one of {', '.join(ALL_SCOPES)}"
    )
