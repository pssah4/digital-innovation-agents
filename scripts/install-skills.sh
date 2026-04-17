#!/usr/bin/env bash
# install-skills.sh
# Installs Digital Innovation Agents skills into ~/.claude/skills/
# (or a custom target directory).
#
# Usage:
#   ./install-skills.sh                       Install from the current checkout
#   ./install-skills.sh --version v1.0.0      Install a specific release tag
#   ./install-skills.sh --target DIR          Install into DIR instead of ~/.claude/skills
#   ./install-skills.sh --dry-run             Show what would happen, change nothing
#   ./install-skills.sh --yes                 Do not ask before overwriting existing skills
#   ./install-skills.sh --no-backup           Skip the automatic backup of existing skills
#   ./install-skills.sh --quiet               Suppress informational output (errors still print)
#   ./install-skills.sh --help                Show this help
#
# Exit codes:
#   0  success (or dry-run completed)
#   1  fatal error (missing dependency, IO failure, validation failure)
#   2  user cancelled at confirmation prompt

set -euo pipefail

# -------- configuration ----------------------------------------------------

DEFAULT_SKILLS_DIR="${HOME:-}/.claude/skills"
REPO_URL="https://github.com/pssah4/digital-innovation-agents.git"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Fixed skill inventory. Keep in sync with the skills/ directory.
SKILLS=(
  "project-conventions"
  "reverse-engineering"
  "business-analyse"
  "requirements-engineering"
  "architecture"
  "coding"
  "testing"
  "security-audit"
  "v-model-workflow"
  "using-digital-innovation-agents"
)

# -------- argument parsing -------------------------------------------------

VERSION=""
TARGET_DIR=""
DRY_RUN=0
ASSUME_YES=0
DO_BACKUP=1
QUIET=0

usage() {
  sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'
}

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
    --target)
      if [ $# -lt 2 ] || [[ "$2" == --* ]]; then
        echo "ERROR: --target requires a directory argument" >&2
        exit 1
      fi
      TARGET_DIR="$2"
      shift 2
      ;;
    --dry-run|-n)
      DRY_RUN=1
      shift
      ;;
    --yes|-y)
      ASSUME_YES=1
      shift
      ;;
    --no-backup)
      DO_BACKUP=0
      shift
      ;;
    --quiet|-q)
      QUIET=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      echo "Run with --help for usage." >&2
      exit 1
      ;;
  esac
done

# -------- logging helpers --------------------------------------------------

log() {
  if [ "$QUIET" -eq 0 ]; then
    echo "$@"
  fi
}

err() {
  echo "$@" >&2
}

run() {
  # Execute or (in dry-run) announce a command
  if [ "$DRY_RUN" -eq 1 ]; then
    log "  [dry-run] $*"
  else
    "$@"
  fi
}

# -------- preflight checks -------------------------------------------------

if [ -z "${HOME:-}" ] && [ -z "$TARGET_DIR" ]; then
  err "ERROR: \$HOME is not set and --target was not supplied."
  err "       Either set HOME or pass --target /path/to/skills"
  exit 1
fi

SKILLS_DIR="${TARGET_DIR:-$DEFAULT_SKILLS_DIR}"

if [ -n "$VERSION" ] && ! command -v git >/dev/null 2>&1; then
  err "ERROR: --version requires 'git' on PATH, but git was not found."
  exit 1
fi

# macOS Git Bash / WSL note
case "${OSTYPE:-}" in
  msys*|cygwin*|win32)
    log "NOTE: Detected Windows-like shell. Make sure \$HOME points at the"
    log "      location Claude Code reads skills from on your setup."
    ;;
esac

# -------- resolve source ---------------------------------------------------

log "=== Digital Innovation Agents -- Skill Installer ==="
log ""
if [ "$DRY_RUN" -eq 1 ]; then
  log "(dry-run mode: no files will be changed)"
  log ""
fi

CLEANUP_TMP=""
cleanup() {
  if [ -n "$CLEANUP_TMP" ] && [ -d "$CLEANUP_TMP" ]; then
    rm -rf "$CLEANUP_TMP"
  fi
}
trap cleanup EXIT

if [ -n "$VERSION" ]; then
  CLEANUP_TMP="$(mktemp -d 2>/dev/null || mktemp -d -t 'dia-install')"
  log "Fetching release $VERSION from remote ..."
  if ! git clone --quiet --depth 1 --branch "$VERSION" "$REPO_URL" "$CLEANUP_TMP/repo" 2>/dev/null; then
    err "ERROR: Could not fetch tag/branch '$VERSION' from $REPO_URL"
    err "       List available releases: gh release list --repo pssah4/digital-innovation-agents"
    exit 1
  fi
  # v2+ has skills/, v1 has claude-code-skills/
  if [ -d "$CLEANUP_TMP/repo/skills" ]; then
    SOURCE_DIR="$CLEANUP_TMP/repo/skills"
  elif [ -d "$CLEANUP_TMP/repo/claude-code-skills" ]; then
    SOURCE_DIR="$CLEANUP_TMP/repo/claude-code-skills"
  else
    err "ERROR: Neither skills/ nor claude-code-skills/ found in $VERSION"
    exit 1
  fi
  log "Source:  release $VERSION ($(basename "$SOURCE_DIR")/)"
else
  SOURCE_DIR="$REPO_ROOT/skills"
  if [ ! -d "$SOURCE_DIR" ]; then
    err "ERROR: $SOURCE_DIR not found. Run from a checkout with a skills/ directory,"
    err "       or pass --version <tag> to install a released snapshot."
    exit 1
  fi
  log "Source:  current checkout (development mode)"
fi

log "Target:  $SKILLS_DIR"
log ""

# -------- plan phase: classify each skill ---------------------------------

declare -a PLAN_NEW=()
declare -a PLAN_UPDATE=()
declare -a PLAN_MISSING=()

for skill in "${SKILLS[@]}"; do
  src="$SOURCE_DIR/$skill"
  dest="$SKILLS_DIR/$skill"

  if [ ! -d "$src" ]; then
    PLAN_MISSING+=("$skill")
    continue
  fi

  if [ -d "$dest" ]; then
    PLAN_UPDATE+=("$skill")
  else
    PLAN_NEW+=("$skill")
  fi
done

if [ "${#PLAN_NEW[@]}" -gt 0 ]; then
  log "Will install (new): ${PLAN_NEW[*]}"
fi
if [ "${#PLAN_UPDATE[@]}" -gt 0 ]; then
  log "Will update (overwrite): ${PLAN_UPDATE[*]}"
fi
if [ "${#PLAN_MISSING[@]}" -gt 0 ]; then
  log "Not in source (skipped): ${PLAN_MISSING[*]}"
fi
log ""

# -------- confirmation -----------------------------------------------------

if [ "$DRY_RUN" -eq 0 ] && [ "$ASSUME_YES" -eq 0 ] && [ "${#PLAN_UPDATE[@]}" -gt 0 ]; then
  # Ask only if we're overwriting something the user already has.
  # Prefer stdin if it's a TTY; otherwise try /dev/tty (for curl | bash);
  # otherwise refuse to guess and tell the user how to proceed.
  prompt="Overwrite ${#PLAN_UPDATE[@]} existing skill(s) in $SKILLS_DIR? [y/N] "
  ans=""
  got_answer=0

  # Probe whether /dev/tty is actually usable without printing any noise
  # from the shell's own redirection machinery.
  tty_usable=0
  if (exec </dev/tty) 2>/dev/null; then
    tty_usable=1
  fi

  if [ -t 0 ]; then
    read -r -p "$prompt" ans || ans=""
    got_answer=1
  elif [ "$tty_usable" -eq 1 ]; then
    if read -r -p "$prompt" ans </dev/tty; then
      got_answer=1
    fi
  fi

  if [ "$got_answer" -eq 0 ]; then
    err "ERROR: no interactive TTY available to confirm the overwrite."
    err "       Re-run with --yes to confirm, or --dry-run to preview."
    exit 1
  fi

  case "${ans:-}" in
    y|Y|yes|YES)
      ;;
    *)
      log "Aborted by user."
      exit 2
      ;;
  esac
fi

# -------- ensure target dir ------------------------------------------------

if [ ! -d "$SKILLS_DIR" ]; then
  log "Creating $SKILLS_DIR"
  run mkdir -p "$SKILLS_DIR"
fi

# -------- backup existing skills ------------------------------------------

if [ "$DO_BACKUP" -eq 1 ] && [ "${#PLAN_UPDATE[@]}" -gt 0 ]; then
  BACKUP_DIR="${SKILLS_DIR}.backup-$(date +%Y%m%d-%H%M%S)"
  log "Backing up existing skills to: $BACKUP_DIR"
  run mkdir -p "$BACKUP_DIR"
  if [ "$DRY_RUN" -eq 0 ]; then
    for skill in "${PLAN_UPDATE[@]}"; do
      run cp -R "$SKILLS_DIR/$skill" "$BACKUP_DIR/"
    done
  fi
fi

# -------- install ----------------------------------------------------------
# Note: "${arr[@]}" fails with set -u on bash 3.2 when arr is empty, so we
# guard each loop with a length check.

if [ "${#PLAN_NEW[@]}" -gt 0 ]; then
  for skill in "${PLAN_NEW[@]}"; do
    log "  [NEW]    $skill"
    run cp -R "$SOURCE_DIR/$skill" "$SKILLS_DIR/$skill"
  done
fi

if [ "${#PLAN_UPDATE[@]}" -gt 0 ]; then
  for skill in "${PLAN_UPDATE[@]}"; do
    log "  [UPDATE] $skill"
    run rm -rf "$SKILLS_DIR/$skill"
    run cp -R "$SOURCE_DIR/$skill" "$SKILLS_DIR/$skill"
  done
fi

if [ "${#PLAN_MISSING[@]}" -gt 0 ]; then
  for skill in "${PLAN_MISSING[@]}"; do
    log "  [SKIP]   $skill (not in source)"
  done
fi

# -------- verify -----------------------------------------------------------

if [ "$DRY_RUN" -eq 0 ]; then
  log ""
  log "Verifying installation ..."
  verify_failed=0
  verify_count=0
  installed=()
  if [ "${#PLAN_NEW[@]}" -gt 0 ]; then
    installed+=("${PLAN_NEW[@]}")
  fi
  if [ "${#PLAN_UPDATE[@]}" -gt 0 ]; then
    installed+=("${PLAN_UPDATE[@]}")
  fi
  if [ "${#installed[@]}" -gt 0 ]; then
    for skill in "${installed[@]}"; do
      verify_count=$((verify_count + 1))
      if [ ! -f "$SKILLS_DIR/$skill/SKILL.md" ]; then
        err "  VERIFY FAIL: $skill is missing SKILL.md"
        verify_failed=1
      fi
    done
  fi
  if [ "$verify_failed" -ne 0 ]; then
    err "ERROR: post-install verification failed."
    exit 1
  fi
  if [ "$verify_count" -gt 0 ]; then
    log "  OK — all $verify_count installed skill(s) contain a SKILL.md"
  else
    log "  (nothing to verify)"
  fi
fi

# -------- summary ----------------------------------------------------------

log ""
log "=== Installation complete ==="
log ""

if [ "$DRY_RUN" -eq 0 ]; then
  log "Installed skills:"
  for skill in "${SKILLS[@]}"; do
    if [ -d "$SKILLS_DIR/$skill" ]; then
      log "  /$skill"
    fi
  done
  log ""
fi

log "Usage in Claude Code:"
log "  /v-model-workflow          -- Orchestrator for the full cycle"
log "  /business-analyse          -- Structured problem analysis (Exploration/Ideation/Validation)"
log "  /requirements-engineering  -- Features, epics, success criteria"
log "  /architecture              -- ADRs, arc42, plan-context.md"
log "  /coding                    -- Context handoff from plan-context.md"
log "  /testing                   -- Unit & integration tests"
log "  /security-audit            -- Security review after implementation"
log "  /project-conventions       -- Project structure & naming conventions"
log ""
log "Verify: Open Claude Code and type / -- skills should appear in autocomplete."
log ""
log "Note: For v2, the recommended installation is via plugin marketplace."
log "      See README.md for Claude Code, Cursor, Codex, OpenCode, Gemini CLI."
