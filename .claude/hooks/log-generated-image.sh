#!/usr/bin/env bash
# Hook: PostToolUse (mcp__nanobananapro__generate_image|edit_image|compose_images)
# Purpose: Log generated images to asset-log.md
# Exit 0: Always (logging is non-blocking)

set -euo pipefail

# Read JSON from stdin
json=$(cat)

# Extract relevant fields
tool_name=$(echo "$json" | jq -r '.tool_name // "unknown"')
output_path=$(echo "$json" | jq -r '.tool_input.output_path // "N/A"')
prompt=$(echo "$json" | jq -r '.tool_input.prompt // "N/A"' | head -c 100)
seed=$(echo "$json" | jq -r '.tool_input.seed // "N/A"')
cwd=$(echo "$json" | jq -r '.cwd // "."')

# Find asset-log.md (walk up from cwd looking for project markers)
find_asset_log() {
  local dir="$1"
  while [[ "$dir" != "/" ]]; do
    if [[ -f "$dir/asset-log.md" ]]; then
      echo "$dir/asset-log.md"
      return 0
    fi
    # Check for project markers
    if [[ -f "$dir/style-guide.md" ]] || [[ -d "$dir/outputs" ]]; then
      # Project root found but no asset-log, create it
      echo "$dir/asset-log.md"
      return 0
    fi
    dir=$(dirname "$dir")
  done
  return 1
}

asset_log=$(find_asset_log "$cwd") || exit 0  # No project context, skip

# Create asset-log.md if missing
if [[ ! -f "$asset_log" ]]; then
  cat > "$asset_log" << 'EOF'
# Asset Log

| Date | Asset | Prompt Summary | Tool Used | Seed | Status | File |
|------|-------|----------------|-----------|------|--------|------|
EOF
fi

# Determine tool display name
case "$tool_name" in
  mcp__nanobananapro__generate_image) tool_display="generate" ;;
  mcp__nanobananapro__edit_image) tool_display="edit" ;;
  mcp__nanobananapro__compose_images) tool_display="compose" ;;
  *) tool_display="$tool_name" ;;
esac

# Format date
date_str=$(date +%Y-%m-%d)

# Truncate prompt for display
prompt_short=$(echo "$prompt" | tr '\n' ' ' | head -c 50)
[[ ${#prompt} -gt 50 ]] && prompt_short="${prompt_short}..."

# Extract filename from output_path
filename=$(basename "$output_path" 2>/dev/null || echo "N/A")

# Append to asset log
echo "| $date_str | $filename | $prompt_short | $tool_display | $seed | exploration | \`$output_path\` |" >> "$asset_log"

exit 0
