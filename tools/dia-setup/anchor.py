#!/usr/bin/env python3
"""
DIA anchor block management.

Writes, removes, verifies the DIA-WORKFLOW marker block in agent-facing
files such as CLAUDE.md, AGENTS.md, GEMINI.md, .cursorrules,
.github/copilot-instructions.md, .windsurfrules.

Block format (Markdown-style files):
    <!-- DIA-WORKFLOW-START (managed by digital-innovation-agents) -->
    ...rendered template content...
    <!-- DIA-WORKFLOW-END -->

For .cursorrules and .windsurfrules (no Markdown comments), the block
uses hash-comment markers:
    # === DIA-WORKFLOW-START (managed by digital-innovation-agents) ===
    ...rendered template content...
    # === DIA-WORKFLOW-END ===

The script is idempotent: running write again replaces an existing
block. running remove against a file without a block is a no-op.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT_MARKERS = (".git", ".dia")

MD_START = "<!-- DIA-WORKFLOW-START (managed by digital-innovation-agents) -->"
MD_END = "<!-- DIA-WORKFLOW-END -->"
HASH_START = "# === DIA-WORKFLOW-START (managed by digital-innovation-agents) ==="
HASH_END = "# === DIA-WORKFLOW-END ==="

MD_BLOCK_RE = re.compile(
    re.escape(MD_START) + r".*?" + re.escape(MD_END),
    re.DOTALL,
)
HASH_BLOCK_RE = re.compile(
    re.escape(HASH_START) + r".*?" + re.escape(HASH_END),
    re.DOTALL,
)


@dataclass(frozen=True)
class TargetFile:
    """Describes a known anchor target file."""

    relative_path: str
    template_name: str
    style: str  # "markdown" or "hash"

    @property
    def start_marker(self) -> str:
        return MD_START if self.style == "markdown" else HASH_START

    @property
    def end_marker(self) -> str:
        return MD_END if self.style == "markdown" else HASH_END

    @property
    def block_re(self) -> re.Pattern[str]:
        return MD_BLOCK_RE if self.style == "markdown" else HASH_BLOCK_RE


# Known agent files we manage anchors for.
# Order matters for status output.
KNOWN_TARGETS: tuple[TargetFile, ...] = (
    TargetFile("CLAUDE.md", "anchor-claude.md.tmpl", "markdown"),
    TargetFile("AGENTS.md", "anchor-claude.md.tmpl", "markdown"),
    TargetFile("GEMINI.md", "anchor-gemini.md.tmpl", "markdown"),
    TargetFile(".cursorrules", "anchor-cursor.tmpl", "hash"),
    TargetFile(".github/copilot-instructions.md", "anchor-copilot.md.tmpl", "markdown"),
    TargetFile(".windsurfrules", "anchor-windsurf.tmpl", "hash"),
)


def find_repo_root(start: Path) -> Path:
    """Walk upwards from start until a .git or .dia marker is found.

    Falls back to start if nothing matches.
    """
    candidate = start.resolve()
    while True:
        for marker in REPO_ROOT_MARKERS:
            if (candidate / marker).exists():
                return candidate
        if candidate.parent == candidate:
            return start.resolve()
        candidate = candidate.parent


def template_dir() -> Path:
    """Resolve the templates directory relative to this script."""
    here = Path(__file__).resolve().parent
    candidates = (
        here.parent.parent / "skills" / "dia-setup" / "templates",
        here.parent / "skills" / "dia-setup" / "templates",
    )
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError(
        "dia-setup templates not found. expected at "
        + str(candidates[0])
    )


def load_template(target: TargetFile) -> str:
    path = template_dir() / target.template_name
    if not path.exists():
        raise FileNotFoundError(f"template not found: {path}")
    return path.read_text(encoding="utf-8")


def render(template: str, mode: str, repo_root: Path) -> str:
    """Replace {{mode}} and {{repo_name}} placeholders.

    Keeps it deliberately simple: no Jinja, no escaping. Templates are
    plain text and trusted.
    """
    return (
        template
        .replace("{{mode}}", mode)
        .replace("{{repo_name}}", repo_root.name)
    )


def build_block(target: TargetFile, mode: str, repo_root: Path) -> str:
    body = render(load_template(target), mode, repo_root).rstrip()
    return f"{target.start_marker}\n{body}\n{target.end_marker}\n"


def has_block(text: str, target: TargetFile) -> bool:
    return target.block_re.search(text) is not None


def replace_or_append_block(text: str, block: str, target: TargetFile) -> str:
    """Either replace an existing block or append at end of file."""
    if has_block(text, target):
        # Strip trailing newline of replacement so we don't grow the file.
        return target.block_re.sub(block.rstrip(), text)
    sep = "" if text.endswith("\n") or text == "" else "\n"
    leading_blank = "" if text == "" or text.endswith("\n\n") else "\n"
    return f"{text}{sep}{leading_blank}{block}"


def remove_block(text: str, target: TargetFile) -> str:
    new = target.block_re.sub("", text)
    # Collapse leftover triple blank lines to maintain tidy files.
    while "\n\n\n" in new:
        new = new.replace("\n\n\n", "\n\n")
    return new.rstrip() + "\n" if new.strip() else ""


def resolve_target(repo_root: Path, name: str) -> TargetFile | None:
    for target in KNOWN_TARGETS:
        if target.relative_path == name:
            return target
    return None


def expand_targets(repo_root: Path, requested: list[str]) -> list[TargetFile]:
    if not requested:
        return [t for t in KNOWN_TARGETS if (repo_root / t.relative_path).exists()]
    out: list[TargetFile] = []
    for name in requested:
        target = resolve_target(repo_root, name)
        if target is None:
            raise SystemExit(f"unknown target file: {name}")
        out.append(target)
    return out


def cmd_write(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve() if args.repo_root else find_repo_root(Path.cwd())
    targets = expand_targets(repo_root, args.files)
    if not targets:
        print("no known agent files detected and no --files given", file=sys.stderr)
        return 1
    changes: list[dict[str, str]] = []
    for target in targets:
        path = repo_root / target.relative_path
        if not path.exists():
            if args.create_missing:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("", encoding="utf-8")
            else:
                changes.append({"path": str(target.relative_path), "status": "skipped (missing)"})
                continue
        original = path.read_text(encoding="utf-8")
        block = build_block(target, args.mode, repo_root)
        updated = replace_or_append_block(original, block, target)
        if original == updated:
            changes.append({"path": str(target.relative_path), "status": "unchanged"})
            continue
        if args.dry_run:
            changes.append({"path": str(target.relative_path), "status": "would write"})
            continue
        path.write_text(updated, encoding="utf-8")
        changes.append({
            "path": str(target.relative_path),
            "status": "wrote" if not has_block(original, target) else "replaced",
        })
    print(json.dumps({"mode": args.mode, "changes": changes}, indent=2))
    return 0


def cmd_remove(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve() if args.repo_root else find_repo_root(Path.cwd())
    targets = expand_targets(repo_root, args.files if not args.all else [])
    if args.all:
        targets = list(KNOWN_TARGETS)
    changes: list[dict[str, str]] = []
    for target in targets:
        path = repo_root / target.relative_path
        if not path.exists():
            changes.append({"path": str(target.relative_path), "status": "missing"})
            continue
        original = path.read_text(encoding="utf-8")
        if not has_block(original, target):
            changes.append({"path": str(target.relative_path), "status": "no-block"})
            continue
        updated = remove_block(original, target)
        if args.dry_run:
            changes.append({"path": str(target.relative_path), "status": "would remove"})
            continue
        if updated == "":
            # Keep the file but ensure it's empty rather than deleting it.
            path.write_text("", encoding="utf-8")
        else:
            path.write_text(updated, encoding="utf-8")
        changes.append({"path": str(target.relative_path), "status": "removed"})
    print(json.dumps({"changes": changes}, indent=2))
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve() if args.repo_root else find_repo_root(Path.cwd())
    rows: list[dict[str, object]] = []
    for target in KNOWN_TARGETS:
        path = repo_root / target.relative_path
        if not path.exists():
            rows.append({"path": target.relative_path, "exists": False, "block": False})
            continue
        text = path.read_text(encoding="utf-8")
        rows.append({
            "path": target.relative_path,
            "exists": True,
            "block": has_block(text, target),
        })
    print(json.dumps({"repo_root": str(repo_root), "files": rows}, indent=2))
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve() if args.repo_root else find_repo_root(Path.cwd())
    config_path = repo_root / ".dia" / "config.toml"
    if not config_path.exists():
        print("no .dia/config.toml found", file=sys.stderr)
        return 2
    text = config_path.read_text(encoding="utf-8")
    expected = parse_anchor_files(text)
    missing: list[str] = []
    for name in expected:
        target = resolve_target(repo_root, name)
        if target is None:
            missing.append(f"{name} (unknown target)")
            continue
        path = repo_root / target.relative_path
        if not path.exists() or not has_block(path.read_text(encoding="utf-8"), target):
            missing.append(name)
    if missing:
        print(json.dumps({"verified": False, "missing": missing}, indent=2))
        return 1
    print(json.dumps({"verified": True, "files": expected}, indent=2))
    return 0


def parse_anchor_files(toml_text: str) -> list[str]:
    """Minimal TOML reader for our config: pulls anchor_files = [...].

    The standard library ships tomllib in 3.11+. We use it when
    available; fall back to a tiny regex scan otherwise to keep the
    script dependency-free on older Pythons.
    """
    try:
        import tomllib  # type: ignore[import-not-found]

        data = tomllib.loads(toml_text)
        files = data.get("anchor_files", [])
        if not isinstance(files, list):
            return []
        return [str(f) for f in files]
    except ModuleNotFoundError:
        match = re.search(r"anchor_files\s*=\s*\[([^\]]*)\]", toml_text)
        if not match:
            return []
        items = re.findall(r'"([^"]+)"', match.group(1))
        return list(items)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dia-setup-anchor",
        description="manage DIA workflow anchor blocks in agent files",
    )
    parser.add_argument(
        "--repo-root",
        help="explicit repo root, overrides auto-detection",
        default=None,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_write = sub.add_parser("write", help="write or refresh anchor blocks")
    p_write.add_argument("--mode", choices=("off", "git-only", "github-sync"), required=True)
    p_write.add_argument("--files", nargs="*", default=[], help="explicit list of agent files")
    p_write.add_argument("--create-missing", action="store_true", help="create the file if missing")
    p_write.add_argument("--dry-run", action="store_true")
    p_write.set_defaults(func=cmd_write)

    p_remove = sub.add_parser("remove", help="remove anchor blocks")
    p_remove.add_argument("--files", nargs="*", default=[])
    p_remove.add_argument("--all", action="store_true", help="remove from all known targets")
    p_remove.add_argument("--dry-run", action="store_true")
    p_remove.set_defaults(func=cmd_remove)

    p_status = sub.add_parser("status", help="show anchor presence")
    p_status.set_defaults(func=cmd_status)

    p_verify = sub.add_parser("verify", help="verify anchors match config")
    p_verify.set_defaults(func=cmd_verify)

    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
