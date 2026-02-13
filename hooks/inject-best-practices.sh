#!/usr/bin/env bash
# Nano Banana Pro — UserPromptSubmit hook
# Injects the NBP cheatsheet into every prompt.
# Install via: scripts/install-hook.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cat "$SCRIPT_DIR/NBP_CHEATSHEET.md"

exit 0
