#!/usr/bin/env bash
# Hook: PreToolUse (Edit|Write)
# Purpose: Block edits to style-guide.md when locked
# Exit 0: Allow edit
# Exit 2: Block edit (locked)

set -euo pipefail

# Read JSON from stdin
json=$(cat)

# Extract file path from tool input
file_path=$(echo "$json" | jq -r '.tool_input.file_path // ""')

# Only check style-guide.md files
if [[ ! "$file_path" =~ style-guide\.md$ ]]; then
  exit 0
fi

# Check if the style guide exists and has a locked header
if [[ -f "$file_path" ]]; then
  # Extract locked status from YAML frontmatter
  locked=$(head -20 "$file_path" | grep -E "^locked:\s*true" || true)

  if [[ -n "$locked" ]]; then
    echo "BLOCKED: style-guide.md is locked." >&2
    echo "Use '/project-setup --unlock' to unlock for editing." >&2
    exit 2
  fi
fi

exit 0
