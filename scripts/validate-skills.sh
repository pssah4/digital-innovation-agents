#!/usr/bin/env bash
# validate-skills.sh
# Validates the frontmatter of every skills/<phase>/SKILL.md:
#   - file exists and has YAML frontmatter fenced by ---
#   - `name` field present and matches the directory name
#   - `description` field present, non-empty, within reasonable length
#   - `depends_on` (optional) is a flow-style list of valid skill names,
#     with no self-reference and no cycles across the whole set
#
# Exit code 0 on success, 1 on any validation failure.
#
# Intended for local pre-commit use and CI.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"

# Anthropic recommends descriptions <=1024 chars; we allow headroom for
# trigger-rich descriptions but still cap to catch runaway copy-paste.
MAX_DESCRIPTION_LEN=2000
MIN_DESCRIPTION_LEN=20

failures=0
checked=0

if [ ! -d "$SKILLS_DIR" ]; then
  echo "ERROR: skills directory not found at $SKILLS_DIR" >&2
  exit 1
fi

fail() {
  echo "FAIL: $1" >&2
  failures=$((failures + 1))
}

# Collect all known skill directory names once, for depends_on validation.
KNOWN_SKILLS=()
while IFS= read -r -d '' d; do
  KNOWN_SKILLS+=("$(basename "$d")")
done < <(find "$SKILLS_DIR" -mindepth 1 -maxdepth 1 -type d -print0 | sort -z)

is_known_skill() {
  local needle="$1"
  local s
  for s in "${KNOWN_SKILLS[@]}"; do
    if [ "$s" = "$needle" ]; then
      return 0
    fi
  done
  return 1
}

# Associative-array-free dependency storage (bash 3.2 compatible):
# DEPS_NAMES is a parallel list of skill names; DEPS_LISTS[i] holds a
# space-separated list of deps for DEPS_NAMES[i].
DEPS_NAMES=()
DEPS_LISTS=()

record_deps() {
  local name="$1"
  local deps="$2"
  DEPS_NAMES+=("$name")
  DEPS_LISTS+=("$deps")
}

validate_skill() {
  local skill_file="$1"
  local skill_dir
  skill_dir="$(dirname "$skill_file")"
  local expected_name
  expected_name="$(basename "$skill_dir")"
  local rel_path="${skill_file#"$REPO_ROOT/"}"

  checked=$((checked + 1))

  local first_line
  first_line="$(head -n 1 "$skill_file")"
  if [ "$first_line" != "---" ]; then
    fail "$rel_path: missing YAML frontmatter (first line is not '---')"
    return
  fi

  local frontmatter
  frontmatter="$(awk '
    /^---[[:space:]]*$/ {
      fence++
      if (fence == 1) { next }
      if (fence == 2) { exit }
    }
    fence == 1 { print }
  ' "$skill_file")"

  if [ -z "$frontmatter" ]; then
    fail "$rel_path: empty or unterminated frontmatter"
    return
  fi

  # Extract a top-level scalar field value, supporting inline and folded/
  # literal block scalars (>, >-, |, |-).
  extract_field() {
    local field="$1"
    printf '%s\n' "$frontmatter" | awk -v field="$field" '
      BEGIN {
        key_re = "^" field ":"
        found = 0
        inline = ""
        block = ""
        collecting = 0
      }
      {
        if (!found) {
          if ($0 ~ key_re) {
            found = 1
            val = $0
            sub(key_re, "", val)
            sub(/^[[:space:]]+/, "", val)
            sub(/[[:space:]]+$/, "", val)
            if (val == ">" || val == ">-" || val == "|" || val == "|-") {
              collecting = 1
            } else {
              inline = val
            }
            next
          }
        } else if (collecting) {
          if ($0 ~ /^[[:space:]]/) {
            line = $0
            sub(/^[[:space:]]+/, "", line)
            sub(/[[:space:]]+$/, "", line)
            if (line == "") { next }
            if (block == "") { block = line } else { block = block " " line }
          } else if ($0 ~ /^[^[:space:]]/) {
            exit
          }
        }
      }
      END {
        if (inline != "") { print inline }
        else { print block }
      }
    '
  }

  # name field
  local name_value
  name_value="$(extract_field "name")"
  if [ -z "$name_value" ]; then
    fail "$rel_path: missing 'name' in frontmatter"
  elif [ "$name_value" != "$expected_name" ]; then
    fail "$rel_path: name '$name_value' does not match directory '$expected_name'"
  fi

  # description field
  local description_value
  description_value="$(extract_field "description")"
  if [ -z "$description_value" ]; then
    fail "$rel_path: missing or empty 'description' in frontmatter"
  else
    local desc_len=${#description_value}
    if [ "$desc_len" -lt "$MIN_DESCRIPTION_LEN" ]; then
      fail "$rel_path: description too short ($desc_len chars, min $MIN_DESCRIPTION_LEN)"
    fi
    if [ "$desc_len" -gt "$MAX_DESCRIPTION_LEN" ]; then
      fail "$rel_path: description too long ($desc_len chars, max $MAX_DESCRIPTION_LEN)"
    fi
  fi

  # depends_on (optional) -- only flow-style "[a, b]" is supported for now
  local deps_raw
  deps_raw="$(extract_field "depends_on")"
  local parsed_deps=""
  if [ -n "$deps_raw" ]; then
    case "$deps_raw" in
      '['*']')
        local inner="${deps_raw#[}"
        inner="${inner%]}"
        # Split on commas, trim each item
        local old_ifs="$IFS"
        IFS=','
        # shellcheck disable=SC2206
        local items=($inner)
        IFS="$old_ifs"
        local item
        if [ "${#items[@]}" -eq 0 ]; then
          record_deps "$expected_name" ""
          return
        fi
        for item in "${items[@]}"; do
          # trim whitespace and surrounding quotes
          item="${item#"${item%%[![:space:]]*}"}"
          item="${item%"${item##*[![:space:]]}"}"
          item="${item#\"}"; item="${item%\"}"
          item="${item#\'}"; item="${item%\'}"
          if [ -z "$item" ]; then continue; fi
          if [ "$item" = "$expected_name" ]; then
            fail "$rel_path: depends_on references itself ('$item')"
            continue
          fi
          if ! is_known_skill "$item"; then
            fail "$rel_path: depends_on references unknown skill '$item'"
            continue
          fi
          parsed_deps="$parsed_deps $item"
        done
        ;;
      *)
        fail "$rel_path: depends_on must be flow-style list, e.g. depends_on: [foo, bar]"
        ;;
    esac
  fi
  record_deps "$expected_name" "$parsed_deps"
}

while IFS= read -r -d '' skill_file; do
  validate_skill "$skill_file"
done < <(find "$SKILLS_DIR" -mindepth 2 -maxdepth 2 -name 'SKILL.md' -print0 | sort -z)

# Verify every skill directory has a SKILL.md
while IFS= read -r -d '' skill_dir; do
  if [ ! -f "$skill_dir/SKILL.md" ]; then
    rel="${skill_dir#"$REPO_ROOT/"}"
    fail "$rel: directory has no SKILL.md"
  fi
done < <(find "$SKILLS_DIR" -mindepth 1 -maxdepth 1 -type d -print0 | sort -z)

# -------- cycle detection across depends_on graph -------------------------

get_deps() {
  local want="$1"
  local i=0
  while [ $i -lt "${#DEPS_NAMES[@]}" ]; do
    if [ "${DEPS_NAMES[$i]}" = "$want" ]; then
      echo "${DEPS_LISTS[$i]}"
      return
    fi
    i=$((i + 1))
  done
}

# Iterative DFS per node. Colours: WHITE (unseen), GRAY (in stack), BLACK (done).
declare_cycle() {
  fail "depends_on cycle involving: $1"
}

CYCLE_PATH=""
visit_color_names=()
visit_color_values=()

get_color() {
  local want="$1"
  local i=0
  while [ $i -lt "${#visit_color_names[@]}" ]; do
    if [ "${visit_color_names[$i]}" = "$want" ]; then
      echo "${visit_color_values[$i]}"
      return
    fi
    i=$((i + 1))
  done
  echo "WHITE"
}

set_color() {
  local target="$1"
  local color="$2"
  local i=0
  while [ $i -lt "${#visit_color_names[@]}" ]; do
    if [ "${visit_color_names[$i]}" = "$target" ]; then
      visit_color_values[$i]="$color"
      return
    fi
    i=$((i + 1))
  done
  visit_color_names+=("$target")
  visit_color_values+=("$color")
}

dfs() {
  local node="$1"
  local path_prefix="$2"
  local current_color
  current_color="$(get_color "$node")"
  if [ "$current_color" = "GRAY" ]; then
    CYCLE_PATH="$path_prefix -> $node"
    return 1
  fi
  if [ "$current_color" = "BLACK" ]; then
    return 0
  fi
  set_color "$node" "GRAY"
  local d
  for d in $(get_deps "$node"); do
    if ! dfs "$d" "$path_prefix -> $node"; then
      return 1
    fi
  done
  set_color "$node" "BLACK"
  return 0
}

# Drive DFS from each skill.
cycle_found=0
for skill in "${KNOWN_SKILLS[@]}"; do
  if [ "$(get_color "$skill")" = "WHITE" ]; then
    if ! dfs "$skill" ""; then
      declare_cycle "${CYCLE_PATH# -> }"
      cycle_found=1
      break
    fi
  fi
done

echo ""
echo "Checked $checked skill file(s); $failures failure(s)."

if [ "$failures" -gt 0 ] || [ "$cycle_found" -ne 0 ]; then
  exit 1
fi
