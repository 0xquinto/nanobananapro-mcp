# Nano Banana Pro MCP Server

<p align="center">
  <img src="https://repository-images.githubusercontent.com/1138054882/f6434f72-1497-4161-9340-f33dcf592793" alt="Nano Banana Pro - Claude discovers the Golden Banana" width="600">
</p>

Local MCP server for Gemini 3 Pro image generation (Nano Banana Pro) for use with Claude Code. Designed for local deployment only.

## Installation

```bash
# Clone and install
git clone https://github.com/0xquinto/nanobananapro-mcp.git
cd nanobananapro-mcp
bun install
```

## Configuration

Get a Gemini API key from: https://aistudio.google.com/apikey

## Usage with Claude Code

```bash
# Add the server (replace YOUR_API_KEY with your actual key)
claude mcp add nanobananapro -e GEMINI_API_KEY=YOUR_API_KEY -- bun run /path/to/nanobananapro-mcp/src/index.ts

# List servers
claude mcp list

# Test a tool
claude mcp test nanobananapro generate_image --prompt "A sunset" --aspect_ratio "16:9"
```

### Using in Multiple Projects

By default, `claude mcp add` creates a **local** configuration that only works in the current project directory. To use nanobananapro across all your Claude Code projects:

```bash
# Add with user scope and specify the project directory
claude mcp add nanobananapro -s user \
  -e GEMINI_API_KEY=YOUR_API_KEY \
  -- bun run /path/to/nanobananapro-mcp/src/index.ts
```

**Troubleshooting: Server not connecting in other projects**

If you previously added the server with local scope, those configs shadow the user config. Remove them first:

```bash
# Check current scope
claude mcp get nanobananapro

# If it shows "Local config", remove it
claude mcp remove nanobananapro -s local

# Then add with user scope (see command above)
```

MCP config is stored in `~/.claude.json`. Local configs are nested under project paths; user configs are at the top level.

## Available Tools

### generate_image

Generate images from text prompts.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | Yes | - | Text description of the image to generate |
| `model` | string | No | `gemini-3-pro-image-preview` | Model to use (see Models section) |
| `aspect_ratio` | string | No | `1:1` | Output aspect ratio |
| `resolution` | string | No | `1K` | Output resolution (1K, 2K, 4K) |
| `output_path` | string | No | None | Path to save the generated image |
| `seed` | integer | No | None | Seed for reproducible generation (0 to 2147483647) |
| `safety` | string | No | None | Safety filter threshold (see Safety Settings) |

### edit_image

Edit existing images with text instructions.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | Yes | - | Instructions for editing the image |
| `image_path` | string | Yes | - | Path to the input image file |
| `model` | string | No | `gemini-3-pro-image-preview` | Model to use |
| `aspect_ratio` | string | No | None | Output aspect ratio (defaults to input) |
| `resolution` | string | No | `1K` | Output resolution (1K, 2K, 4K) |
| `output_path` | string | No | None | Path to save the edited image |
| `seed` | integer | No | None | Seed for reproducible generation |
| `safety` | string | No | None | Safety filter threshold (see Safety Settings) |

### compose_images

Combine multiple reference images into a new composition.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | Yes | - | Instructions for composing the images |
| `image_paths` | string[] | Yes | - | Paths to input images (max 14) |
| `model` | string | No | `gemini-3-pro-image-preview` | Model to use |
| `aspect_ratio` | string | No | `1:1` | Output aspect ratio |
| `resolution` | string | No | `2K` | Output resolution (1K, 2K, 4K) |
| `output_path` | string | No | None | Path to save the composed image |
| `seed` | integer | No | None | Seed for reproducible generation |
| `safety` | string | No | None | Safety filter threshold (see Safety Settings) |

### search_grounded_image

Generate images using real-time Google Search data.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | Yes | - | Description incorporating real-time data needs |
| `aspect_ratio` | string | No | `16:9` | Output aspect ratio |
| `resolution` | string | No | `2K` | Output resolution (1K, 2K, 4K) |
| `output_path` | string | No | None | Path to save the image |
| `safety` | string | No | None | Safety filter threshold (see Safety Settings) |

### generate_interleaved

Generate interleaved text and image output from a single prompt. Ideal for illustrated recipes, stories, tutorials, and other mixed-media content. Returns multiple content blocks preserving the order of text and images from the model response.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | Yes | - | Text description that may produce mixed text+image output |
| `model` | string | No | `gemini-3-pro-image-preview` | Model to use |
| `aspect_ratio` | string | No | `1:1` | Output aspect ratio |
| `resolution` | string | No | `1K` | Output resolution (1K, 2K, 4K) |
| `output_dir` | string | No | `outputs` | Directory to save generated images |
| `safety` | string | No | None | Safety filter threshold (see Safety Settings) |

### start_image_chat

Start a new multi-turn image editing session.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `initial_prompt` | string | Yes | - | First prompt to generate the initial image |
| `model` | string | No | `gemini-3-pro-image-preview` | Model to use for the session |
| `output_path` | string | No | None | Path to save the image |
| `seed` | integer | No | None | Optional seed (currently ignored in chat sessions) |

Returns a `session_id` for use with `continue_image_chat`.

### continue_image_chat

Continue an existing image chat session.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `session_id` | string | Yes | - | ID of the session to continue |
| `prompt` | string | Yes | - | Next instruction for image modification |
| `aspect_ratio` | string | No | None | Optional new aspect ratio |
| `resolution` | string | No | None | Optional new resolution |
| `output_path` | string | No | None | Path to save the image |

### end_image_chat

End and clean up an image chat session.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `session_id` | string | Yes | - | ID of the session to end |

### list_chat_sessions

List all active chat sessions. No parameters.

### validate_intake_digest

Validate a Stage 0 source digest against the intake schema.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `yaml_content` | string | Yes | - | JSON string of the digest to validate |

## Best Practices Hook

Prompting best practices and tool routing guidance are delivered automatically via a `UserPromptSubmit` hook. When your prompt mentions image generation, the hook injects a compact cheatsheet into context — no manual tool call needed.

### Install

```bash
scripts/install-hook.sh
```

This copies the hook to `~/.claude/hooks/` and registers it in `~/.claude/settings.json`, so it works across all projects.

### Uninstall

```bash
scripts/install-hook.sh --uninstall
```

### What it does

When your prompt contains image-related keywords (e.g., "generate an image", "edit the photo", "poster", "infographic"), the hook automatically injects:

- **Tool routing** — which tool to use for which task
- **Prompt engineering rules** — the 6-component formula, text rendering limits
- **Parameter guidance** — resolution, safety, model selection
- **Workflow tips** — iterative editing, character consistency, composition

## Model

Uses `gemini-3-pro-image-preview` (Gemini 3 Pro). You can also use the aliases `pro` or `nano-banana-pro`.

## Features

- Text-to-image generation
- Image editing with text prompts
- Multi-image composition (up to 14 images)
- Interleaved text+image generation for mixed-media content
- Google Search grounding for real-time data
- Multi-turn chat sessions for iterative refinement
- Configurable safety filter thresholds
- Resolutions: 1K, 2K, 4K
- Reproducible generation with seed parameter

### Valid Values

**Aspect Ratios**: `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

**Resolutions**: `1K`, `2K`, `4K`

### Safety Settings

The `safety` parameter controls content filtering on generation tools. When omitted, the API uses its defaults.

| Value | Behavior |
|-------|----------|
| `block_none` | No content blocked |
| `block_low` | Block low-threshold and above |
| `block_medium` | Block medium-threshold and above |
| `block_high` | Block only high-threshold content |

Applied uniformly across all harm categories (harassment, hate speech, sexually explicit, dangerous content). Not available on chat session tools (`start_image_chat`, `continue_image_chat`).

## Development

```bash
# Install dependencies
bun install

# Run tests
bun test

# Run server
GEMINI_API_KEY=your-key bun run src/index.ts

# Run with watch mode
GEMINI_API_KEY=your-key bun --watch run src/index.ts
```

## Stack

- **Runtime**: [Bun](https://bun.sh/)
- **Language**: TypeScript
- **MCP SDK**: `@modelcontextprotocol/sdk`
- **Gemini SDK**: `@google/genai`
- **Validation**: `zod`

## CLAUDE.md Configuration

For better Claude Code integration, add instructions about the MCP server to your project's `CLAUDE.md` file. This helps Claude understand the available tools and how to use them.

> [!TIP]
> **If you already have a CLAUDE.md:** Ask Claude Code to append the relevant instructions:
> ```
> Read the nanobananapro-mcp README and add instructions for using the image generation tools to my CLAUDE.md
> ```
>
> **If you don't have a CLAUDE.md yet:** Ask Claude Code to create one:
> ```
> Read the README.md and create a CLAUDE.md with instructions on using the nanobananapro MCP server
> ```
