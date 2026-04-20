#!/usr/bin/env bash
# V-Model Graph Viewer Launcher.
# Parst die Markdown-Artefakte unter <root> (default .) und oeffnet
# den HTML-Viewer mit dem Graph als URL-Parameter.
#
# Aufruf:
#   bash open-graph.sh [<project-root>]
#
# Oeffnet den Viewer im default Browser. JSON wird in-memory
# uebergeben, kein persistierter Export.
set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT="${1:-.}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 nicht gefunden. Bitte Python 3 installieren." >&2
  exit 1
fi

# JSON generieren
JSON=$(python3 "$SCRIPT_DIR/parse-graph.py" "$ROOT")

# Base64 encode fuer URL-Parameter (standard base64, URL-encoded)
ENCODED=$(printf '%s' "$JSON" | base64 | tr -d '\n')
ENCODED=$(python3 -c "import sys, urllib.parse; print(urllib.parse.quote(sys.stdin.read()))" <<< "$ENCODED")

VIEWER="file://$SCRIPT_DIR/graph-viewer.html?data=$ENCODED"

# Viewer oeffnen
if command -v open >/dev/null 2>&1; then
  open "$VIEWER"
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$VIEWER"
else
  echo "Kein Browser-Opener gefunden. Oeffne diese URL manuell:" >&2
  echo "$VIEWER"
  exit 0
fi

# Auch Pfad zum manuellen Oeffnen ausgeben
echo "Viewer geoeffnet. URL (falls Browser nicht automatisch aufging):"
echo "$VIEWER"
