#!/usr/bin/env bash
# hack2win multi-agent installer (macOS / Linux / Git Bash)
# Usage:
#   ./install.sh              # global install (auto-detect agents)
#   ./install.sh --project    # additionally wire rules into the CURRENT project
#   ./install.sh -u           # uninstall everything this script created
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="hack2win"
MARK_BEGIN="# >>> hack2win >>>"
MARK_END="# <<< hack2win <<<"
MODE="global"; PROJECT_DIR=""
for arg in "$@"; do
  case "$arg" in
    --project) MODE="project" ;;
    -u|--uninstall) MODE="uninstall" ;;
    *) echo "unknown flag: $arg (supported: --project, -u)"; exit 2 ;;
  esac
done

copy_skill() { # $1 = the agent's skills root dir (already named skills/ or skill/)
  local dest="$1/$SKILL_NAME"
  mkdir -p "$dest"
  # tar-based copy preserves structure and excludes .git and the installers themselves
  rm -rf "$dest"; mkdir -p "$dest"
  (cd "$SRC" && tar --exclude='./.git' --exclude='./install.sh' --exclude='./install.ps1' -cf - .) | (cd "$dest" && tar -xf -)
  echo "  [ok] $dest"
}

remove_dir_if_managed() { # $1 = skill dir
  if [ -f "$1/SKILL.md" ]; then rm -rf "$1"; echo "  [removed] $1"; fi
}

strip_block() { # $1 = file with managed block
  [ -f "$1" ] || return 0
  if grep -qF "$MARK_BEGIN" "$1"; then
    sed -i.bak "/$MARK_BEGIN/,/$MARK_END/d" "$1" && rm -f "$1.bak"
    echo "  [cleaned] $1"
  fi
}

append_block() { # $1 = target file, $2 = block file
  local target="$1" block="$2"
  [ -f "$target" ] && grep -qF "$MARK_BEGIN" "$target" && { echo "  [skip] $target (already wired)"; return 0; }
  mkdir -p "$(dirname "$target")"
  { echo ""; cat "$SRC/adapters/codex-AGENTS-block.md" | sed "1s@^@$MARK_BEGIN@"; echo "$MARK_END"; } >> "$target"
  echo "  [wired] $target"
}

echo "hack2win installer — mode: $MODE"

if [ "$MODE" = "uninstall" ]; then
  echo "Uninstalling:"
  [ -d "$HOME/.agents" ]     && remove_dir_if_managed "$HOME/.agents/skills/$SKILL_NAME"
  [ -d "$HOME/.claude" ]     && remove_dir_if_managed "$HOME/.claude/skills/$SKILL_NAME"
  [ -d "$HOME/.codex" ]      && remove_dir_if_managed "$HOME/.codex/skills/$SKILL_NAME"; strip_block "$HOME/.codex/AGENTS.md"; rm -f "$HOME/.codex/prompts/$SKILL_NAME.md"
  [ -d "$HOME/.zcode" ]      && remove_dir_if_managed "$HOME/.zcode/skills/$SKILL_NAME"
  [ -d "$HOME/.config/opencode" ] && remove_dir_if_managed "$HOME/.config/opencode/skill/$SKILL_NAME"
  echo "Done. (project-level rules, if any, remove manually: .cursor/rules/hack2win.mdc, .windsurf/rules/hack2win.md)"
  exit 0
fi

echo "Global install (canonical ~/.agents + any detected agents):"
copy_skill "$HOME/.agents/skills"
[ -d "$HOME/.claude" ] && { echo "Claude Code detected:"; copy_skill "$HOME/.claude/skills"; }
if [ -d "$HOME/.codex" ]; then
  echo "Codex detected:"
  copy_skill "$HOME/.codex/skills"
  append_block "$HOME/.codex/AGENTS.md" "adapters/codex-AGENTS-block.md"
  mkdir -p "$HOME/.codex/prompts"
  cp "$SRC/adapters/codex-AGENTS-block.md" "$HOME/.codex/prompts/$SKILL_NAME.md"
  echo "  [wired] ~/.codex/prompts/$SKILL_NAME.md (use: /$SKILL_NAME)"
fi
[ -d "$HOME/.zcode" ] && { echo "ZCode detected:"; copy_skill "$HOME/.zcode/skills"; }
[ -d "$HOME/.config/opencode" ] && { echo "OpenCode detected:"; copy_skill "$HOME/.config/opencode/skill"; }

if [ "$MODE" = "project" ]; then
  PROJECT_DIR="$(pwd)"
  echo "Project wiring in: $PROJECT_DIR"
  cp "$SRC/AGENTS.md" "$PROJECT_DIR/AGENTS.md"; echo "  [wired] AGENTS.md (Codex & agents.md tools)"
  mkdir -p "$PROJECT_DIR/.cursor/rules";   cp "$SRC/adapters/cursor.mdc"   "$PROJECT_DIR/.cursor/rules/$SKILL_NAME.mdc";  echo "  [wired] .cursor/rules/$SKILL_NAME.mdc"
  mkdir -p "$PROJECT_DIR/.windsurf/rules"; cp "$SRC/adapters/windsurf.md"  "$PROJECT_DIR/.windsurf/rules/$SKILL_NAME.md"; echo "  [wired] .windsurf/rules/$SKILL_NAME.md"
  mkdir -p "$PROJECT_DIR/.github"
  COPILOT="$PROJECT_DIR/.github/copilot-instructions.md"
  if [ -f "$COPILOT" ] && grep -qF "$MARK_BEGIN" "$COPILOT"; then echo "  [skip] $COPILOT (already wired)";
  else { echo ""; echo "$MARK_BEGIN"; cat "$SRC/adapters/copilot.md"; echo "$MARK_END"; } >> "$COPILOT"; echo "  [wired] $COPILOT"; fi
fi

echo "Verify: python \"$HOME/.agents/skills/$SKILL_NAME/scripts/list_skills.py\""
echo "Done."
