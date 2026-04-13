#!/bin/bash
# install-skills.sh
# Installs Digital Innovation Agents skills to ~/.claude/skills/
#
# Usage:
#   ./install-skills.sh                    Install from current directory
#   ./install-skills.sh --version v1.0.0   Install specific release tag
#   ./install-skills.sh --help             Show this help

set -euo pipefail

SKILLS_DIR="$HOME/.claude/skills"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_URL="https://github.com/pssah4/digital-innovation-agents.git"
VERSION=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --version)
      if [ $# -lt 2 ] || [[ "$2" == --* ]]; then
        echo "ERROR: --version requires a tag argument (e.g. --version v1.0.0)" >&2
        exit 1
      fi
      VERSION="$2"
      shift 2
      ;;
    --help|-h)
      cat <<EOF
Usage:
  ./install-skills.sh                    Install from current directory
  ./install-skills.sh --version v1.0.0   Install specific release tag
  ./install-skills.sh --help             Show this help

Available releases: https://github.com/pssah4/digital-innovation-agents/releases
EOF
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      echo "Run with --help for usage." >&2
      exit 1
      ;;
  esac
done

echo "=== Digital Innovation Agents -- Skill Installer ==="
echo ""

if [ -n "$VERSION" ]; then
  TMPDIR=$(mktemp -d)
  trap 'rm -rf "$TMPDIR"' EXIT
  echo "Fetching release $VERSION from remote..."
  if ! git clone --quiet --depth 1 --branch "$VERSION" "$REPO_URL" "$TMPDIR/repo" 2>/dev/null; then
    echo "ERROR: Could not fetch tag/branch '$VERSION' from $REPO_URL" >&2
    echo "       Check: gh release list --repo pssah4/digital-innovation-agents" >&2
    exit 1
  fi
  SOURCE_DIR="$TMPDIR/repo/claude-code-skills"
  echo "Source:  release $VERSION"
else
  SOURCE_DIR="$SCRIPT_DIR"
  echo "Source:  current directory (development mode)"
fi

echo "Target:  $SKILLS_DIR"
echo ""

# Create directory if needed
mkdir -p "$SKILLS_DIR"

# Skills to install
SKILLS=(
  "project-conventions"
  "business-analyse"
  "requirements-engineering"
  "architecture"
  "coding"
  "testing"
  "security-audit"
  "v-model-workflow"
)

for skill in "${SKILLS[@]}"; do
  src="$SOURCE_DIR/$skill"
  dest="$SKILLS_DIR/$skill"

  if [ ! -d "$src" ]; then
    echo "  [SKIP]   $skill (not found in source)"
    continue
  fi

  if [ -d "$dest" ]; then
    echo "  [UPDATE] $skill (exists, will be overwritten)"
    rm -rf "$dest"
  else
    echo "  [NEW]    $skill"
  fi

  cp -r "$src" "$dest"
done

echo ""
echo "=== Installation complete ==="
echo ""
echo "Installed skills:"
for skill in "${SKILLS[@]}"; do
  echo "  /$skill"
done
echo ""
echo "Usage in Claude Code:"
echo "  /business-analyse          -- Structured problem analysis (Exploration/Ideation/Validation)"
echo "  /requirements-engineering  -- Features, epics, success criteria"
echo "  /architecture              -- ADRs, arc42, plan-context.md"
echo "  /coding                    -- Context handoff from plan-context.md"
echo "  /testing                   -- Unit & integration tests"
echo "  /security-audit            -- Security review after implementation"
echo "  /project-conventions       -- Project structure & naming conventions"
echo "  /v-model-workflow          -- Orchestrator for the full cycle"
echo ""
echo "Verify: Open Claude Code and type / -- skills should appear in autocomplete."
