#!/usr/bin/env bash
# Nano Banana Pro — Hook installer
# Copies the best-practices hook to ~/.claude/hooks/ and registers it in settings.
#
# Usage:
#   scripts/install-hook.sh            # install
#   scripts/install-hook.sh --uninstall # remove

set -euo pipefail

HOOK_DIR="$HOME/.claude/hooks"
SETTINGS_FILE="$HOME/.claude/settings.json"
HOOK_SCRIPT="inject-best-practices.sh"
CHEATSHEET="NBP_CHEATSHEET.md"
HOOK_COMMAND="$HOOK_DIR/$HOOK_SCRIPT"
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
  local hook_entry
  hook_entry=$(cat <<'ENTRY'
{
  "hooks": [
    {
      "type": "command",
      "command": "HOOK_CMD_PLACEHOLDER"
    }
  ]
}
ENTRY
)
  hook_entry="${hook_entry//HOOK_CMD_PLACEHOLDER/$HOOK_COMMAND}"

  if [ ! -f "$SETTINGS_FILE" ]; then
    mkdir -p "$(dirname "$SETTINGS_FILE")"
    echo '{}' > "$SETTINGS_FILE"
  fi

  local current
  current=$(cat "$SETTINGS_FILE")

  # Check if the hook is already registered
  if echo "$current" | jq -e ".hooks.UserPromptSubmit[]? | select(.hooks[]?.command == \"$HOOK_COMMAND\")" &>/dev/null; then
    echo "Hook already registered in $SETTINGS_FILE"
    return
  fi

  # Add the hook entry to UserPromptSubmit array
  local updated
  updated=$(echo "$current" | jq --argjson entry "$hook_entry" '
    .hooks //= {} |
    .hooks.UserPromptSubmit //= [] |
    .hooks.UserPromptSubmit += [$entry]
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

  # Remove entries whose hooks contain our command
  local updated
  updated=$(echo "$current" | jq --arg cmd "$HOOK_COMMAND" '
    if .hooks.UserPromptSubmit then
      .hooks.UserPromptSubmit |= map(
        select(.hooks | all(.command != $cmd))
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
    echo "Run this script from the nanobananapro-mcp repo root." >&2
    exit 1
  fi

  mkdir -p "$HOOK_DIR"
  cp "$SOURCE_DIR/$HOOK_SCRIPT" "$HOOK_DIR/$HOOK_SCRIPT"
  cp "$SOURCE_DIR/$CHEATSHEET" "$HOOK_DIR/$CHEATSHEET"
  chmod +x "$HOOK_DIR/$HOOK_SCRIPT"

  echo "Copied $HOOK_SCRIPT and $CHEATSHEET to $HOOK_DIR/"

  add_hook_to_settings

  echo ""
  echo "Done! The NBP best-practices hook is now active."
  echo "It will inject prompting guidance when your prompts mention image generation."
}

# ── uninstall ────────────────────────────────────────────────────────────────

uninstall() {
  ensure_jq

  rm -f "$HOOK_DIR/$HOOK_SCRIPT" "$HOOK_DIR/$CHEATSHEET"
  echo "Removed $HOOK_SCRIPT and $CHEATSHEET from $HOOK_DIR/"

  remove_hook_from_settings

  echo ""
  echo "Done! The NBP best-practices hook has been removed."
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
