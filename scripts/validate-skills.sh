#!/usr/bin/env bash
# validate-skills.sh
# Validates the frontmatter of every skills/<phase>/SKILL.md:
#   - file exists and has YAML frontmatter fenced by ---
#   - `name` field present and matches the directory name
#   - `description` field present, non-empty, and within reasonable length
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

validate_skill() {
  local skill_file="$1"
  local skill_dir
  skill_dir="$(dirname "$skill_file")"
  local expected_name
  expected_name="$(basename "$skill_dir")"
  local rel_path="${skill_file#"$REPO_ROOT/"}"

  checked=$((checked + 1))

  # Must start with frontmatter fence
  local first_line
  first_line="$(head -n 1 "$skill_file")"
  if [ "$first_line" != "---" ]; then
    fail "$rel_path: missing YAML frontmatter (first line is not '---')"
    return
  fi

  # Extract frontmatter between the first two --- markers
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

  # Extract a top-level scalar field value, supporting:
  #   key: value                (inline)
  #   key: >                    (folded block scalar)
  #     continuation lines
  #   key: |                    (literal block scalar)
  #     continuation lines
  # Continuation lines are any lines indented more than column 0 until the
  # next top-level key (non-indented) or the end of the frontmatter.
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
}

while IFS= read -r -d '' skill_file; do
  validate_skill "$skill_file"
done < <(find "$SKILLS_DIR" -mindepth 2 -maxdepth 2 -name 'SKILL.md' -print0 | sort -z)

# Also verify every skill directory has a SKILL.md
while IFS= read -r -d '' skill_dir; do
  if [ ! -f "$skill_dir/SKILL.md" ]; then
    rel="${skill_dir#"$REPO_ROOT/"}"
    fail "$rel: directory has no SKILL.md"
  fi
done < <(find "$SKILLS_DIR" -mindepth 1 -maxdepth 1 -type d -print0 | sort -z)

echo ""
echo "Checked $checked skill file(s); $failures failure(s)."

if [ "$failures" -gt 0 ]; then
  exit 1
fi
