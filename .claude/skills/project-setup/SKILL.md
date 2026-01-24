---
name: project-setup
version: 1.1.0
description: Scaffold an image generation project with style guide, references,
  and output directories. Use when starting a new visual project, brand work,
  or any multi-image effort requiring consistency. Creates project structure
  and style-guide.md template.
argument-hint: "[project-name] [--type=brand|campaign|character|product] [--quick] [--dry-run] [--lock] [--unlock]"
---

# Project Setup

Scaffold a complete image generation project with style guide, directories, and templates for consistent visual output.

## Generated Structure

```
project-name/
├── style-guide.md           # AI-ready style guide (filled template)
├── style-library.md         # Presets extracted from style guide
├── references/
│   ├── moodboards/          # Visual direction
│   ├── characters/          # Character sheets
│   └── inspiration/         # Reference images
├── outputs/
│   ├── exploration/         # Work in progress
│   └── finals/              # Approved assets
└── asset-log.md             # Generation metadata tracking
```

## Style Guide Versioning

Every generated `style-guide.md` includes a version header:

```markdown
---
version: 1.0.0
created: 2026-01-23
modified: 2026-01-23
locked: false
---
```

### Version Semantics

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Breaking (palette, core style) | Major (1.0 → 2.0) | Changed brand colors |
| Additive (new elements) | Minor (1.0 → 1.1) | Added character styles |
| Clarification (wording) | Patch (1.0.0 → 1.0.1) | Fixed typo |

### Locking

Lock style guides during active campaigns with `--lock` / `--unlock`. When locked:
- `/image-prompt` reads but cannot trigger style updates
- `/capture-trends --guide` warns before modifying
- Manual edits show warning in git diff

Changes are tracked in `style-guide-history.md`.

## Project Types

| Type | Focus | Extra content |
|------|-------|---------------|
| `brand` | Visual identity | Color system section, typography notes, logo usage guidelines |
| `campaign` | Marketing assets | Moodboard template, shot list, deliverables checklist |
| `character` | Character design | Character sheet template, pose library section, expression guide |
| `product` | Product photography | Lighting setup notes, background options, angle guide |

## Process

### Step 1: Parse Input

Parse project name and type from command (e.g., `/project-setup my-brand --type=brand`).

**Flags:**

| Flag | Effect |
|------|--------|
| `--quick` | Skip interview, use defaults below |
| `--dry-run` | Preview structure without creating files |
| `--lock` | Lock style-guide.md (see [Locking](#locking)) |
| `--unlock` | Unlock style-guide.md for editing |

**Quick Mode Defaults:**

| Parameter | Default |
|-----------|---------|
| Project Type | `brand` |
| Visual Style | "clean and modern" |
| Color Preferences | "neutral palette with one accent color" |
| Reference Medium | Photography |

When `--type` is also provided, only that parameter is set—others use defaults.

**Quick Vibe Presets:**

For even faster setup, use `--quick=<vibe>`:

| Preset | Style | Colors | Feeling |
|--------|-------|--------|---------|
| `--quick=cozy` | Warm, inviting | Earth tones, warm neutrals | Like a favorite cafe |
| `--quick=minimal` | Clean, modern | White, black, one accent | Calm confidence |
| `--quick=bold` | High contrast | Saturated, vibrant | Attention-grabbing |
| `--quick=dreamy` | Soft, ethereal | Pastels, soft focus | Nostalgic, romantic |

**Usage:**
```bash
/project-setup my-brand --quick=cozy
/project-setup portfolio --quick=minimal --type=brand
```

### Step 2: Interactive Interview (if details missing)

Ask these questions to gather project requirements:

| # | Question | Why We Ask | Example Answers |
|---|----------|-----------|-----------------|
| 1 | What's your project called? | Creates your folder | `coastal-retreat`, `my-brand` |
| 2 | What are you making? | Customizes templates | brand / campaign / character / product |
| 3 | What vibe are you going for? | Sets the mood | "cozy coffee shop", "clean tech startup" |
| 4 | What colors feel right? | Defines your palette | "earthy and warm", "bold neons" |
| 5 | Real photos or artistic? | Guides the AI | photography / illustration / 3D / mixed |
| 6 | What should this NOT look like? | Prevents mistakes | "not corporate", "avoid stock photo vibes" |

### Step 3: Generate Structure

Create all directories and files based on answers, then show what was created and suggest next steps.

## File Templates

### style-guide.md

```markdown
# [Project Name] Style Guide

> AI-ready style guide for consistent image generation

## Overview

**Project:** [name]
**Type:** [brand|campaign|character|product]
**Created:** [date]

## Visual Direction

### Style Summary
[User's style description from interview]

### Mood Keywords
- [keyword 1]
- [keyword 2]
- [keyword 3]

## Color Palette

### Primary Colors
| Name | Hex | Usage |
|------|-----|-------|
| [Color 1] | #XXXXXX | Primary backgrounds, main elements |
| [Color 2] | #XXXXXX | Accents, highlights |
| [Color 3] | #XXXXXX | Text, shadows |

### Color Mood
[User's color preference from interview]

## Visual Medium

**Primary:** [Photography | Illustration | 3D Render]

### Medium Details
- Lighting style: [to be defined]
- Texture preference: [to be defined]
- Level of detail: [to be defined]

## Constraints & Avoidances

### Do Not Use
- [Constraint from interview, e.g., "corporate blue tones"]
- [Additional constraint]

### Avoid Looking Like
- [Competitor or style to differentiate from]

### Technical Restrictions
- No text in generated images (unless explicitly needed)
- Avoid [specific elements that don't fit brand]

### Quality Guardrails
- Reject images with: [artifacts, wrong colors, off-brand elements]

## Prompt Patterns

### Base Prompt Template
```
[Subject description]. [Action/pose]. [Location/environment].
[Style from this guide]. [Color palette: primary colors].
[Medium: photography/illustration/3D]. [Composition notes].
```

### Prompt Do's
- Use specific, descriptive language
- Reference the color palette by name
- Maintain consistent lighting across assets
- Include constraint reminders: "avoid [constraint]"

### Prompt Don'ts
- Avoid generic quality words (4k, masterpiece, best quality)
- Don't mix incompatible styles
- Avoid keyword spam
- Never include elements from "Do Not Use" list above

## Asset Requirements

### Dimensions
- Primary: [to be defined]
- Social: [to be defined]
- Print: [to be defined]

### File Naming
`[project]-[asset-type]-[version]-[date].[ext]`

Example: `mybrand-hero-v2-20260121.png`

---

*Use this guide with `/image-prompt --style=project` to maintain consistency*
```

### style-library.md (Starter)

```markdown
# Style Library

Presets for [Project Name]. Use with `--style=preset-name`.

## Ready-to-Use Presets

These work immediately. Copy and customize for your project.

### Vibes

- **cozy**: "Warm intimate atmosphere. Soft textures, natural materials, golden lighting. Feels like a favorite coffee shop or well-loved home. Rich shadows, inviting spaces."

- **minimal**: "Clean and uncluttered. Lots of white space, simple forms, precise geometry. Calm and confident. No decoration for decoration's sake."

- **bold**: "High contrast, saturated colors, strong shapes. Confident and attention-grabbing. Makes a statement. Not subtle."

- **dreamy**: "Soft focus, pastel colors, ethereal quality. Slightly hazy atmosphere. Romantic and nostalgic. Like a memory or daydream."

- **editorial**: "Magazine-quality polish. Intentional composition, sophisticated color grading. Looks professionally art-directed."

### Color Moods

- **earthy**: "Terracotta, sage green, warm browns, cream. Natural and grounded. Avoid pure black or neon."

- **monochrome**: "Single color in multiple shades. Sophisticated and cohesive. Add one accent color sparingly."

- **sunset**: "Warm oranges, pinks, deep purples. Golden hour warmth. Rich and atmospheric."

- **ocean**: "Deep blues, seafoam, sandy beige, coral accents. Fresh but not tropical-tacky."

### Lighting

- **golden-hour**: "Warm side lighting, long shadows. Magic hour feeling. Soft and flattering."

- **studio-soft**: "Even, diffused lighting. Minimal shadows. Clean and professional."

- **dramatic**: "Single strong light source. Deep shadows, high contrast. Moody and cinematic."

### Compositions

- **centered**: "Subject dead center. Bold and direct. Works for portraits and product hero shots."

- **rule-of-thirds**: "Subject offset. Creates visual flow. More dynamic than centered."

- **negative-space**: "Generous empty areas. Subject small in frame. Elegant and airy."

## Your Project Presets

Customize these for [Project Name]:

- **project-main**: "[Describe your core visual style here]"
- **project-colors**: "[Your color palette description]"
- **project-mood**: "[The feeling your brand evokes]"
```

### asset-log.md

```markdown
# Asset Log

Track all generated assets for [Project Name]

| Date | Asset | Prompt Summary | Tool Used | Status | Approval | File |
|------|-------|----------------|-----------|--------|----------|------|
| | | | | | | |

## Status Key
- **exploration** — Work in progress, testing ideas
- **review** — Ready for feedback
- **approved** — Internal approval
- **client-approved** — External sign-off
- **archived** — Not using, kept for reference

## Approval Notes

| Asset | Version | Note | Date |
|-------|---------|------|------|
| | | | |

*Use approval notes to track revision feedback and sign-off history*
```

## Type-Specific Additions

### Brand Type

Add to style-guide.md:

```markdown
## Brand Elements

### Logo Usage
- Minimum clear space: [to be defined]
- Minimum size: [to be defined]
- Background restrictions: [to be defined]

### Typography (for reference)
- Headlines: [font family]
- Body: [font family]
- Accent: [font family]

### Brand Voice (visual)
- [Adjective 1]
- [Adjective 2]
- [Adjective 3]
```

### Campaign Type

Add to style-guide.md:

```markdown
## Campaign Details

### Deliverables Checklist
- [ ] Hero image
- [ ] Social media set (IG, FB, Twitter)
- [ ] Banner ads (various sizes)
- [ ] Email header

### Shot List
| # | Description | Aspect Ratio | Priority |
|---|-------------|--------------|----------|
| 1 | | | |
| 2 | | | |

### Moodboard Notes
See `/references/moodboards/` for visual direction
```

### Character Type

Add to style-guide.md:

```markdown
## Character Details

### Character Sheet Template

**Name:** [Character name]

**Physical Description:**
- Age:
- Build:
- Hair:
- Eyes:
- Distinguishing features:

**Clothing/Equipment:**
- Default outfit:
- Accessories:

**Personality Indicators:**
- Expression tendency:
- Posture:
- Gestures:

### Required Poses
- [ ] Front view (neutral)
- [ ] 3/4 view
- [ ] Profile
- [ ] Action pose
- [ ] Expression sheet

### Expression Guide
- Neutral
- Happy
- Determined
- Surprised
- Angry
```

### Product Type

Add to style-guide.md:

```markdown
## Product Photography

### Lighting Setups
| Setup | Description | Use Case |
|-------|-------------|----------|
| Hero | Dramatic single key light | Main product shots |
| Soft | Diffused even lighting | Detail shots |
| Lifestyle | Natural/ambient | Context shots |

### Background Options
- **Seamless white**: Clean, e-commerce style
- **Gradient**: Subtle depth, premium feel
- **Contextual**: In-use environment
- **Textured**: Material backdrop (wood, marble)

### Angle Guide
- Eye level: Standard view
- High angle: Overview, shows top
- Low angle: Dramatic, premium
- Flat lay: Top-down, arrangement
- Detail: Macro, texture focus
```

## Output Format

After scaffolding, display created structure with checkmarks, next steps (add references, customize style-guide, start generating), and a quick start command. See [Example Session](#example-session).

## Integration with Other Skills

This skill creates files that other skills detect and use:

| File Created | Used By | How |
|--------------|---------|-----|
| `style-library.md` | `/enhance-prompt --style=`, `/image-prompt --style=`, `/style-library` | Loads presets by name |
| `style-guide.md` | `/image-prompt` | Reads for constraints and brand context |
| `references/` | `/image-prompt --refs=`, `/capture-trends` | Source for reference images and style extraction |
| `outputs/` | `/image-prompt` | Default save location for generated images |
| `asset-log.md` | `/image-prompt` | Appends generation metadata after each image |

### Related Skills

| Skill | Relationship |
|-------|--------------|
| `/quickstart` | Routes new users here for multi-image projects |
| `/capture-trends` | Populates style-library.md from reference images |
| `/style-library` | Manages presets created by this skill |
| `/image-prompt` | Primary consumer of project structure |

## Example Session

```
User: /project-setup
Claude: What's the project name?
User: coastal-retreat-brand
Claude: What type of project? (brand/campaign/character/product)
User: brand
Claude: Visual style direction?
User: serene, natural, upscale coastal living
Claude: Color preferences?
User: ocean blues, sandy beiges, weathered white, touches of coral
Claude: Visual medium? (photography/illustration/3D/mixed)
User: photography
Claude: Anything to avoid?
User: no tropical/tacky beach vibes, avoid neon colors

Claude:
## Project Created: coastal-retreat-brand
✓ style-guide.md, style-library.md (5 presets), asset-log.md
✓ references/{moodboards,characters,inspiration}/
✓ outputs/{exploration,finals}/

Next: Add references → customize style-guide.md → `/image-prompt`
```

**Quick mode:** `/project-setup summer-campaign --type=campaign --quick` creates the same structure with defaults applied (style: "clean and modern", colors: "neutral with accent", medium: photography).

## Error Handling

| Situation | Response |
|-----------|----------|
| Directory exists | "Project `[name]` already exists. Use a different name or delete the existing folder." |
| Invalid type | "Unknown type `[type]`. Valid types: brand, campaign, character, product" |
| No write permission | "Cannot create project here. Check folder permissions." |
| Nothing to update | "Project `[name]` is already complete. No changes needed." |

## Subcommands

### /project-setup validate

Check project structure integrity: `/project-setup validate [./path]`

| Check | Pass | Fail |
|-------|------|------|
| style-guide.md exists | ✓ Found | ⚠ Missing — run `/project-setup` |
| style-library.md exists | ✓ Found | ⚠ Missing — will use root library |
| outputs/ directory | ✓ Found | ⚠ Missing — created on first generation |
| references/ directory | ✓ Found | ℹ Missing (optional) |
| asset-log.md exists | ✓ Found | ⚠ Missing — create for tracking |
| style-guide.md customized | ✓ Populated | ⚠ Template only |
| style-library.md has presets | ✓ Has presets | ℹ Empty — use `/capture-trends` |

**States:** ✓ Ready | ⚠ Needs attention | ✗ Not a project

### /project-setup update

Refresh structure while preserving customizations: `/project-setup update [./path]`

| Item | Action |
|------|--------|
| Missing directories/files | Create with template |
| Existing style-guide.md | **Preserve** (never overwrite) |
| Existing style-library.md | **Merge** new presets, keep existing |
| Existing asset-log.md | **Preserve** (never overwrite) |

Reports what was added, preserved, and already exists.
