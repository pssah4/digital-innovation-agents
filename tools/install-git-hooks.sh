#!/usr/bin/env bash
# install-git-hooks.sh -- install DIA git hooks into a target project.
#
# Usage (run from inside the target project's repo root):
#     bash <DIA-source>/tools/install-git-hooks.sh
#     bash <DIA-source>/tools/install-git-hooks.sh --uninstall
#
# Installation strategy:
#   1. Copy tools/consistency-check.py to <target>/.git/hooks-data/
#      (so the hook keeps working even if the DIA repo moves).
#   2. Copy tools/git-hooks/pre-commit to <target>/.git/hooks/pre-commit.
#   3. Make both executable.
#
# This puts hook code under .git/, so it is project-local and not
# committed. Update path: re-run this installer when DIA releases a
# new tool version.

set -euo pipefail

DIA_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIA_ROOT="$(cd "$DIA_SCRIPT_DIR/.." && pwd)"

if ! command -v git >/dev/null 2>&1; then
    echo "ERROR: git is not installed." >&2
    exit 1
fi

TARGET_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || {
    echo "ERROR: not inside a git repository. Run from the target project's working tree." >&2
    exit 1
}

HOOK_DST="$TARGET_ROOT/.git/hooks/pre-commit"
DATA_DIR="$TARGET_ROOT/.git/hooks-data"

if [ "${1:-}" = "--uninstall" ]; then
    rm -f "$HOOK_DST"
    rm -rf "$DATA_DIR"
    echo "[install-git-hooks] uninstalled."
    exit 0
fi

mkdir -p "$DATA_DIR"
cp "$DIA_ROOT/tools/consistency-check.py" "$DATA_DIR/consistency-check.py"
chmod +x "$DATA_DIR/consistency-check.py"

if [ -e "$HOOK_DST" ] && [ ! -L "$HOOK_DST" ]; then
    cp "$HOOK_DST" "$HOOK_DST.bak"
    echo "[install-git-hooks] backed up existing pre-commit to pre-commit.bak"
fi

cp "$DIA_ROOT/tools/git-hooks/pre-commit" "$HOOK_DST"
chmod +x "$HOOK_DST"

echo "[install-git-hooks] installed in $TARGET_ROOT"
echo "  pre-commit hook : .git/hooks/pre-commit"
echo "  hook data       : .git/hooks-data/consistency-check.py"
echo
echo "Test: git commit --allow-empty -m 'test'"
echo "Bypass any single commit: git commit --no-verify"
echo "Uninstall: bash $0 --uninstall"
