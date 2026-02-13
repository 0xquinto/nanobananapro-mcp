#!/usr/bin/env bash
# Nano Banana Pro — Hook installer
# Copies the best-practices hook to the current project's .claude/hooks/
# and registers it in .claude/settings.local.json.
#
# Usage:
#   Run from the TARGET project directory (not the nanobananapro-mcp repo):
#   /path/to/nanobananapro-mcp/scripts/install-hook.sh                    # install
#   /path/to/nanobananapro-mcp/scripts/install-hook.sh --uninstall       # remove from project
#   /path/to/nanobananapro-mcp/scripts/install-hook.sh --uninstall-global # remove from ~/.claude/

set -euo pipefail

PROJECT_DIR="$(pwd)"
HOOK_SCRIPT="inject-best-practices.sh"
CHEATSHEET="NBP_CHEATSHEET.md"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/../hooks"

GLOBAL_HOOK_DIR="$HOME/.claude/hooks"
GLOBAL_SETTINGS="$HOME/.claude/settings.json"
PROJECT_HOOK_DIR="$PROJECT_DIR/.claude/hooks"
PROJECT_SETTINGS="$PROJECT_DIR/.claude/settings.local.json"

# ── helpers ──────────────────────────────────────────────────────────────────

ensure_jq() {
  if ! command -v jq &>/dev/null; then
    echo "Error: jq is required but not installed." >&2
    echo "  brew install jq  OR  apt-get install jq" >&2
    exit 1
  fi
}

add_hook_to_settings() {
  local settings_file="$1"

  if [ ! -f "$settings_file" ]; then
    mkdir -p "$(dirname "$settings_file")"
    echo '{}' > "$settings_file"
  fi

  local current
  current=$(cat "$settings_file")

  # Check if the hook is already registered
  if echo "$current" | jq -e '.hooks.UserPromptSubmit[]? | select(.hooks[]?.command | contains("inject-best-practices"))' &>/dev/null; then
    echo "Hook already registered in $settings_file"
    return
  fi

  # Add the hook entry to UserPromptSubmit array
  local updated
  updated=$(echo "$current" | jq '
    .hooks //= {} |
    .hooks.UserPromptSubmit //= [] |
    .hooks.UserPromptSubmit += [{
      "hooks": [{
        "type": "command",
        "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/inject-best-practices.sh"
      }]
    }]
  ')

  echo "$updated" > "$settings_file"
  echo "Registered hook in $settings_file"
}

remove_hook_from_settings() {
  local settings_file="$1"

  if [ ! -f "$settings_file" ]; then
    echo "No settings file found at $settings_file"
    return
  fi

  local current
  current=$(cat "$settings_file")

  # Check if there's anything to remove
  if ! echo "$current" | jq -e '.hooks.UserPromptSubmit[]? | select(.hooks[]?.command | contains("inject-best-practices"))' &>/dev/null; then
    echo "No NBP hook found in $settings_file"
    return
  fi

  # Remove entries whose hooks contain our script
  local updated
  updated=$(echo "$current" | jq '
    if .hooks.UserPromptSubmit then
      .hooks.UserPromptSubmit |= map(
        select(.hooks | all(.command | contains("inject-best-practices") | not))
      ) |
      if .hooks.UserPromptSubmit == [] then del(.hooks.UserPromptSubmit) else . end |
      if .hooks == {} then del(.hooks) else . end
    else . end
  ')

  echo "$updated" > "$settings_file"
  echo "Removed hook from $settings_file"
}

# ── install ──────────────────────────────────────────────────────────────────

install() {
  ensure_jq

  if [ ! -f "$SOURCE_DIR/$HOOK_SCRIPT" ]; then
    echo "Error: $SOURCE_DIR/$HOOK_SCRIPT not found." >&2
    echo "Run this script using the full path to nanobananapro-mcp/scripts/install-hook.sh" >&2
    exit 1
  fi

  mkdir -p "$PROJECT_HOOK_DIR"
  cp "$SOURCE_DIR/$HOOK_SCRIPT" "$PROJECT_HOOK_DIR/$HOOK_SCRIPT"
  cp "$SOURCE_DIR/$CHEATSHEET" "$PROJECT_HOOK_DIR/$CHEATSHEET"
  chmod +x "$PROJECT_HOOK_DIR/$HOOK_SCRIPT"

  echo "Copied $HOOK_SCRIPT and $CHEATSHEET to $PROJECT_HOOK_DIR/"

  add_hook_to_settings "$PROJECT_SETTINGS"

  # Clean up stale global install if present
  cleanup_global silent

  echo ""
  echo "Done! The NBP best-practices hook is now active for $PROJECT_DIR"
  echo "It will inject prompting guidance when your prompts mention image generation."
}

# ── uninstall ────────────────────────────────────────────────────────────────

uninstall() {
  ensure_jq

  rm -f "$PROJECT_HOOK_DIR/$HOOK_SCRIPT" "$PROJECT_HOOK_DIR/$CHEATSHEET"
  echo "Removed $HOOK_SCRIPT and $CHEATSHEET from $PROJECT_HOOK_DIR/"

  remove_hook_from_settings "$PROJECT_SETTINGS"

  echo ""
  echo "Done! The NBP best-practices hook has been removed from $PROJECT_DIR"
}

# ── uninstall-global ─────────────────────────────────────────────────────────

cleanup_global() {
  local quiet="${1:-}"

  # Remove hook files from ~/.claude/hooks/
  if [ -f "$GLOBAL_HOOK_DIR/$HOOK_SCRIPT" ] || [ -f "$GLOBAL_HOOK_DIR/$CHEATSHEET" ]; then
    rm -f "$GLOBAL_HOOK_DIR/$HOOK_SCRIPT" "$GLOBAL_HOOK_DIR/$CHEATSHEET"
    echo "Removed $HOOK_SCRIPT and $CHEATSHEET from $GLOBAL_HOOK_DIR/"
  fi

  # Remove hook entry from ~/.claude/settings.json
  remove_hook_from_settings "$GLOBAL_SETTINGS"

  if [ "$quiet" != "silent" ]; then
    echo ""
    echo "Done! The NBP best-practices hook has been removed from global settings."
  fi
}

# ── main ─────────────────────────────────────────────────────────────────────

case "${1:-}" in
  --uninstall)
    uninstall
    ;;
  --uninstall-global)
    ensure_jq
    cleanup_global
    ;;
  *)
    install
    ;;
esac
