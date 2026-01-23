---
name: capture-trends
description: Extract visual trends from URLs, articles, PDFs, or images and
  save as style presets. Use when user shares inspiration links, trend reports,
  reference images, or wants to capture a style from an external source.
  Populates style-library.md with extracted presets. Use --guide to also create/update style-guide.md.
argument-hint: "<source> [--name=preset] [--guide] [--preview] [--dry-run]"
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

| Flag | Usage | Description |
|------|-------|-------------|
| `--name=<preset>` | `--name=moody-portrait` | Name for the extracted preset (otherwise auto-generated) |
| `--category=<cat>` | `--category=lighting` | Target category in style library |
| `--preview` | `--preview` | Show extraction without saving to file |
| `--merge` | `--merge` | Combine with existing preset of same name |
| `--modular` | `--modular` | Extract into separate style/palette/mood/lighting presets |
| `--guide` | `--guide` | Also create/update style-guide.md with extracted constraints |
| `--root` | `--root` | Force save to root style-library.md (ignore project context) |
| `--project=<path>` | `--project=demo-campaign` | Save to specific project's style-library.md |
| `--dry-run` | `--dry-run` | Analyze source and show extracted styles without saving (alias for --preview) |

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

When `--guide` creates a new `style-guide.md`, it uses this structure:

```markdown
# [Source Name] Style Guide

> AI-ready style guide extracted from [source]

## Overview

**Source:** [URL/file path]
**Extracted:** [date]
**Trends covered:** [count if multi-trend]

## Visual Direction

### Style Summary
[Synthesized from extracted trends]

### Mood Keywords
- [keyword 1]
- [keyword 2]
- [keyword 3]

## Color Palette

### Primary Colors
| Name | Hex | Usage |
|------|-----|-------|
| [Color 1] | #XXXXXX | [extracted context] |
| [Color 2] | #XXXXXX | [extracted context] |

### Color Mood
[Overall color direction from source]

## Visual Medium

**Primary:** [Most common medium from source]

### Medium Notes
- [Extracted medium guidance]

## Prompt Patterns

### Recommended Presets
Reference these from the extracted style-library.md:
- `--style=[preset1]`
- `--style=[preset2]`

### Do's
- [Extracted positive guidance]

### Don'ts
- [Extracted things to avoid]

## Asset Requirements

[Any dimension, format, or technical requirements found]

---

*Generated from [source] using `/capture-trends --guide`*
*Presets saved to style-library.md*
```

### Behavior with Existing style-guide.md

| Situation | Action |
|-----------|--------|
| No style-guide.md exists | Create new from template |
| style-guide.md exists | **Merge** new content, preserving existing sections |
| Conflicting content | Show diff, ask user which to keep |

### Example with --guide

```bash
/capture-trends ./Pinterest-Predicts-2026.pdf --modular --guide

## Extraction Complete

### style-library.md
✓ Added 84 presets (21 trends × 4 categories)

### style-guide.md
✓ Created with:
  - 21 mood keywords
  - Color palettes from all trends
  - Medium guidance (photography, illustration mix)
  - Do's/Don'ts for trend-aligned imagery
  - Recommended preset combinations

**Files created:**
- style-library.md (presets)
- style-guide.md (constraints)

Ready to use:
/image-prompt a portrait --style=vamp-romantic
```

### When to Use --guide

| Scenario | Use --guide? |
|----------|--------------|
| Setting up a new project from a trend report | ✓ Yes |
| Adding a single style from a reference image | ✗ No (just presets) |
| Comprehensive brand/style document | ✓ Yes |
| Quick inspiration capture | ✗ No (just presets) |
| Multi-trend PDF/report | ✓ Yes (creates unified guide) |

## Critical: Multi-Trend Documents

**IMPORTANT:** Some sources (trend reports, style guides, mood board collections) contain **multiple distinct trends**, not one unified style.

### How to Detect Multi-Trend Sources

Look for:
- Numbered or named sections (e.g., "Trend 1: Cool Blue", "Trend 2: Vamp Romantic")
- Multiple distinct aesthetics described separately
- Trend forecasts or "predicts" documents
- Style guides with different "looks" or "moods"

### What NOT to Do

❌ **Never create a meta-style named after the source document:**
```
# BAD - This just describes the PDF, not a usable style
- **pinterest-2026**: "2026 trends mixing maximalist glamour with..."
```

❌ **Never combine unrelated trends into one preset:**
```
# BAD - These are separate aesthetics, not one style
- **trend-report**: "Icy blues AND gothic romance AND candy textures..."
```

### What TO Do

✓ **Extract each trend as its own preset:**
```
# GOOD - Each trend is distinct and usable
- **cool-blue**: "Icy subzero aesthetic, crystalline surfaces..."
- **vamp-romantic**: "Gothic romance, Victorian silhouettes..."
- **gimme-gummy**: "Tactile candy aesthetic, glossy surfaces..."
```

✓ **Ask the user if multiple trends are detected:**
```
I found 21 distinct trends in this document. Should I:
1. Extract all as separate presets
2. Let you pick specific trends to extract
3. Extract just the first few as examples
```

## Modular Extraction (--modular flag)

When `--modular` is used (or for multi-trend documents), extract into **separate categories** that can be mixed and matched:

| Category | What to Extract | Keep Separate From |
|----------|-----------------|-------------------|
| **Art Styles** | Composition, textures, subject matter, visual treatment | Colors, mood, lighting |
| **Color Palettes** | Color schemes with hex codes | Style, mood |
| **Moods** | Emotional atmosphere, energy, feeling | Style, colors |
| **Lighting** | Light direction, quality, temperature | Style, colors, mood |

### Critical: 1:1:1:1 Extraction Rule

**For multi-trend documents, extract ALL FOUR categories for EACH trend.**

❌ **WRONG - Incomplete extraction:**
```
Art Styles: 21 presets (one per trend)
Color Palettes: 10 presets  ← Missing 11!
Moods: 8 presets            ← Missing 13!
Lighting: 7 presets         ← Missing 14!
```

✓ **CORRECT - Complete extraction:**
```
Art Styles: 21 presets (one per trend)
Color Palettes: 21 presets (one per trend)
Moods: 21 presets (one per trend)
Lighting: 21 presets (one per trend)
```

Each trend has its own:
- Visual aesthetic → Art Style preset
- Color direction → Color Palette preset
- Emotional atmosphere → Mood preset
- Lighting quality → Lighting preset

**Label each preset with its source trend** for easy matching:
```markdown
### From Vamp Romantic
- **vamp-darks**: "Deep burgundy #722F37, black #0D0D0D..."
```

### Why Modular?

Non-modular (baked-in):
```
- **vamp-romantic**: "Gothic aesthetic, deep burgundy palette, haunting mood, candlelit lighting"
# Can only use this exact combination
```

Modular (mix-and-match):
```
- **vamp-romantic**: "Gothic aesthetic, Victorian silhouettes, lace textures, velvet fabrics"
- **vamp-darks**: "Deep burgundy #722F37, black #0D0D0D, gold accents"
- **haunting-melancholy**: "Dramatic shadows, romantic longing, bittersweet atmosphere"
- **candlelit-gothic**: "Warm flickering candlelight, deep dramatic shadows, intimate glow"
# Can combine any style + palette + mood + lighting
```

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

When analyzing an image, describe what you observe:

**Colors:**
- Identify 3-5 dominant colors
- Note if warm or cool overall
- Extract approximate hex codes
- Describe color relationships (complementary, analogous, monochromatic)

**Lighting:**
- Direction: front, side, back, top, ambient
- Quality: hard (sharp shadows) or soft (diffused)
- Color temperature: warm, neutral, cool
- Contrast level: high contrast or low contrast

**Composition:**
- Subject placement (centered, off-center, rule of thirds)
- Depth (shallow DOF, deep focus, layered)
- Framing (tight, medium, wide)
- Angle (eye level, low, high, dutch)

**Medium/Technique:**
- Photography, illustration, painting, 3D, mixed
- If photography: film vs digital feel, grain, processing
- If illustration: style (flat, detailed, sketchy)
- Texture quality: smooth, grainy, textured

**Mood:**
- Emotional impression (peaceful, tense, joyful, mysterious)
- Atmosphere (intimate, expansive, claustrophobic)
- Energy level (calm, dynamic, chaotic)

### From Text/URLs

Scan for these patterns:

**Direct style mentions:**
- "in the style of [artist/movement]"
- "[medium] aesthetic"
- "inspired by [reference]"

**Color language:**
- Named colors: "terracotta", "sage", "midnight blue"
- Hex codes: #XXXXXX
- Color moods: "earthy", "neon", "muted"

**Atmosphere words:**
- Lighting: "golden hour", "harsh shadows", "soft glow"
- Mood: "dreamy", "gritty", "ethereal", "cozy"
- Era: "vintage", "futuristic", "retro 80s"

## Examples

### From Image

```
/capture-trends ./inspiration/moody-portrait.jpg --name=dark-editorial

## Trend Extraction: moody-portrait.jpg

**Source:** ./inspiration/moody-portrait.jpg
**Detected type:** Image (JPEG)

### Extracted Elements

| Category | Found |
|----------|-------|
| Colors | #1A1A2E (deep navy), #E8D5B7 (warm skin), #4A4A6A (muted purple) |
| Lighting | Single key light from camera left, strong shadows on right side |
| Medium | Studio photography, possibly film |
| Mood | Contemplative, intimate, slightly melancholic |
| Composition | Tight crop, negative space on shadow side, eye-level |

### Generated Preset

**Name:** `dark-editorial`
**Category:** `lighting`

"Low-key portrait lighting, single dramatic side light from left, deep
shadows obscuring half the face, desaturated color palette with warm
skin tones against deep navy #1A1A2E background, shallow depth of field,
editorial photography style with subtle film grain, contemplative mood"

✓ Added `dark-editorial` to style-library.md under `lighting`
```

### From Multi-Trend Document (PDF/Report)

```
/capture-trends ./docs/Pinterest-Predicts-2026.pdf --modular

## Trend Extraction: Pinterest Predicts 2026

**Source:** ./docs/Pinterest-Predicts-2026.pdf
**Detected type:** PDF (24 pages)
**Document type:** Multi-trend report (21 distinct trends detected)

### Detected Trends

1. Cool Blue - Subzero sophistication
2. Vamp Romantic - Gothic romance
3. Neo Deco - Art deco revival
... (18 more)

**How should I proceed?**
1. Extract all 21 trends as separate presets
2. Pick specific trends to extract
3. Extract first 5 as examples

> User: Extract all, make it modular

### Extracted to style-library.md (1:1:1:1 complete)

**Art Styles (21 presets):** one per trend
- cool-blue, vamp-romantic, pen-pals, glamoratti, wilderkind...

**Color Palettes (21 presets):** one per trend
- icy-subzero, vamp-darks, postal-vintage, gilded-luxe, moss-forest...

**Moods (21 presets):** one per trend
- icy-sophistication, haunting-melancholy, nostalgic-intimacy, bold-decadence...

**Lighting (21 presets):** one per trend
- icy-crisp, candlelit-gothic, window-warmth, studio-glamour, dappled-forest...

✓ Created modular style library with 84 mix-and-match presets (21 × 4 categories)

**Usage:**
/image-prompt portrait --style=vamp-romantic --palette=icy-subzero --mood=bold-confidence
```

### From Single-Style URL

```
/capture-trends https://example.com/moody-portrait-tutorial --name=moody-portrait

## Trend Extraction: moody-portrait-tutorial

**Source:** https://example.com/moody-portrait-tutorial
**Detected type:** Web article
**Document type:** Single style (not multi-trend)

### Extracted Elements

| Category | Found |
|----------|-------|
| Colors | "Deep shadows", "warm skin tones", "dark background" |
| Lighting | "Single key light", "dramatic side lighting" |
| Medium | "Editorial photography" |
| Mood | "Contemplative", "intimate" |

### Generated Preset

**Name:** `moody-portrait`
**Category:** `art-styles`

"Editorial portrait photography, single dramatic side light, deep shadows
on opposite side, warm skin tones against dark background, shallow depth
of field, contemplative intimate mood"

✓ Added `moody-portrait` to style-library.md under `art-styles`
```

### With --merge

```
/capture-trends ./ref2.jpg --name=dark-editorial --merge

Existing preset `dark-editorial`:
"Low-key portrait lighting, single dramatic side light..."

New extraction adds:
- Color: #8B4513 (warm brown accent)
- Detail: "catchlight in eyes"

Merged preset `dark-editorial`:
"Low-key portrait lighting, single dramatic side light from left, deep
shadows, desaturated palette with teal #264653, burnt orange #E76F51,
and warm brown #8B4513 accents, catchlight in eyes, shallow depth of
field, editorial photography style, contemplative mood"

✓ Updated `dark-editorial` in style-library.md
```

## Integration

### With /style-library

Extracted presets are saved in the same format `/style-library` manages:
```markdown
- **preset-name**: "Full style definition here"
```

### With /project-setup

When in a project folder with `references/` directory:
- Suggest running `/capture-trends` on reference images
- Auto-populate `style-library.md` with project-relevant presets

### With /image-prompt

After capturing a trend:
```
Style captured! Try: /image-prompt [your concept] --style=[preset-name]
```

## Error Handling

| Situation | Response |
|-----------|----------|
| URL unreachable | "Could not fetch URL. Check the link and try again." |
| Image not found | "File not found: [path]. Check the path is correct." |
| Unsupported format | "Unsupported file type. Supported: PNG, JPG, WEBP, GIF, PDF, MD" |
| Empty extraction | "Could not extract meaningful style information. Try a different source." |
| Preset exists (no --merge) | "Preset `[name]` already exists. Use `--merge` to combine, or choose a different name." |
