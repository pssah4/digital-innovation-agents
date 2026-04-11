#!/bin/bash
# install-skills.sh
# Installs V-Model Skills to ~/.claude/skills/
#
# Usage: chmod +x install-skills.sh && ./install-skills.sh

set -euo pipefail

SKILLS_DIR="$HOME/.claude/skills"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Digital Innovation Agents -- Skill Installer ==="
echo ""
echo "Target: $SKILLS_DIR"
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
  src="$SCRIPT_DIR/$skill"
  dest="$SKILLS_DIR/$skill"

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
