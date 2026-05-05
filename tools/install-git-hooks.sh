#!/usr/bin/env bash
# install-git-hooks.sh -- install DIA git hooks into a target project.
#
# Usage (run from inside the target project's repo root):
#     bash <DIA-source>/tools/install-git-hooks.sh
#     bash <DIA-source>/tools/install-git-hooks.sh --uninstall
#
# Installation strategy:
#   1. Copy tools/consistency-check.py and tools/renumber-for-merge.py
#      to <target>/.git/hooks-data/ (so the hooks keep working even if
#      the DIA repo moves).
#   2. Copy tools/git-hooks/pre-commit to <target>/.git/hooks/pre-commit.
#   3. Copy tools/git-hooks/pre-merge-commit to
#      <target>/.git/hooks/pre-merge-commit.
#   4. Make all four executable.
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

HOOK_PRE_COMMIT="$TARGET_ROOT/.git/hooks/pre-commit"
HOOK_PRE_MERGE="$TARGET_ROOT/.git/hooks/pre-merge-commit"
DATA_DIR="$TARGET_ROOT/.git/hooks-data"

if [ "${1:-}" = "--uninstall" ]; then
    rm -f "$HOOK_PRE_COMMIT"
    rm -f "$HOOK_PRE_MERGE"
    rm -rf "$DATA_DIR"
    echo "[install-git-hooks] uninstalled."
    exit 0
fi

mkdir -p "$DATA_DIR"
cp "$DIA_ROOT/tools/consistency-check.py" "$DATA_DIR/consistency-check.py"
chmod +x "$DATA_DIR/consistency-check.py"
cp "$DIA_ROOT/tools/renumber-for-merge.py" "$DATA_DIR/renumber-for-merge.py"
chmod +x "$DATA_DIR/renumber-for-merge.py"

for HOOK in pre-commit pre-merge-commit; do
    DST="$TARGET_ROOT/.git/hooks/$HOOK"
    if [ -e "$DST" ] && [ ! -L "$DST" ]; then
        cp "$DST" "$DST.bak"
        echo "[install-git-hooks] backed up existing $HOOK to $HOOK.bak"
    fi
    cp "$DIA_ROOT/tools/git-hooks/$HOOK" "$DST"
    chmod +x "$DST"
done

echo "[install-git-hooks] installed in $TARGET_ROOT"
echo "  pre-commit hook       : .git/hooks/pre-commit"
echo "  pre-merge-commit hook : .git/hooks/pre-merge-commit"
echo "  hook data             : .git/hooks-data/{consistency-check,renumber-for-merge}.py"
echo
echo "Test commit  : git commit --allow-empty -m 'test'"
echo "Test merge   : bash scripts/merge-to-dev.sh <branch> dev"
echo "Bypass once  : git commit --no-verify (or git merge --no-verify)"
echo "Uninstall    : bash $0 --uninstall"
