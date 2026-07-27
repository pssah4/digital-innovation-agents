"""Files that pattern-based scanners (grep-fallback, secret patterns)
should not read.

Two mechanisms combined:

  * Path patterns (fnmatch-style) covering the common bulk sources of
    false positives: test fixtures that intentionally include payloads,
    minified/bundled assets that copy library code, dist/build outputs.

  * A per-file opt-out header: a file whose first ~50 lines contain
    `security-audit-scan: skip` is skipped. Detector modules use this to
    tell the scanner "these regex patterns are MY payloads, don't scan
    me for them".

Both are purely additive to the SAST layer that has real taint analysis
(CodeQL). CodeQL is not affected; it does its own reachability check
and does not confuse a fixture with an exploitable call site.

stdlib-only, deterministic, no network.
"""
from __future__ import annotations
import fnmatch
from pathlib import Path

_SKIP_HEADER_MAX_LINES = 50
_SKIP_HEADER_MARKER = "security-audit-scan: skip"

# fnmatch-style patterns. Matched against POSIX-style relative paths.
_SKIP_GLOBS = (
    # Test files/directories: fixtures deliberately include eval/XSS/etc.
    "**/tests/**",
    "**/test/**",
    "**/__tests__/**",
    "**/test_*.py",
    "**/*_test.py",
    "**/*_test.go",
    "**/*.test.js",
    "**/*.test.ts",
    "**/*.spec.js",
    "**/*.spec.ts",
    # Minified/bundled assets: library code the project did not write.
    "**/*.min.js",
    "**/*.min.css",
    "**/*.min.mjs",
    "**/*.bundle.js",
    # Build outputs and vendored code.
    "**/dist/**",
    "**/build/**",
    "**/out/**",
    "**/coverage/**",
    "**/vendor/**",
    "**/node_modules/**",
)


def _matches_any(rel_posix: str, patterns) -> bool:
    """fnmatch does not treat `**` as multi-level like shell glob does.
    For any pattern that begins with `**/`, also try the pattern with
    the leading `**/` stripped, so `**/dist/**` matches both
    `foo/dist/x.js` and top-level `dist/x.js`.
    """
    for pat in patterns:
        if fnmatch.fnmatchcase(rel_posix, pat):
            return True
        if pat.startswith("**/") and fnmatch.fnmatchcase(rel_posix, pat[3:]):
            return True
    return False


def is_path_skipped(rel_path: str) -> bool:
    """True if the relative path matches any built-in skip glob."""
    rel_posix = rel_path.replace("\\", "/")
    return _matches_any(rel_posix, _SKIP_GLOBS)


def has_skip_header(path: Path) -> bool:
    """True if the file's first N lines contain the opt-out marker.

    Reading is bounded (line count only) so the check is O(header size),
    not O(file size). Returns False on any read error.
    """
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            for _ in range(_SKIP_HEADER_MAX_LINES):
                line = fh.readline()
                if not line:
                    return False
                if _SKIP_HEADER_MARKER in line:
                    return True
        return False
    except OSError:
        return False


def should_scan(rel_path: str, root: Path) -> bool:
    """Overall gate. True iff neither the path nor the file's header
    excludes the file from pattern-based scanning.
    """
    if is_path_skipped(rel_path):
        return False
    return not has_skip_header(root / rel_path)
