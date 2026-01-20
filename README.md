# Nano Banana Pro MCP Server

![Nano Banana Pro - South Park Style](assets/southpark-nanobananapro.png)

Local MCP server for Google Gemini image generation models (Nano Banana / Nano Banana Pro) for use with Claude Code. Designed for local deployment only.

## Installation

```bash
# Clone and install
git clone https://github.com/0xquinto/nanobananapro-mcp.git
cd nanobananapro-mcp
uv sync
```

## Configuration

Get a Gemini API key from: https://aistudio.google.com/apikey

## Usage with Claude Code

```bash
# Add the server (replace YOUR_API_KEY with your actual key)
claude mcp add nanobananapro -e GEMINI_API_KEY=YOUR_API_KEY -- uv run python -m nanobananapro_mcp

# List servers
claude mcp list

# Test a tool
claude mcp test nanobananapro generate_image --prompt "A sunset" --aspect_ratio "16:9"
```

## Available Tools

### generate_image

Generate images from text prompts.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | Yes | - | Text description of the image to generate |
| `model` | string | No | `gemini-2.5-flash-image` | Model to use (see Models section) |
| `aspect_ratio` | string | No | `1:1` | Output aspect ratio |
| `resolution` | string | No | `1K` | Output resolution (Pro only for 2K/4K) |
| `output_path` | string | No | None | Path to save the generated image |

### edit_image

Edit existing images with text instructions.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | Yes | - | Instructions for editing the image |
| `image_path` | string | Yes | - | Path to the input image file |
| `model` | string | No | `gemini-2.5-flash-image` | Model to use |
| `aspect_ratio` | string | No | None | Output aspect ratio (defaults to input) |
| `resolution` | string | No | `1K` | Output resolution |
| `output_path` | string | No | None | Path to save the edited image |

### compose_images

Combine multiple reference images into a new composition.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | Yes | - | Instructions for composing the images |
| `image_paths` | list[string] | Yes | - | Paths to input images (max 3 for Flash, 14 for Pro) |
| `model` | string | No | `gemini-3-pro-image-preview` | Model to use (Pro recommended) |
| `aspect_ratio` | string | No | `1:1` | Output aspect ratio |
| `resolution` | string | No | `2K` | Output resolution |
| `output_path` | string | No | None | Path to save the composed image |

### search_grounded_image

Generate images using real-time Google Search data. **Pro model only.**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | Yes | - | Description incorporating real-time data needs |
| `aspect_ratio` | string | No | `16:9` | Output aspect ratio |
| `resolution` | string | No | `2K` | Output resolution (1K, 2K, 4K) |
| `output_path` | string | No | None | Path to save the image |

### start_image_chat

Start a new multi-turn image editing session.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `initial_prompt` | string | Yes | - | First prompt to generate the initial image |
| `model` | string | No | `gemini-3-pro-image-preview` | Model to use for the session |

Returns a `session_id` for use with `continue_image_chat`.

### continue_image_chat

Continue an existing image chat session.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `session_id` | string | Yes | - | ID of the session to continue |
| `prompt` | string | Yes | - | Next instruction for image modification |
| `aspect_ratio` | string | No | None | Optional new aspect ratio |
| `resolution` | string | No | None | Optional new resolution |

### end_image_chat

End and clean up an image chat session.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `session_id` | string | Yes | - | ID of the session to end |

### list_chat_sessions

List all active chat sessions. No parameters.

## Models

| Alias | Full Model Name | Description |
|-------|-----------------|-------------|
| `flash` | `gemini-2.5-flash-image` | Fast generation |
| `pro` | `gemini-3-pro-image-preview` | High quality with advanced features |
| `nano-banana` | `gemini-2.5-flash-image` | Alias for flash |
| `nano-banana-pro` | `gemini-3-pro-image-preview` | Alias for pro |

### Model Capabilities

| Feature | Flash | Pro |
|---------|-------|-----|
| **Resolution** | 1K only | 1K, 2K, 4K |
| **Max Input Images** | 3 | 14 |
| **Google Search Grounding** | ❌ | ✅ |
| **Speed** | Faster | Slower |
| **Quality** | Good | Best |

### Valid Values

**Aspect Ratios**: `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

**Resolutions**: `1K`, `2K`, `4K` (Flash model silently downgrades to 1K)

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
