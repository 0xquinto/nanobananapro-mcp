#!/usr/bin/env bash
# Nano Banana Pro — Hook installer
# Copies the best-practices hook to the current project's .claude/hooks/
# and registers it in .claude/settings.local.json.
#
# Usage:
#   Run from the TARGET project directory (not the nanobananapro-mcp repo):
#   /path/to/nanobananapro-mcp/scripts/install-hook.sh            # install
#   /path/to/nanobananapro-mcp/scripts/install-hook.sh --uninstall # remove

set -euo pipefail

PROJECT_DIR="$(pwd)"
HOOK_DIR="$PROJECT_DIR/.claude/hooks"
SETTINGS_FILE="$PROJECT_DIR/.claude/settings.local.json"
HOOK_SCRIPT="inject-best-practices.sh"
CHEATSHEET="NBP_CHEATSHEET.md"
HOOK_COMMAND="\"\$CLAUDE_PROJECT_DIR\"/.claude/hooks/$HOOK_SCRIPT"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/../hooks"

# ── helpers ──────────────────────────────────────────────────────────────────

ensure_jq() {
  if ! command -v jq &>/dev/null; then
    echo "Error: jq is required but not installed." >&2
    echo "  brew install jq  OR  apt-get install jq" >&2
    exit 1
  fi
}

add_hook_to_settings() {
  local hook_command_escaped
  hook_command_escaped='"\\"\\$CLAUDE_PROJECT_DIR\\"/.claude/hooks/inject-best-practices.sh"'

  if [ ! -f "$SETTINGS_FILE" ]; then
    mkdir -p "$(dirname "$SETTINGS_FILE")"
    echo '{}' > "$SETTINGS_FILE"
  fi

  local current
  current=$(cat "$SETTINGS_FILE")

  # Check if the hook is already registered
  if echo "$current" | jq -e '.hooks.UserPromptSubmit[]? | select(.hooks[]?.command | contains("inject-best-practices"))' &>/dev/null; then
    echo "Hook already registered in $SETTINGS_FILE"
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

  echo "$updated" > "$SETTINGS_FILE"
  echo "Registered hook in $SETTINGS_FILE"
}

remove_hook_from_settings() {
  if [ ! -f "$SETTINGS_FILE" ]; then
    echo "No settings file found at $SETTINGS_FILE"
    return
  fi

  local current
  current=$(cat "$SETTINGS_FILE")

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

  echo "$updated" > "$SETTINGS_FILE"
  echo "Removed hook from $SETTINGS_FILE"
}

# ── install ──────────────────────────────────────────────────────────────────

install() {
  ensure_jq

  if [ ! -f "$SOURCE_DIR/$HOOK_SCRIPT" ]; then
    echo "Error: $SOURCE_DIR/$HOOK_SCRIPT not found." >&2
    echo "Run this script using the full path to nanobananapro-mcp/scripts/install-hook.sh" >&2
    exit 1
  fi

  mkdir -p "$HOOK_DIR"
  cp "$SOURCE_DIR/$HOOK_SCRIPT" "$HOOK_DIR/$HOOK_SCRIPT"
  cp "$SOURCE_DIR/$CHEATSHEET" "$HOOK_DIR/$CHEATSHEET"
  chmod +x "$HOOK_DIR/$HOOK_SCRIPT"

  echo "Copied $HOOK_SCRIPT and $CHEATSHEET to $HOOK_DIR/"

  add_hook_to_settings

  echo ""
  echo "Done! The NBP best-practices hook is now active for $PROJECT_DIR"
  echo "It will inject prompting guidance when your prompts mention image generation."
}

# ── uninstall ────────────────────────────────────────────────────────────────

uninstall() {
  ensure_jq

  rm -f "$HOOK_DIR/$HOOK_SCRIPT" "$HOOK_DIR/$CHEATSHEET"
  echo "Removed $HOOK_SCRIPT and $CHEATSHEET from $HOOK_DIR/"

  remove_hook_from_settings

  echo ""
  echo "Done! The NBP best-practices hook has been removed from $PROJECT_DIR"
}

# ── main ─────────────────────────────────────────────────────────────────────

case "${1:-}" in
  --uninstall)
    uninstall
    ;;
  *)
    install
    ;;
esac
