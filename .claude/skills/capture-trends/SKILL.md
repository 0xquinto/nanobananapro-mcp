---
name: capture-trends
description: Extract visual trends from URLs, articles, PDFs, or images and
  save as style presets. Use when user shares inspiration links, trend reports,
  reference images, or wants to capture a style from an external source.
  Populates style-library.md with extracted presets. Use --guide to also create/update style-guide.md.
argument-hint: "<source> [--name=preset] [--guide] [--preview] [--modular]"
---

# Capture Trends

Extract visual trends from external sources and convert them to reusable style presets.

## Project Context Detection

This skill is project-aware and determines where to save presets based on context:

### Detection Priority

1. **`--project=<path>` flag** → Save to `<path>/style-library.md`
2. **`--root` flag** → Save to repository root `style-library.md`
3. **Current directory has project markers** → Save to current project's `style-library.md`
4. **Parent directory has project markers** → Save to that project's `style-library.md`
5. **No project context** → Save to repository root `style-library.md`

### Project Markers

A directory is considered a "project" if it contains ANY of:
- `style-guide.md`
- `style-library.md`
- `outputs/` directory
- `references/` directory

### Inheritance Behavior

When saving to a **project** `style-library.md`:
- The project inherits all presets from **root** `style-library.md`
- Project presets can override or extend root presets
- Add note: `*Inherits all presets from root style-library.md*`

When saving to **root** `style-library.md`:
- Presets are available to all projects
- Use for shared/global styles

### Examples

```bash
# In demo-campaign/ folder → saves to demo-campaign/style-library.md
/capture-trends ./inspiration.jpg

# Force save to root even when in project folder
/capture-trends ./inspiration.jpg --root

# Explicitly target a project from anywhere
/capture-trends ./trends.pdf --project=demo-campaign

# From root with no project context → saves to root style-library.md
/capture-trends https://example.com/trends
```

## Supported Sources

| Source Type | Detection | What to Extract |
|-------------|-----------|-----------------|
| **Web URL** | Starts with `http://` or `https://` | Color mentions, style keywords, mood descriptors, art movements |
| **Image file** | `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif` | Dominant colors, lighting, composition, texture, medium |
| **PDF file** | `.pdf` | Text analysis for style terms, embedded image analysis |
| **Markdown file** | `.md` | Style descriptions, color codes, reference terms |

## Process

### Step 1: Detect Source Type

Parse the input to determine source:
- URL → fetch and analyze page content
- Image → analyze visual properties
- PDF → extract text and images, analyze both
- Markdown → parse for style-relevant content

### Step 2: Extract Style Indicators

**From text sources (URL, PDF, Markdown):**
- Color names and hex codes
- Art movements and styles (impressionist, brutalist, etc.)
- Lighting descriptions (soft, dramatic, golden hour)
- Mood keywords (cozy, tense, ethereal)
- Medium references (watercolor, photography, 3D)
- Texture words (grainy, smooth, textured)

**From images:**
- Dominant color palette (extract 3-5 main colors with hex codes)
- Lighting quality (direction, hardness, color temperature)
- Composition style (centered, rule of thirds, symmetrical)
- Texture and detail level
- Apparent medium (photo, illustration, painting, 3D)
- Overall mood and atmosphere

### Step 3: Synthesize Preset

Combine extracted elements into a prompt-ready style definition:

```
"[Lighting description], [color palette with hex codes], [texture/medium],
[composition tendency], [mood/atmosphere]"
```

### Step 4: Save to Style Library

1. Check if `style-library.md` exists
   - If no: create with starter template
2. Determine category (or use `--category` flag)
3. Add preset under appropriate section
4. Confirm with preview of what was added

## Options

| Flag | Description |
|------|-------------|
| `--name=<preset>` | Name for the extracted preset (otherwise auto-generated) |
| `--category=<cat>` | Target category in style library |
| `--preview` | Show extraction without saving |
| `--merge` | Combine with existing preset of same name |
| `--modular` | Extract into separate style/palette/mood/lighting presets |
| `--guide` | Also create/update style-guide.md with extracted constraints |
| `--root` | Force save to root style-library.md (ignore project context) |
| `--project=<path>` | Save to specific project's style-library.md |

## Style Guide Generation (--guide flag)

When `--guide` is used, also create or update `style-guide.md` with extracted project constraints.

### What Gets Extracted for style-guide.md

| Source Content | Populates In style-guide.md |
|----------------|----------------------------|
| Color palettes with hex codes | **Color Palette** section with primary/secondary colors |
| Mood/atmosphere descriptions | **Mood Keywords** section |
| Medium mentions (photo, illustration) | **Visual Medium** section |
| Style do's and don'ts | **Prompt Patterns** → Do's and Don'ts |
| Dimension/format mentions | **Asset Requirements** section |
| Lighting descriptions | **Visual Direction** notes |

### Style Guide Template

When `--guide` creates a new `style-guide.md`, use this structure:

| Section | Content |
|---------|---------|
| **Overview** | Source, date, trend count |
| **Visual Direction** | Style summary, mood keywords |
| **Color Palette** | Primary colors (name, hex, usage), color mood |
| **Visual Medium** | Primary medium, notes |
| **Prompt Patterns** | Recommended presets, do's/don'ts |
| **Asset Requirements** | Dimensions, formats, technical specs |

Footer: `*Generated from [source] using /capture-trends --guide*`

### Behavior with Existing style-guide.md

| Situation | Action |
|-----------|--------|
| No style-guide.md exists | Create new from template |
| style-guide.md exists | **Merge** new content, preserving existing sections |
| Conflicting content | Show diff, ask user which to keep |

### When to Use --guide

| Scenario | Use --guide? |
|----------|--------------|
| New project from trend report | Yes |
| Single style from reference image | No |
| Comprehensive brand document | Yes |
| Quick inspiration capture | No |
| Multi-trend PDF/report | Yes |

## Critical: Multi-Trend Documents

**IMPORTANT:** Some sources (trend reports, style guides, mood board collections) contain **multiple distinct trends**, not one unified style.

### Detection Signals

- Numbered/named sections ("Trend 1: Cool Blue", "Trend 2: Vamp Romantic")
- Multiple distinct aesthetics described separately
- Trend forecasts or "predicts" documents

### Required Behavior

| Do | Don't |
|----|-------|
| Extract each trend as separate preset | Create meta-style named after source document |
| `cool-blue`, `vamp-romantic`, `gimme-gummy` | `pinterest-2026` combining everything |
| Ask user how to proceed when multiple detected | Silently merge unrelated aesthetics |

When multiple trends detected, prompt:
```
I found 21 distinct trends. Should I:
1. Extract all as separate presets
2. Let you pick specific trends
3. Extract first few as examples
```

## Modular Extraction (--modular flag)

When `--modular` is used, extract into **separate categories** for mix-and-match:

| Category | Extracts | Independent Of |
|----------|----------|----------------|
| **Art Styles** | Composition, textures, visual treatment | Colors, mood, lighting |
| **Color Palettes** | Color schemes with hex codes | Style, mood |
| **Moods** | Emotional atmosphere, energy | Style, colors |
| **Lighting** | Direction, quality, temperature | Style, colors, mood |

### Critical: 1:1:1:1 Extraction Rule

**For multi-trend documents, extract ALL FOUR categories for EACH trend.**

If document has 21 trends, output must be:
- Art Styles: 21 presets
- Color Palettes: 21 presets
- Moods: 21 presets
- Lighting: 21 presets

**Total: N trends x 4 categories = 4N presets**

Label presets with source trend for matching:
```markdown
### From Vamp Romantic
- **vamp-darks**: "Deep burgundy #722F37, black #0D0D0D..."
```

### Why Modular?

| Approach | Example | Flexibility |
|----------|---------|-------------|
| Non-modular | `vamp-romantic` = style + palette + mood + lighting | One fixed combination |
| Modular | Separate `vamp-romantic`, `vamp-darks`, `haunting-melancholy`, `candlelit-gothic` | Mix any style + palette + mood + lighting |

## Category Auto-Detection

If no `--category` specified, infer from content:

| Content Focus | Auto Category |
|---------------|---------------|
| Color-dominant (palette, hex codes) | `color-palettes` |
| Lighting-focused (shadows, key light) | `lighting` |
| Art movement/medium | `art-styles` |
| Emotional descriptors | `moods` |
| Person/figure description | `characters` |
| Framing/angle focus | `compositions` |

## Output Format

### Preview (with --preview or always before saving)

```
## Trend Extraction: [source name]

**Source:** [URL/path]
**Detected type:** [Image/URL/PDF/Markdown]

### Extracted Elements

| Category | Found |
|----------|-------|
| Colors | #264653 (teal), #E76F51 (coral), #2A9D8F (sage) |
| Lighting | Low-key, single dramatic side light |
| Medium | Editorial photography |
| Mood | Contemplative, intimate |
| Composition | Close framing, shallow depth |

### Generated Preset

**Name:** `[name]`
**Category:** `[category]`

"Low-key portrait lighting, single dramatic side light, deep shadows,
desaturated color palette with teal #264653 and burnt orange #E76F51
accents, shallow depth of field, editorial photography style,
contemplative mood"
```

### After Saving

```
✓ Added `[preset-name]` to style-library.md under `[category]`

Use with:
- `/enhance-prompt --style=[preset-name]`
- `/image-prompt --style=[preset-name]`
```

## Extraction Guidelines

### From Images

| Aspect | Extract |
|--------|---------|
| **Colors** | 3-5 dominant colors with hex codes, warm/cool balance, relationships |
| **Lighting** | Direction, quality (hard/soft), temperature, contrast |
| **Composition** | Subject placement, depth, framing, angle |
| **Medium** | Photo/illustration/3D, processing style, texture quality |
| **Mood** | Emotional impression, atmosphere, energy level |

### From Text/URLs

| Pattern Type | Examples |
|--------------|----------|
| Style mentions | "in the style of...", "[medium] aesthetic", "inspired by..." |
| Color language | Named colors, hex codes, color moods (earthy, neon, muted) |
| Atmosphere | Lighting words, mood descriptors, era references |

## Examples

### Single Source (Image/URL)

```
/capture-trends ./moody-portrait.jpg --name=dark-editorial

## Trend Extraction: moody-portrait.jpg
**Source:** ./moody-portrait.jpg | **Type:** Image (JPEG)

| Category | Found |
|----------|-------|
| Colors | #1A1A2E (deep navy), #E8D5B7 (warm skin), #4A4A6A (muted purple) |
| Lighting | Single key light from left, strong shadows |
| Medium | Studio photography, film grain |
| Mood | Contemplative, intimate |

**Preset:** `dark-editorial` → "Low-key portrait lighting, dramatic side light,
desaturated palette with warm skin against deep navy #1A1A2E..."

✓ Added to style-library.md under `lighting`
```

### Multi-Trend Document (--modular)

```
/capture-trends ./Pinterest-Predicts-2026.pdf --modular

## Trend Extraction: Pinterest Predicts 2026
**Source:** ./Pinterest-Predicts-2026.pdf | **Type:** PDF (24 pages)
**Detected:** 21 distinct trends

How should I proceed?
1. Extract all as separate presets
2. Pick specific trends
3. Extract first few as examples

> User: Extract all, make it modular

### Result (1:1:1:1 complete)
- Art Styles (21): cool-blue, vamp-romantic, pen-pals...
- Color Palettes (21): icy-subzero, vamp-darks, postal-vintage...
- Moods (21): icy-sophistication, haunting-melancholy...
- Lighting (21): icy-crisp, candlelit-gothic, window-warmth...

✓ 84 mix-and-match presets (21 × 4 categories)

Usage: /image-prompt portrait --style=vamp-romantic --palette=icy-subzero
```

### With --merge

```
/capture-trends ./ref2.jpg --name=dark-editorial --merge

Existing: "Low-key portrait lighting, single dramatic side light..."
Adding: #8B4513 (warm brown accent), "catchlight in eyes"
Merged: "...with teal #264653, burnt orange #E76F51, and warm brown #8B4513..."

✓ Updated `dark-editorial` in style-library.md
```

## Integration

| Skill | Integration |
|-------|-------------|
| `/style-library` | Presets saved in same format: `- **name**: "definition"` |
| `/project-setup` | Suggest capture-trends on `references/` images |
| `/image-prompt` | After capture: `Try: /image-prompt [concept] --style=[preset]` |

## Error Handling

| Situation | Response |
|-----------|----------|
| URL unreachable | "Could not fetch URL. Check the link and try again." |
| Image not found | "File not found: [path]. Check the path is correct." |
| Unsupported format | "Unsupported file type. Supported: PNG, JPG, WEBP, GIF, PDF, MD" |
| Empty extraction | "Could not extract meaningful style information. Try a different source." |
| Preset exists (no --merge) | "Preset `[name]` already exists. Use `--merge` to combine, or choose a different name." |
