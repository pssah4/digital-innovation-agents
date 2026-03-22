#!/bin/bash
# install-skills.sh
# Installiert die V-Model Skills nach ~/.claude/skills/
#
# Usage: chmod +x install-skills.sh && ./install-skills.sh

set -euo pipefail

SKILLS_DIR="$HOME/.claude/skills"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== V-Model Skills Installer ==="
echo ""
echo "Ziel: $SKILLS_DIR"
echo ""

# Verzeichnis erstellen falls noetig
mkdir -p "$SKILLS_DIR"

# Skills die installiert werden
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
    echo "  [UPDATE] $skill (existiert bereits, wird ueberschrieben)"
    rm -rf "$dest"
  else
    echo "  [NEU]    $skill"
  fi

  cp -r "$src" "$dest"
done

echo ""
echo "=== Installation abgeschlossen ==="
echo ""
echo "Installierte Skills:"
for skill in "${SKILLS[@]}"; do
  echo "  /$skill"
done
echo ""
echo "Nutzung in Claude Code:"
echo "  /project-conventions       -- Projektstruktur & Namenskonventionen"
echo "  /business-analyse          -- Strukturierte Problem-Analyse"
echo "  /requirements-engineering  -- Features, Epics, Success Criteria"
echo "  /architecture              -- ADRs, arc42, plan-context.md"
echo "  /coding                    -- Kontext-Uebergabe aus plan-context.md"
echo "  /testing                   -- Unit & Integration Tests"
echo "  /security-audit            -- Security Review nach Implementierung"
echo "  /v-model-workflow          -- Orchestrator fuer den gesamten Zyklus"
echo ""
echo "Teste mit: claude und dann /skills eingeben"
