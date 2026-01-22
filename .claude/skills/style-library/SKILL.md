---
name: style-library
description: Manage style presets for consistent image generation. Use when
  user wants to save a style, apply a preset, list available styles, or
  maintain brand consistency. Creates/updates style-library.md.
argument-hint: "[add|list|apply|remove] [preset-name] [style definition] [--root] [--project=path]"
---

# Style Library

Manage reusable style presets for consistent image generation. Creates and maintains `style-library.md`.

## Project Context Detection

This skill is project-aware and determines which `style-library.md` to use:

### Detection Priority

1. **`--project=<path>` flag** → Use `<path>/style-library.md`
2. **`--root` flag** → Use repository root `style-library.md`
3. **Current directory has project markers** → Use current project's `style-library.md`
4. **Parent directory has project markers** → Use that project's `style-library.md`
5. **No project context** → Use repository root `style-library.md`

### Project Markers

A directory is considered a "project" if it contains ANY of:
- `style-guide.md`
- `style-library.md`
- `outputs/` directory
- `references/` directory

### Inheritance Model

```
root/style-library.md          ← Global presets (available to all projects)
    │
    ├── project-a/style-library.md   ← Project-specific + inherits root
    │
    └── project-b/style-library.md   ← Project-specific + inherits root
```

When **listing** presets:
- Show project presets first (if in project)
- Then show root presets marked as "(inherited)"

When **applying** a preset:
- First check project `style-library.md`
- Then check root `style-library.md`
- Project presets override root presets of the same name

### Examples

```bash
# In demo-campaign/ → uses demo-campaign/style-library.md
/style-library list

# Force use root style-library.md
/style-library list --root

# Target specific project from anywhere
/style-library add my-style "..." --project=demo-campaign

# Add to root (global) style library
/style-library add shared-style "..." --root
```

## Operations

| Command | Usage | Description |
|---------|-------|-------------|
| `add` | `/style-library add <name> "<definition>"` | Add or update a preset |
| `list` | `/style-library list [category]` | Show all presets or filter by category |
| `apply` | `/style-library apply <name>` | Output preset text for use |
| `remove` | `/style-library remove <name>` | Delete a preset |
| `import` | `/style-library import <category> <file>` | Import preset from external file |

## Categories

Organize presets into these categories:

| Category | Purpose | Example presets |
|----------|---------|-----------------|
| `art-styles` | Visual mediums and techniques | cinematic, flat-vector, watercolor, pixel-art |
| `color-palettes` | Color schemes and moods | warm-earth, neon-noir, pastel-soft, monochrome |
| `lighting` | Lighting setups and moods | golden-hour, dramatic-side, soft-diffused, rim-lit |
| `characters` | Recurring character descriptions | protagonist, sidekick, villain |
| `compositions` | Framing and layout patterns | hero-shot, symmetrical, rule-of-thirds |
| `moods` | Emotional atmosphere | cozy, tense, ethereal, gritty |

## File Format

The `style-library.md` file uses this structure:

```markdown
# Style Library

## Art Styles

- **cinematic**: "Cinematic lighting, anamorphic lens flare, film grain, dramatic shadows, 2.39:1 aspect ratio feel"
- **flat-vector**: "Flat vector illustration, bold colors, clean lines, no gradients, geometric shapes"
- **watercolor**: "Soft watercolor painting, visible brushstrokes, paper texture, colors bleeding at edges, organic shapes"

## Color Palettes

- **warm-earth**: "Warm earth tones: terracotta #E07A5F, cream #F4F1DE, sage #81B29A, soft shadows"
- **neon-noir**: "Neon-noir palette: deep black #0D0D0D, electric cyan #00FFFF, hot magenta #FF00FF, rain-slicked reflections"

## Lighting

- **golden-hour**: "Golden hour lighting, warm amber tones, long soft shadows, backlit subjects with rim light"
- **dramatic-side**: "Single dramatic side light, deep shadows, high contrast, moody atmosphere"

## Characters

- **luna**: "Luna, a red-haired pilot with bright green goggles pushed up on her forehead, weathered brown leather jacket with brass buttons, confident expression, freckles across her nose"

## Compositions

- **hero-shot**: "Low angle hero shot, subject dominant in frame, dramatic sky background, strong silhouette"

## Moods

- **cozy**: "Cozy atmosphere, warm interior lighting, soft textures, inviting environment, comfort and safety"
```

## Process by Command

### ADD

1. Parse: `/style-library add <name> "<definition>"`
2. Detect or ask for category based on content
3. Check if `style-library.md` exists
   - If no: create file with starter template
   - If yes: read existing content
4. Add or update the preset under appropriate category
5. Write updated file
6. Confirm: "Added `<name>` to `<category>`"

**Example:**
```
/style-library add vintage-photo "Vintage photograph style, faded colors, light leaks, soft vignette, film grain, slightly overexposed highlights"

→ Added `vintage-photo` to `art-styles`
```

### LIST

1. Parse: `/style-library list [category]`
2. Read `style-library.md`
   - If not found: "No style library found. Use `/style-library add` to create one."
3. Display presets
   - If category specified: show only that category
   - If no category: show all, grouped by category

**Output format:**
```
## Style Library

### Art Styles (4 presets)
- cinematic
- flat-vector
- watercolor
- pixel-art

### Color Palettes (2 presets)
- warm-earth
- neon-noir

### Characters (1 preset)
- luna

Use `/style-library apply <name>` to see full definition.
```

### APPLY

1. Parse: `/style-library apply <name>`
2. Read `style-library.md`
3. Find preset by name (case-insensitive)
   - If not found: suggest similar names or list available
4. Output the full definition for copy/paste

**Output format:**
```
## cinematic

"Cinematic lighting, anamorphic lens flare, film grain, dramatic shadows, 2.39:1 aspect ratio feel"

Copy this text to append to your image prompt, or use with `/enhance-prompt --style=cinematic`
```

### REMOVE

1. Parse: `/style-library remove <name>`
2. Read `style-library.md`
3. Find and remove the preset
4. Write updated file
5. Confirm: "Removed `<name>` from style library"

### IMPORT

1. Parse: `/style-library import <category> <file-path>`
2. Read the external file (markdown, text, or image)
3. If image: analyze for style characteristics (colors, lighting, technique)
4. Extract or generate a style definition
5. Add to specified category in `style-library.md`

**From markdown/text file:**
```
/style-library import characters ./references/hero-design.md

→ Imported character description as `hero-design` in characters
```

**From image:**
```
/style-library import art-styles ./references/mood-reference.jpg

→ Analyzed image. Extracted style:
"Moody low-key lighting, desaturated teal and orange color grade, shallow depth of field, cinematic grain, contemplative atmosphere"

Added as `mood-reference` in art-styles
```

## Starter Template

When creating a new `style-library.md`, use this starter:

```markdown
# Style Library

A collection of reusable style presets for consistent image generation.

## Art Styles

- **cinematic**: "Cinematic lighting, anamorphic lens flare, film grain, dramatic shadows, 2.39:1 aspect ratio feel"
- **flat-vector**: "Flat vector illustration, bold colors, clean lines, no gradients, geometric shapes"

## Color Palettes

- **warm-earth**: "Warm earth tones: terracotta #E07A5F, cream #F4F1DE, sage #81B29A, soft natural lighting"

## Lighting

- **golden-hour**: "Golden hour lighting, warm amber tones, long soft shadows, backlit rim light"

## Characters

<!-- Add character presets here -->

## Compositions

- **hero-shot**: "Low angle hero shot, subject dominant in frame, dramatic sky background"

## Moods

- **cozy**: "Cozy atmosphere, warm interior lighting, soft textures, inviting and comfortable"
```

## Integration with Other Skills

### With /enhance-prompt

When `/enhance-prompt --style=<preset>` is used:
1. Read `style-library.md`
2. Find the preset
3. Append the style definition to the enhanced prompt

### With /image-prompt

The master skill checks for `style-library.md` and:
1. Offers style suggestions based on the user's concept
2. Applies styles when `--style=<preset>` is specified
3. Shows available presets when user asks about styles

### With /project-setup

When a project is scaffolded:
1. Creates `style-library.md` with starter content
2. Pre-fills with any styles mentioned during setup interview

### With /capture-trends

Extracted trends are saved to `style-library.md` in the appropriate category.

## Best Practices for Preset Definitions

**Good presets are:**
- Specific: Use concrete descriptors, not vague words
- Composable: Work well when combined with other elements
- Complete: Address lighting, color, texture, mood
- Reusable: Applicable to different subjects

**Example of a well-crafted preset:**
```
- **noir-detective**: "High contrast black and white, single harsh light source from venetian blinds,
  deep shadows obscuring half the scene, cigarette smoke catching light, 1940s film noir atmosphere,
  slight film grain"
```

**Avoid:**
```
- **cool-style**: "Looks cool, very artistic, nice colors"  ← Too vague
```

## Error Handling

| Situation | Response |
|-----------|----------|
| File not found | "No style library found. Create one with `/style-library add <name> \"<definition>\"`" |
| Preset not found | "Preset `<name>` not found. Available presets: [list]. Did you mean `<similar>`?" |
| Invalid category | "Unknown category `<cat>`. Valid categories: art-styles, color-palettes, lighting, characters, compositions, moods" |
| Duplicate name | "Preset `<name>` already exists. Use `/style-library add` to update it." |
