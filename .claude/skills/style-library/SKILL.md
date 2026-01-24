---
name: style-library
description: Manage style presets for consistent image generation. Use when
  user wants to save a style, apply a preset, list available styles, or
  maintain brand consistency. Creates/updates style-library.md.
argument-hint: "[add|list|apply|remove] [preset-name] [style definition] [--root] [--project=path]"
---

# Style Library

Manage reusable style presets for consistent image generation.

## Project Context Detection

Determines which `style-library.md` to use, in priority order:

1. `--project=<path>` flag - Use specified path
2. `--root` flag - Use repository root
3. Current/parent directory with project markers - Use that project's file
4. Default - Use repository root

**Project markers**: `style-guide.md`, `style-library.md`, `outputs/`, `references/`

### Inheritance Model

```
root/style-library.md              <- Global presets (available everywhere)
    ├── project-a/style-library.md <- Inherits root, can override
    └── project-b/style-library.md <- Inherits root, can override
```

- **List**: Shows project presets first, then root presets marked "(inherited)"
- **Apply**: Checks project first, then root; project presets override root

## Operations

| Command | Usage | Description |
|---------|-------|-------------|
| `add` | `add <name> "<definition>"` | Add or update a preset |
| `list` | `list [category]` | Show all presets or filter by category |
| `apply` | `apply <name>` | Output preset for use |
| `remove` | `remove <name>` | Delete a preset |
| `import` | `import <category> <file>` | Import from file or image |

## Categories

| Category | Purpose | Examples |
|----------|---------|----------|
| `art-styles` | Visual mediums/techniques | cinematic, flat-vector, watercolor |
| `color-palettes` | Color schemes | warm-earth, neon-noir, pastel-soft |
| `lighting` | Lighting setups | golden-hour, dramatic-side, rim-lit |
| `characters` | Recurring characters | protagonist, sidekick, villain |
| `compositions` | Framing patterns | hero-shot, symmetrical, rule-of-thirds |
| `moods` | Emotional atmosphere | cozy, tense, ethereal, gritty |

## File Format

```markdown
# Style Library

## Art Styles

- **cinematic**: "Cinematic lighting, anamorphic lens flare, film grain, dramatic shadows"
- **flat-vector**: "Flat vector illustration, bold colors, clean lines, no gradients"

## Color Palettes

- **warm-earth**: "Warm earth tones: terracotta #E07A5F, cream #F4F1DE, sage #81B29A"

## Lighting

- **golden-hour**: "Golden hour lighting, warm amber tones, long soft shadows, backlit rim light"

## Characters

- **luna**: "Red-haired pilot with green goggles, weathered brown leather jacket, confident expression"

## Compositions

- **hero-shot**: "Low angle hero shot, subject dominant in frame, dramatic sky background"

## Moods

- **cozy**: "Cozy atmosphere, warm interior lighting, soft textures, inviting environment"
```

## Command Details

### ADD

1. Parse `add <name> "<definition>"`
2. Detect or ask for category
3. Create `style-library.md` if missing (use template above)
4. Add/update preset under appropriate category
5. Confirm: "Added `<name>` to `<category>`"

### LIST

1. Parse `list [category]`
2. If file missing: prompt to create with `add`
3. Display presets grouped by category (or filtered if category specified)
4. Show: "Use `/style-library apply <name>` for full definition"

### APPLY

1. Parse `apply <name>`
2. Find preset (case-insensitive)
3. If not found: suggest similar names
4. Output full definition for copy/paste

### REMOVE

1. Parse `remove <name>`
2. Find and remove preset
3. Confirm: "Removed `<name>` from style library"

### IMPORT

1. Parse `import <category> <file-path>`
2. For images: analyze style characteristics (colors, lighting, technique)
3. For text/markdown: extract description
4. Add to specified category

## Integration

| Skill | Integration |
|-------|-------------|
| `/enhance-prompt` | `--style=<preset>` appends style definition to prompt |
| `/image-prompt` | Offers style suggestions, applies `--style=<preset>` |
| `/project-setup` | Creates starter `style-library.md` |
| `/capture-trends` | Saves extracted trends to appropriate category |

## Best Practices

**Good presets are**: specific, composable, complete (lighting/color/texture/mood), reusable

```markdown
# Good - specific and complete
- **noir-detective**: "High contrast B&W, harsh light through venetian blinds, deep shadows, cigarette smoke, 1940s film noir, slight grain"

# Bad - too vague
- **cool-style**: "Looks cool, very artistic, nice colors"
```

## Error Handling

| Situation | Response |
|-----------|----------|
| File not found | Prompt to create with `add` |
| Preset not found | Suggest similar names, list available |
| Invalid category | List valid categories |
| Duplicate name | Inform preset will be updated |
