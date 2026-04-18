#!/usr/bin/env bash
# check-manifest-drift.sh
# Verifies that every place in the repo which enumerates skill names
# agrees with the actual set of `skills/<name>/` directories.
#
# Checked sources:
#   1. scripts/install-skills.sh   -- SKILLS=(...) array
#   2. scripts/install-skills.sh   -- "/NAME -- description" echo lines
#   3. hooks/session-start         -- any `skills/<NAME>/` path referenced
#
# Exit code 0 on agreement, 1 on any drift.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"
INSTALL="$REPO_ROOT/scripts/install-skills.sh"
SESSION_HOOK="$REPO_ROOT/hooks/session-start"

failures=0

fail() {
  echo "FAIL: $1" >&2
  failures=$((failures + 1))
}

if [ ! -d "$SKILLS_DIR" ]; then
  echo "ERROR: $SKILLS_DIR not found" >&2
  exit 1
fi

# --- Truth: actual skill directory names ---------------------------------

ACTUAL=()
while IFS= read -r -d '' d; do
  ACTUAL+=("$(basename "$d")")
done < <(find "$SKILLS_DIR" -mindepth 1 -maxdepth 1 -type d -print0 | sort -z)

contains() {
  local needle="$1"; shift
  local item
  for item in "$@"; do
    if [ "$item" = "$needle" ]; then return 0; fi
  done
  return 1
}

compare_sets() {
  local source_label="$1"
  local truth_label="$2"
  shift 2
  # Parse the first half of args as "source" list, then -- , then "truth" list.
  # Instead, we pass two newline-separated blobs via env.
  local source_list="$SRC_LIST"
  local truth_list="$TRUTH_LIST"
  local s
  while IFS= read -r s; do
    [ -z "$s" ] && continue
    if ! printf '%s\n' "$truth_list" | grep -qx -- "$s"; then
      fail "$source_label lists '$s' but no matching directory under $truth_label"
    fi
  done <<< "$source_list"
  while IFS= read -r s; do
    [ -z "$s" ] && continue
    if ! printf '%s\n' "$source_list" | grep -qx -- "$s"; then
      fail "$truth_label has '$s' but $source_label does not list it"
    fi
  done <<< "$truth_list"
}

TRUTH_LIST="$(printf '%s\n' "${ACTUAL[@]}" | sort -u)"

# --- Source 1: install-skills.sh SKILLS=(...) ----------------------------

if [ ! -f "$INSTALL" ]; then
  fail "missing $INSTALL"
else
  ARRAY_LIST="$(awk '
    /^SKILLS=\(/ { inside=1; next }
    inside && /^\)/ { inside=0; next }
    inside {
      line = $0
      gsub(/#.*/, "", line)
      gsub(/"/, "", line)
      gsub(/^[[:space:]]+|[[:space:]]+$/, "", line)
      if (length(line) > 0) print line
    }
  ' "$INSTALL" | sort -u)"

  SRC_LIST="$ARRAY_LIST"
  compare_sets "install-skills.sh SKILLS=()" "skills/"
fi

# --- Source 2: install-skills.sh "/NAME -- description" echo lines -------

if [ -f "$INSTALL" ]; then
  ECHO_LIST="$(awk '
    /^echo[[:space:]]+"[[:space:]]*\// {
      match($0, /\/[a-z0-9][a-z0-9-]*/)
      if (RSTART > 0) {
        name = substr($0, RSTART + 1, RLENGTH - 1)
        print name
      }
    }
  ' "$INSTALL" | sort -u)"

  # The echo list is a user-facing summary and may legitimately skip
  # the "meta" skills project-conventions, reverse-engineering, and
  # using-digital-innovation-agents. So we only flag names that are
  # listed in the echo output but do NOT exist as skill directories.
  while IFS= read -r name; do
    [ -z "$name" ] && continue
    if ! contains "$name" "${ACTUAL[@]}"; then
      fail "install-skills.sh echo lists '/$name' but no skill directory exists"
    fi
  done <<< "$ECHO_LIST"
fi

# --- Source 3: hooks/session-start references ----------------------------

if [ -f "$SESSION_HOOK" ]; then
  HOOK_LIST="$(grep -oE 'skills/[a-z0-9][a-z0-9-]*' "$SESSION_HOOK" \
    | awk -F/ '{print $2}' | sort -u || true)"
  while IFS= read -r name; do
    [ -z "$name" ] && continue
    if ! contains "$name" "${ACTUAL[@]}"; then
      fail "hooks/session-start references 'skills/$name' but no such directory exists"
    fi
  done <<< "$HOOK_LIST"
fi

echo ""
if [ "$failures" -eq 0 ]; then
  echo "Manifest drift check: OK. ${#ACTUAL[@]} skill directory(ies)."
  exit 0
fi
echo "Manifest drift check: $failures failure(s)."
exit 1
