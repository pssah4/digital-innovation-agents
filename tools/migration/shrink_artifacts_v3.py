#!/usr/bin/env python3
"""DIA migration -- v3.6.0 shrink: align existing artefacts with shrunk templates.

Walks _devprocess/ and applies surgical edits so that artefacts match the
v3.6.0 conventions: leading meta-HTML stripped, no forbidden frontmatter
keys, no empty refs arrays, no backlog-pointer Status sections, no
ceremony footers. Two read-only warnings flag over-cap files and
duplicated style blocks.

Idempotent: a clean tree produces zero edits and zero warnings.

Usage:
    python3 shrink_artifacts_v3.py --root <project-root> [subcommand] [--dry-run] [--apply]

Subcommands:
    audit           (default) scan and report, no edits
    fix-headers     transformation 1 (strip leading meta-HTML blocks)
    fix-frontmatter transformations 2+3 (strip forbidden keys + empty arrays)
    fix-sections    transformations 4+5 (strip Status / Next-Steps sections)
    warn-caps       transformation 6 (warn only, never edits)
    warn-duplicates transformation 7 (warn only)
    all             run 1-5 with --apply, then 6+7 as warnings

Default mode is --dry-run; --apply is required for writes.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Re-use the frontmatter stripper from Phase 2a.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from strip_frontmatter_status import strip as strip_fm_status  # noqa: E402

FM = re.compile(r"^---\s*$")
HTML_COMMENT_OPEN = re.compile(r"^\s*<!--\s*$|^\s*<!--")
HTML_COMMENT_CLOSE = re.compile(r"-->")

META_MARKERS = (
    "instructions for the agent",
    "this template",
    "save under",
    "status lives in",
    "how to fill",
    "specs: skills/project-conventions",
)
META_MARKERS_KEEP = (
    "see skills/",  # one-line pointer comments stay
)

EMPTY_REFS_KEYS = (
    "asr-refs",
    "feature-refs",
    "related-adrs",
    "depends-on",
)
NULL_REFS_KEYS = (
    "supersedes",
    "superseded-by",
)

STATUS_POINTER_PHRASES = (
    "see backlog row",
    "status, phase, last update live in",
    "status lives in the backlog",
    "backlog row for current status",
    "see backlog for status",
)

CEREMONY_HEADERS = (
    "next steps",
    "promotion footer",
    "transition to ideation",
    "transition to validation",
    "transition to requirements",
    "transition to architecture",
    "transition to coding",
)

DUPLICATE_STYLE_MARKERS = (
    "em dash",
    "ai vocabulary list",
    "status values: backlog, ready, in progress",
)

# Owner-skill inferred from path segment.
OWNER_SKILL_BY_DIR = {
    "analysis": "business-analysis",
    "requirements/epics": "requirements-engineering",
    "requirements/features": "requirements-engineering",
    "requirements/fixes": "coding",
    "requirements/improvements": "coding",
    "requirements/handoff": "requirements-engineering",
    "architecture/adrs": "architecture",
    "architecture": "architecture",
    "implementation/plans": "coding",
    "security": "security-audit",
    "context": "dia-guide",
}

# Per-artefact line caps from skills/project-conventions/SKILL.md section 1.
# (path-substring, filename-prefix) -> cap.
CAPS: list[tuple[str, str, int]] = [
    ("analysis", "BA-PROJECT", 200),
    ("analysis", "BA-EPIC", 120),
    ("analysis", "BA-FEAT", 60),
    ("analysis", "BA-IMP", 40),
    ("analysis", "BA-FIX", 40),
    ("analysis", "BA-MINI", 40),
    ("analysis", "EXPLORATION-BOARD", 70),
    ("analysis", "BA-", 200),  # fallback Project-BA
    ("requirements/epics", "EPIC", 35),
    ("requirements/features", "FEAT", 65),
    ("requirements/features", "FEATURE", 65),
    ("requirements/handoff", "architect-handoff", 60),
    ("requirements/fixes", "FIX", 28),
    ("requirements/fixes", "IMP", 26),
    ("requirements/improvements", "IMP", 26),
    ("architecture/adrs", "ADR", 50),
    ("architecture", "arc42-snapshot", 100),
    ("architecture", "plan-context", 55),
    ("implementation/plans", "PLAN", 50),
    ("security", "AUDIT", 55),
    ("context", "METRICS", 50),
]

TARGET_GLOBS = (
    "_devprocess/analysis/*.md",
    "_devprocess/requirements/epics/*.md",
    "_devprocess/requirements/features/*.md",
    "_devprocess/requirements/fixes/*.md",
    "_devprocess/requirements/improvements/*.md",
    "_devprocess/requirements/handoff/*.md",
    "_devprocess/architecture/adrs/*.md",
    "_devprocess/architecture/*.md",
    "_devprocess/implementation/plans/*.md",
    "_devprocess/security/*.md",
    "_devprocess/context/METRICS.md",
)


@dataclass
class Result:
    audited: int = 0
    edited: int = 0
    warnings: int = 0
    writes: list[str] = field(default_factory=list)
    warns: list[str] = field(default_factory=list)
    ok: list[str] = field(default_factory=list)


def infer_owner_skill(rel_path: str) -> str:
    for key, owner in OWNER_SKILL_BY_DIR.items():
        if f"/{key}/" in f"/{rel_path}/" or f"/{key}" in f"/{rel_path}":
            return owner
    return "dia-guide"


def split_frontmatter(content: str) -> tuple[list[str], list[str]]:
    """Return (frontmatter_lines_incl_fences, body_lines)."""
    lines = content.split("\n")
    if not lines or not FM.match(lines[0]):
        return [], lines
    for i in range(1, len(lines)):
        if FM.match(lines[i]):
            return lines[: i + 1], lines[i + 1 :]
    return [], lines


def join_doc(fm_lines: list[str], body_lines: list[str]) -> str:
    if fm_lines:
        return "\n".join(fm_lines) + "\n" + "\n".join(body_lines)
    return "\n".join(body_lines)


def transform_1_strip_meta_header(content: str, rel_path: str) -> tuple[str, bool]:
    """Strip leading multi-line meta-instruction HTML comments."""
    fm_lines, body_lines = split_frontmatter(content)
    if not body_lines:
        return content, False

    idx = 0
    while idx < len(body_lines) and body_lines[idx].strip() == "":
        idx += 1
    if idx >= len(body_lines):
        return content, False

    first = body_lines[idx]
    if not first.lstrip().startswith("<!--"):
        return content, False

    # Find closing -->.
    end = None
    for j in range(idx, len(body_lines)):
        if HTML_COMMENT_CLOSE.search(body_lines[j]):
            end = j
            break
    if end is None:
        return content, False

    block = "\n".join(body_lines[idx : end + 1]).lower()

    # Keep one-line pointer comments untouched.
    if end == idx and any(k in block for k in META_MARKERS_KEEP) and not any(
        m in block for m in META_MARKERS
    ):
        return content, False

    if not any(m in block for m in META_MARKERS):
        return content, False

    owner = infer_owner_skill(rel_path)
    pointer = f"<!-- See skills/{owner}/SKILL.md for how to fill -->"
    new_body = body_lines[:idx] + [pointer] + body_lines[end + 1 :]
    return join_doc(fm_lines, new_body), True


def transform_2_strip_forbidden_keys(content: str) -> tuple[str, bool]:
    """Strip status, phase, last_updated, author, deciders from frontmatter."""
    # First pass: re-use Phase 2a stripper (status, phase, last_updated variants).
    new, removed = strip_fm_status(content)
    changed = bool(removed)

    # Second pass: author and deciders (not covered by 2a).
    extra_keys = {"author", "deciders"}
    fm_lines, body_lines = split_frontmatter(new)
    if not fm_lines:
        return new, changed

    inner = fm_lines[1:-1]
    out: list[str] = []
    skip = False
    any_removed = False
    for line in inner:
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:", line)
        if m:
            key = m.group(1).lower()
            if key in extra_keys:
                skip = True
                any_removed = True
                continue
            skip = False
            out.append(line)
        elif skip and (
            line.startswith(" ") or line.startswith("\t") or line.strip().startswith("-")
        ):
            any_removed = True
            continue
        else:
            skip = False
            out.append(line)

    if not any_removed:
        return new, changed

    fm_new = ["---"] + out + ["---"]
    return join_doc(fm_new, body_lines), True


def transform_3_strip_empty_refs(content: str) -> tuple[str, bool]:
    """Remove empty list/null relation keys from frontmatter."""
    fm_lines, body_lines = split_frontmatter(content)
    if not fm_lines:
        return content, False

    inner = fm_lines[1:-1]
    out: list[str] = []
    changed = False
    for line in inner:
        stripped = line.strip()
        key_match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$", stripped)
        if key_match:
            key = key_match.group(1).lower()
            value = key_match.group(2).strip()
            if key in EMPTY_REFS_KEYS and value in ("[]", "[ ]"):
                changed = True
                continue
            if key in NULL_REFS_KEYS and value in ("null", "~", ""):
                changed = True
                continue
        out.append(line)

    if not changed:
        return content, False

    fm_new = ["---"] + out + ["---"]
    return join_doc(fm_new, body_lines), True


def transform_4_strip_status_section(content: str) -> tuple[str, bool]:
    """Remove `## Status` H2 sections that only point to the backlog."""
    fm_lines, body_lines = split_frontmatter(content)
    if not body_lines:
        return content, False

    out: list[str] = []
    i = 0
    changed = False
    while i < len(body_lines):
        line = body_lines[i]
        header = re.match(r"^##\s+(Status|Backlog row pointer|Backlog Row Pointer)\s*$", line.strip())
        if header:
            # Collect section until next H2 or EOF.
            j = i + 1
            while j < len(body_lines) and not re.match(r"^##\s+\S", body_lines[j]):
                j += 1
            section = "\n".join(body_lines[i + 1 : j]).lower()
            if any(p in section for p in STATUS_POINTER_PHRASES) or section.strip() == "":
                changed = True
                i = j
                continue
        out.append(line)
        i += 1

    if not changed:
        return content, False
    return join_doc(fm_lines, out), True


def transform_5_strip_ceremony(content: str) -> tuple[str, bool]:
    """Remove Next-Steps / Promotion-footer / Transition sections."""
    fm_lines, body_lines = split_frontmatter(content)
    if not body_lines:
        return content, False

    out: list[str] = []
    i = 0
    changed = False
    while i < len(body_lines):
        line = body_lines[i]
        m = re.match(r"^##\s+(.+?)\s*$", line.strip())
        if m:
            heading = m.group(1).strip().lower()
            if any(heading.startswith(h) for h in CEREMONY_HEADERS):
                j = i + 1
                while j < len(body_lines) and not re.match(r"^##\s+\S", body_lines[j]):
                    j += 1
                changed = True
                i = j
                continue
        out.append(line)
        i += 1

    if not changed:
        return content, False
    return join_doc(fm_lines, out), True


def cap_for(rel_path: str, filename: str) -> int | None:
    for path_sub, prefix, cap in CAPS:
        if path_sub in rel_path and filename.startswith(prefix):
            return cap
    return None


def warn_cap(path: Path, rel_path: str, content: str) -> str | None:
    cap = cap_for(rel_path, path.name)
    if cap is None:
        return None
    if "## Reasoned exception" in content:
        return None
    lines = content.count("\n") + (0 if content.endswith("\n") else 1)
    if lines <= cap:
        return None
    excess = round((lines - cap) / cap * 100)
    return (
        f"{rel_path}: {lines} > cap {cap} "
        f"(excess {excess}%). Add '## Reasoned exception' at top or shrink content."
    )


def warn_duplicate(rel_path: str, content: str) -> str | None:
    fm_lines, body_lines = split_frontmatter(content)
    body_text = "\n".join(body_lines).lower()
    body_no_headers = "\n".join(
        ln for ln in body_text.split("\n") if not ln.lstrip().startswith("#")
    )
    hits = [m for m in DUPLICATE_STYLE_MARKERS if m in body_no_headers]
    if not hits:
        return None
    return (
        f"{rel_path}: duplicated style block "
        f"({', '.join(hits)}). Move to skills/project-conventions/SKILL.md."
    )


def iter_targets(root: Path):
    seen: set[Path] = set()
    for glob in TARGET_GLOBS:
        for fp in root.glob(glob):
            if not fp.is_file() or fp in seen:
                continue
            seen.add(fp)
            yield fp


def run(root: Path, sub: str, apply: bool) -> Result:
    res = Result()
    edit_funcs: list = []
    warn_funcs: list = []

    if sub in ("fix-headers", "all"):
        edit_funcs.append(("header", transform_1_strip_meta_header))
    if sub in ("fix-frontmatter", "all"):
        edit_funcs.append(("fm-keys", lambda c, _p: transform_2_strip_forbidden_keys(c)))
        edit_funcs.append(("empty-refs", lambda c, _p: transform_3_strip_empty_refs(c)))
    if sub in ("fix-sections", "all"):
        edit_funcs.append(("status-section", lambda c, _p: transform_4_strip_status_section(c)))
        edit_funcs.append(("ceremony", lambda c, _p: transform_5_strip_ceremony(c)))
    if sub in ("warn-caps", "all", "audit"):
        warn_funcs.append(("cap", warn_cap))
    if sub in ("warn-duplicates", "all", "audit"):
        warn_funcs.append(("dup", lambda _p, rel, content: warn_duplicate(rel, content)))

    if sub == "audit":
        edit_funcs = [
            ("header", transform_1_strip_meta_header),
            ("fm-keys", lambda c, _p: transform_2_strip_forbidden_keys(c)),
            ("empty-refs", lambda c, _p: transform_3_strip_empty_refs(c)),
            ("status-section", lambda c, _p: transform_4_strip_status_section(c)),
            ("ceremony", lambda c, _p: transform_5_strip_ceremony(c)),
        ]

    for fp in iter_targets(root):
        res.audited += 1
        rel = str(fp.relative_to(root))
        original = fp.read_text(encoding="utf-8")
        current = original

        file_changed = False
        for label, fn in edit_funcs:
            new, changed = fn(current, rel)
            if changed:
                current = new
                file_changed = True
                res.writes.append(f"WRITE: {rel} [{label}]")

        if file_changed:
            res.edited += 1
            if apply:
                fp.write_text(current, encoding="utf-8")

        for label, wfn in warn_funcs:
            if label == "cap":
                msg = wfn(fp, rel, current)
            else:
                msg = wfn(fp, rel, current)
            if msg:
                res.warnings += 1
                res.warns.append(f"WARN: {msg}")

        if not file_changed and not any(
            w.split(": ", 1)[1].startswith(rel) for w in res.warns[-5:]
        ):
            res.ok.append(f"OK: {rel}")

    return res


def print_result(res: Result, apply: bool) -> None:
    for line in res.writes:
        prefix = "WRITE" if apply else "DRY  "
        print(line.replace("WRITE", prefix, 1))
    for line in res.warns:
        print(line)
    mode = "edited" if apply else "would-edit"
    print(
        f"\n{res.audited} files audited, "
        f"{res.edited} {mode}, {res.warnings} warnings"
    )


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--root", required=True, help="project root")
    p.add_argument(
        "subcommand",
        nargs="?",
        default="audit",
        choices=[
            "audit",
            "fix-headers",
            "fix-frontmatter",
            "fix-sections",
            "warn-caps",
            "warn-duplicates",
            "all",
        ],
    )
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", default=True)
    mode.add_argument("--apply", action="store_true")
    args = p.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"ERROR: root {root} does not exist", file=sys.stderr)
        return 2

    apply = args.apply and args.subcommand not in ("audit", "warn-caps", "warn-duplicates")
    res = run(root, args.subcommand, apply)
    print_result(res, apply)
    return 0


if __name__ == "__main__":
    sys.exit(main())
