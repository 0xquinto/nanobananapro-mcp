#!/usr/bin/env bash
# Nano Banana Pro — UserPromptSubmit hook
# Detects image-related prompts and injects the NBP cheatsheet into context.
# Install via: scripts/install-hook.sh

PROMPT=$(jq -r '.prompt // ""' < /dev/stdin)

PATTERN="generate.*(image|photo|poster|illustration|graphic|banner|thumbnail|logo|icon|artwork|wallpaper|infographic)|edit.*(image|photo)|compose.*(image|photo)|compose.tool|photo|picture|poster|illustration|infographic|storyboard|sketch|nanobananapro|nano.banana|gemini.image|image.chat|image.generation|image.edit|compose.images|generate.image|edit.image|search.grounded|interleaved|4[Kk]|aspect.ratio|resolution"

if echo "$PROMPT" | grep -qiE "$PATTERN"; then
  SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
  cat "$SCRIPT_DIR/NBP_CHEATSHEET.md"
fi

exit 0
