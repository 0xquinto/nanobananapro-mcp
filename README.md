# Nano Banana Pro MCP Server

MCP server for Google Gemini image generation models (Nano Banana / Nano Banana Pro) for use with Claude Code.

## Installation

```bash
# Clone and install
git clone <repo>
cd nanobananapro-mcp
uv sync
```

## Configuration

Set your Gemini API key:

```bash
export GEMINI_API_KEY=your-api-key
```

Get an API key from: https://aistudio.google.com/apikey

## Usage with Claude Code

```bash
# Add the server
claude mcp add nanobananapro -e GEMINI_API_KEY=$GEMINI_API_KEY -- uv run python -m nanobananapro_mcp

# List servers
claude mcp list

# Test a tool
claude mcp test nanobananapro generate_image --prompt "A sunset" --aspect_ratio "16:9"
```

## Available Tools

### generate_image
Generate images from text prompts.

### edit_image
Edit existing images with text instructions.

### compose_images
Combine multiple reference images into a new composition.

### search_grounded_image
Generate images using real-time Google Search data.

### start_image_chat / continue_image_chat / end_image_chat
Multi-turn conversational image editing.

## Models

| Alias | Model | Best For |
|-------|-------|----------|
| `flash` | gemini-2.5-flash-image | Fast generation, up to 3 input images |
| `pro` | gemini-3-pro-image-preview | High quality, up to 14 images, 4K, Google Search |

## Development

```bash
# Install dev dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Run with verbose logging
GEMINI_API_KEY=your-key uv run python -m nanobananapro_mcp
```

## License

MIT
