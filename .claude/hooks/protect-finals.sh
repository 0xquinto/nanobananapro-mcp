#!/usr/bin/env bash
# Hook: PreToolUse (Edit|Write)
# Purpose: Prevent modification of files in outputs/finals/
# Exit 0: Allow edit
# Exit 2: Block edit (protected)

set -euo pipefail

# Read JSON from stdin
json=$(cat)

# Extract file path from tool input
file_path=$(echo "$json" | jq -r '.tool_input.file_path // ""')

# Block edits to anything in outputs/finals/
if [[ "$file_path" =~ /outputs/finals/ ]]; then
  echo "BLOCKED: Files in outputs/finals/ are protected." >&2
  echo "Finals are immutable once approved. Copy to exploration/ to modify." >&2
  exit 2
fi

exit 0
