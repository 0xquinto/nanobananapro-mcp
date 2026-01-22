# Image Generation Skills

Claude Code skills for AI-powered image generation using the nanobananapro MCP server (Gemini 3 Pro).

## Quick Reference

| Skill | Command | Purpose |
|-------|---------|---------|
| [quickstart](#quickstart) | `/quickstart` | New user onboarding |
| [image-prompt](#image-prompt) | `/image-prompt` | Generate images from concepts |
| [enhance-prompt](#enhance-prompt) | `/enhance-prompt` | Improve naive prompts |
| [prompt-anatomy](#prompt-anatomy) | `/prompt-anatomy` | Analyze prompt quality |
| [style-library](#style-library) | `/style-library` | Manage style presets |
| [capture-trends](#capture-trends) | `/capture-trends` | Extract styles from references |
| [project-setup](#project-setup) | `/project-setup` | Scaffold visual projects |

## Workflow Overview

```
                    ┌─────────────────┐
                    │   quickstart    │ ← Start here if new
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  project-setup  │ ← Or here for multi-image projects
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ capture-trends  │ │  style-library  │ │ enhance-prompt  │
│ (from refs)     │ │ (manage presets)│ │ (improve ideas) │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  image-prompt   │ ← Primary generation skill
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ prompt-anatomy  │ ← Debug if results are poor
                    └─────────────────┘
```

## Skills

### image-prompt

**The primary skill for image creation.** Takes rough concepts through enhancement, generation, and iteration.

```bash
# Basic usage
/image-prompt a coffee shop

# With options
/image-prompt a portrait --style=cinematic --aspect=16:9
/image-prompt character design --chat              # Multi-turn refinement
/image-prompt product shot --refs=./references/    # With reference images
/image-prompt weather in Tokyo --grounded          # Real-time data
```

**Options:**
- `--chat` — Iterative refinement session
- `--style=<preset>` — Apply style from style-library.md
- `--refs=<path>` — Include reference images
- `--aspect=<ratio>` — Set aspect ratio (1:1, 16:9, 9:16, etc.)
- `--resolution=<res>` — Output quality (1K, 2K, 4K)
- `--grounded` — Use search-grounded generation for real-world data
- `--project=<path>` — Use specific project context

---

### enhance-prompt

Transform vague concepts into effective prompts using the 6-element formula.

```bash
# Interactive mode
/enhance-prompt

# Direct enhancement
/enhance-prompt a dog in a park

# Quick mode (skip questions)
/enhance-prompt a sunset --quick

# With style preset
/enhance-prompt a portrait --style=cinematic

# Generate immediately after enhancing
/enhance-prompt a wizard --generate
```

**Options:**
- `--quick` — Skip questions, enhance directly
- `--generate` — Call MCP tool after enhancing
- `--style=<preset>` — Apply preset from style-library.md
- `--explain` — Show enhancement breakdown

---

### quickstart

**New user onboarding.** Guided introduction that routes to the right skill.

```bash
# Start guided onboarding
/quickstart
```

Automatically suggests itself when:
- No style-library.md found
- First image-related request in session
- User asks "how do I start?" or "what can you do?"

---

### prompt-anatomy

Analyze prompts against the 6-element framework. Educational tool for understanding prompt structure.

```bash
# Basic analysis
/prompt-anatomy a cat sitting

# With fix suggestions
/prompt-anatomy "a mountain landscape" --fix

# Verbose mode with explanations
/prompt-anatomy "cyberpunk city at night" --verbose
```

**The 6-Element Framework:**

| Element | What it defines |
|---------|-----------------|
| Subject | Who/what is the main focus |
| Composition | How the frame is arranged |
| Action | What's happening |
| Location | Where it takes place |
| Style | Visual treatment |
| Constraints | Text, aspect ratio, specifics |

---

### style-library

Manage reusable style presets for consistent image generation.

```bash
# List all presets
/style-library list

# List by category
/style-library list art-styles

# Add a preset
/style-library add vintage-photo "Faded colors, light leaks, film grain"

# Apply a preset (shows definition)
/style-library apply cinematic

# Remove a preset
/style-library remove old-preset

# Save to root (global) library
/style-library add shared-style "..." --root
```

**Categories:** art-styles, color-palettes, lighting, characters, compositions, moods

---

### capture-trends

Extract visual trends from URLs, images, PDFs, or articles and save as presets.

```bash
# From an image
/capture-trends ./inspiration/mood-photo.jpg --name=dark-editorial

# From a URL
/capture-trends https://example.com/design-trends

# From a trend report (extracts all trends)
/capture-trends ./Pinterest-2026.pdf --modular

# Also create style-guide.md
/capture-trends ./brand-doc.pdf --guide

# Preview without saving
/capture-trends ./reference.jpg --preview
```

**Options:**
- `--name=<preset>` — Name for the extracted preset
- `--category=<cat>` — Target category
- `--modular` — Extract separate style/palette/mood/lighting presets
- `--guide` — Also create/update style-guide.md
- `--preview` — Show extraction without saving
- `--merge` — Combine with existing preset

---

### project-setup

Scaffold a complete image generation project with style guide, directories, and templates.

```bash
# Interactive setup
/project-setup

# With name and type
/project-setup my-brand --type=brand
/project-setup hero-campaign --type=campaign
/project-setup luna-character --type=character
/project-setup product-shots --type=product
```

**Generated Structure:**
```
project-name/
├── style-guide.md           # AI-ready style constraints
├── style-library.md         # Project presets
├── references/
│   ├── moodboards/
│   ├── characters/
│   └── inspiration/
├── outputs/
│   ├── exploration/         # Work in progress
│   └── finals/              # Approved assets
└── asset-log.md             # Generation tracking
```

## Flag Syntax Standard

All skills follow consistent flag patterns:

| Pattern | Type | Example | Meaning |
|---------|------|---------|---------|
| `--flag` | Boolean | `--chat`, `--quick` | Enables a feature |
| `--flag=<value>` | Value | `--style=cinematic` | Sets a parameter |

**Common flags across skills:**

| Flag | Available In | Description |
|------|--------------|-------------|
| `--style=<preset>` | image-prompt, enhance-prompt | Apply style from style-library.md |
| `--project=<path>` | image-prompt, enhance-prompt | Use specific project context |
| `--quick` | enhance-prompt | Skip interactive questions |
| `--generate` | enhance-prompt | Generate image after enhancing |
| `--chat` | image-prompt | Enable iterative refinement session |

---

## Project Context

Skills are project-aware. When inside a project directory (one containing `style-guide.md`, `style-library.md`, `outputs/`, or `references/`):

- Style presets are loaded from the project's `style-library.md`
- Brand constraints are read from `style-guide.md`
- Generated images save to `outputs/`
- Project presets override root presets of the same name

**Override context:**
- `--project=<path>` — Use specific project
- `--root` — Use root style-library.md

## MCP Tools Used

These skills orchestrate the nanobananapro MCP tools:

| MCP Tool | Used For |
|----------|----------|
| `generate_image` | Standard image generation |
| `edit_image` | Single modifications to existing images |
| `compose_images` | Combining multiple reference images |
| `search_grounded_image` | Images with real-time data (weather, news) |
| `start_image_chat` | Begin iterative refinement session |
| `continue_image_chat` | Continue refinement session |
| `end_image_chat` | Close refinement session |

## Examples

### Quick Image Generation
```bash
/image-prompt a cozy reading nook with warm lighting
```

### Brand-Consistent Campaign
```bash
/project-setup spring-launch --type=campaign
/capture-trends ./brand-guidelines.pdf --guide
/image-prompt hero banner --style=brand-main
```

### Character Design Iteration
```bash
/image-prompt fantasy warrior character --chat
> "add armor"
> "make the pose more dynamic"
> "done"
```

### Style Extraction
```bash
/capture-trends ./inspiration.jpg --name=moody-portrait
/image-prompt corporate headshot --style=moody-portrait
```
