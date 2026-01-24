# Image Generation Skills

Claude Code skills for AI-powered image generation using the nanobananapro MCP server (Gemini 3 Pro).

## Quick Reference

| Skill | Command | Purpose |
|-------|---------|---------|
| [quickstart](#quickstart) | `/quickstart` | New user onboarding |
| [moodboard](#moodboard) | `/moodboard` | Learn design through moodboard creation |
| [image-prompt](#image-prompt) | `/image-prompt` | Generate images from concepts |
| [enhance-prompt](#enhance-prompt) | `/enhance-prompt` | Improve naive prompts |
| [prompt-anatomy](#prompt-anatomy) | `/prompt-anatomy` | Analyze prompt quality |
| [taste-check](#taste-check) | `/taste-check` | Detect clichés, accessibility issues, and content flags |
| [style-library](#style-library) | `/style-library` | Manage style presets |
| [capture-trends](#capture-trends) | `/capture-trends` | Extract styles from references |
| [project-setup](#project-setup) | `/project-setup` | Scaffold visual projects |

## Workflow Overview

```
                    ┌─────────────────┐
                    │   quickstart    │ ← Start here if new
                    └────────┬────────┘
                             │
            ┌────────────────┴────────────────┐
            │                                 │
            ▼                                 ▼
   ┌─────────────────┐               ┌─────────────────┐
   │  project-setup  │               │    moodboard    │ ← Learn design thinking
   └────────┬────────┘               └────────┬────────┘
            │                                 │
            └────────────────┬────────────────┘
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
                    └────────┬────────┘   (includes taste layer)
                             │
                             ▼
         ┌───────────────────┴───────────────────┐
         │                                       │
         ▼                                       ▼
┌─────────────────┐                     ┌─────────────────┐
│ prompt-anatomy  │ ← Debug structure   │   taste-check   │ ← Debug aesthetics/a11y
└─────────────────┘                     └─────────────────┘
```

### How to Navigate

**Entry points:**
- **New to image generation?** → Start with `/quickstart`
- **Want to learn design fundamentals?** → Use `/moodboard` for guided learning
- **Multi-image project (campaign, brand, product)?** → Start with `/project-setup`
- **Just want one image?** → Jump straight to `/image-prompt`

**Preparation layer (optional):**
- `/capture-trends` — Extract style from reference images, URLs, or PDFs
- `/style-library` — Save and manage reusable presets
- `/enhance-prompt` — Standalone prompt improvement (also built into image-prompt)

**Generation:**
- `/image-prompt` — The primary skill. Handles prompt enhancement, generation, and iteration. Includes a taste layer for cliché detection.

**Debugging (when things don't work):**
- `/prompt-anatomy` — Structural issues (missing elements, poor composition)
- `/taste-check` — Aesthetic issues (clichés, vague intent), accessibility, and content flags

### Decision Logic

```
"I want to get better at design"
  → /moodboard — Guided learning through moodboard creation

"I want an image"
  → Is this part of a larger project?
    → Yes → /project-setup first
    → No  → /image-prompt

"My prompt isn't working"
  → Is the output structurally wrong (wrong subject, bad framing)?
    → Yes → /prompt-anatomy
  → Does it look generic or AI-ish?
    → Yes → /taste-check

"I have reference images to match"
  → /capture-trends to extract style → /style-library to save → /image-prompt --style=<preset>

"I want consistency across images"
  → /project-setup → define style-guide.md → all /image-prompt calls inherit constraints
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
- `--taste=<level>` — Cliché detection sensitivity (low/medium/high)
- `--learn` — Show reasoning for taste suggestions
- `--no-taste` — Skip taste checks (speed mode)

**Taste Layer:** The skill now asks "What should the viewer feel?" before enhancement, runs cliché detection after, and offers critique after generation.

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
/quickstart
```

Auto-suggests when: no style-library.md found, first image request, or user asks "how do I start?"

---

### moodboard

**Learn design thinking through guided moodboard creation.** For vibecoders who want to develop visual design intuition.

```bash
/moodboard
/moodboard "coffee shop brand"
/moodboard "summer campaign" --quick
/moodboard analyze ./reference.png
/moodboard learn colors
```

**Workflow:** Define intent -> Build palette -> Generate -> Reflect -> Extract and save

**What you'll learn:** Articulate visual preferences, build design vocabulary, make intentional choices, create consistency.

---

### prompt-anatomy

Analyze prompts against the 6-element framework (Subject, Composition, Action, Location, Style, Constraints). Educational tool for understanding prompt structure.

```bash
/prompt-anatomy a cat sitting
/prompt-anatomy "a mountain landscape" --fix
/prompt-anatomy "cyberpunk city at night" --verbose
```

---

### taste-check

Analyze prompts for aesthetic quality, accessibility, and content considerations. Detects cliches, checks specificity, evaluates intent clarity, and flags potential issues.

```bash
/taste-check "An epic fantasy landscape"
/taste-check "A busy infographic with small text" --accessibility
/taste-check "A portrait of a child" --learn --accessibility
```

**Options:** `--learn`, `--taste=<level>`, `--fix`, `--accessibility`

See `taste-check/taste-patterns.md` for pattern definitions.

---

### style-library

Manage reusable style presets for consistent image generation.

```bash
/style-library list [category]
/style-library add vintage-photo "Faded colors, light leaks, film grain"
/style-library apply cinematic
/style-library remove old-preset
```

**Categories:** art-styles, color-palettes, lighting, characters, compositions, moods

---

### capture-trends

Extract visual trends from URLs, images, PDFs, or articles and save as presets.

```bash
/capture-trends ./inspiration/mood-photo.jpg --name=dark-editorial
/capture-trends https://example.com/design-trends
/capture-trends ./Pinterest-2026.pdf --modular
/capture-trends ./brand-doc.pdf --guide
```

**Options:** `--name`, `--category`, `--modular`, `--guide`, `--preview`, `--merge`

---

### project-setup

Scaffold a complete image generation project with style guide, directories, and templates.

```bash
/project-setup
/project-setup my-brand --type=brand
/project-setup my-project --quick
```

**Options:** `--type=<brand|campaign|character|product>`, `--quick`, `--lock`, `--unlock`

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

## Flag Syntax

All skills use consistent flag patterns: `--flag` (boolean) or `--flag=<value>` (parameter).

Common flags: `--style`, `--project`, `--quick`, `--dry-run`, `--format`. See individual skill documentation for complete flag reference.

---

## Project Context

Skills are project-aware. When inside a project directory (containing `style-guide.md`, `style-library.md`, `outputs/`, or `references/`):

- Style presets load from the project's `style-library.md`
- Brand constraints apply from `style-guide.md`
- Generated images save to `outputs/`
- Project presets override root presets of the same name

**Override:** `--project=<path>` or `--root`

## Pattern Documentation

- **[gemini-patterns.md](../gemini-patterns.md)** — Model-specific behaviors
- **[taste-patterns.md](./taste-check/taste-patterns.md)** — Cliche detection patterns

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

## Hooks

Claude Code hooks enforce project conventions automatically.

| Hook | Purpose |
|------|---------|
| `check-style-guide-lock.sh` | Block edits to locked style-guide.md |
| `protect-finals.sh` | Prevent modification of outputs/finals/ |
| `log-generated-image.sh` | Auto-log generated images to asset-log.md |

**Key behaviors:**
- Locked style guides (`locked: true` in frontmatter) require `/project-setup --unlock` to edit
- Files in `outputs/finals/` are protected; copy to `outputs/exploration/` to iterate
- Asset logging captures date, filename, prompt summary, tool, seed, and path

Hooks are defined in `.claude/settings.json` and can be overridden in `.claude/settings.local.json`.

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
