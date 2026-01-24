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
| `--minimal` | Create only style-guide.md (no folders) |
| `--lock` | Lock style-guide.md (see [Locking](#locking)) |
| `--unlock` | Unlock style-guide.md for editing |

**Minimal Mode (`--minimal`):**

Creates only `style-guide.md`—no folders. Useful for experiments or adding AI generation to existing projects. Folders are created on first image generation.

**Dry Run (`--dry-run`):**

```
> /project-setup coastal-brand --type=brand --dry-run

Preview: coastal-brand

Would create:
├── style-guide.md (brand template)
├── style-library.md (15 starter presets)
├── asset-log.md
├── references/{moodboards,characters,inspiration}/
└── outputs/{exploration,finals}/

Run without --dry-run to create.
```

**Quick Mode Defaults:**

| Parameter | Default |
|-----------|---------|
| Project Type | `brand` |
| Visual Style | "clean and modern" |
| Color Preferences | "neutral palette with one accent color" |
| Reference Medium | Photography |

When `--type` is also provided, only that parameter is set—others use defaults.

**Quick Vibe Presets:**

Use `--quick=<vibe>` for instant styling: `cozy`, `minimal`, `bold`, `dreamy`, `editorial`. These map directly to the Vibes section in `style-library.md`.

```bash
/project-setup my-brand --quick=cozy
/project-setup portfolio --quick=minimal --type=brand
```

### Step 2: Interactive Interview (if details missing)

Ask these questions to gather project requirements:

| # | Question | Example Answers |
|---|----------|-----------------|
| 1 | What's your project called? | `coastal-retreat`, `my-brand` |
| 2 | What are you making? | brand / campaign / character / product |
| 3 | What vibe are you going for? | "cozy coffee shop", "clean tech startup" |
| 4 | What colors feel right? | "earthy and warm", "bold neons" |
| 5 | Real photos or artistic? | photography / illustration / 3D / mixed |
| 6 | What should this NOT look like? | "not corporate", "avoid stock photo vibes" |

### Step 3: Generate Structure

Create all directories and files based on answers, then show what was created and suggest next steps.

### Step 4: First Image (Optional)

After structure creation, offer a sample image:

```
Structure created! Test your style with a sample image?
1. Yes - Generate a test image
2. No - I'll add references first
3. Show me a prompt for later
```

| Choice | Action |
|--------|--------|
| Yes | Generate "[project-type subject] in [user's style]" → save to `outputs/exploration/first-test.png` |
| Show prompt | Display a ready-to-copy prompt with explanation |

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

## Vibes

- **cozy**: "Warm intimate atmosphere. Soft textures, golden lighting, inviting spaces."
- **minimal**: "Clean, uncluttered. White space, simple forms, calm confidence."
- **bold**: "High contrast, saturated colors, strong shapes. Attention-grabbing."
- **dreamy**: "Soft focus, pastels, ethereal. Nostalgic, like a memory."
- **editorial**: "Magazine polish. Intentional composition, sophisticated grading."

## Color Moods

- **earthy**: "Terracotta, sage, warm browns, cream. Natural, grounded."
- **monochrome**: "Single color in multiple shades. One accent sparingly."
- **sunset**: "Warm oranges, pinks, deep purples. Golden hour warmth."
- **ocean**: "Deep blues, seafoam, sandy beige, coral. Fresh, not tacky."

## Lighting

- **golden-hour**: "Warm side lighting, long shadows. Soft and flattering."
- **studio-soft**: "Even, diffused. Minimal shadows, professional."
- **dramatic**: "Single strong source. Deep shadows, cinematic."

## Compositions

- **centered**: "Subject dead center. Bold, direct."
- **rule-of-thirds**: "Subject offset. Creates visual flow."
- **negative-space**: "Generous empty areas. Elegant and airy."

## Your Project Presets

- **project-main**: "[Your core visual style]"
- **project-colors**: "[Your color palette]"
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

Claude: What's your project called? (This creates your folder)

User: coastal-retreat

Claude: What are you making?
• brand - Visual identity (logos, colors, the whole look)
• campaign - Marketing stuff (ads, social posts)
• character - Characters/mascots
• product - Product photography

User: brand

Claude: What vibe are you going for? Describe it like you'd tell a friend.

User: serene, natural, upscale coastal living - think expensive beach house, not spring break

Claude: What colors feel right?

User: ocean blues, sandy beiges, weathered white, maybe touches of coral

Claude: Real photos or more artistic?
• photography - Realistic images
• illustration - Artistic/drawn style
• 3D - Digital renders
• mixed - Whatever fits

User: photography

Claude: Last one - what should this NOT look like? Any styles to avoid?

User: no tropical/tacky beach vibes, nothing that looks like a generic resort ad

Claude:
## Created: coastal-retreat/

✓ style-guide.md - Your brand rules (customized with your answers)
✓ style-library.md - 15 ready-to-use presets
✓ asset-log.md - Tracks everything you generate
✓ references/ - Drop inspiration images here
✓ outputs/ - Your generated images land here

### Try it now

Generate your first test image:
`/image-prompt a hero image for coastal retreat website --style=project-main`

Or add some reference images first:
Drop images into `references/inspiration/` then run `/capture-trends`
```

**Quick mode:** `/project-setup summer-campaign --quick=cozy` creates everything with warm, inviting defaults - customize the style-guide.md after.

## Common Use Cases

Quick-start templates for specific creator needs:

### YouTube Thumbnail Project

```bash
/project-setup my-channel --type=campaign --quick=bold
```

Pre-configured for:
- 16:9 aspect ratio defaults
- High-contrast, attention-grabbing style
- Face + text composition patterns

### Social Media Brand Kit

```bash
/project-setup brand-name --type=brand
```

Interview asks about:
- Platform focus (IG, TikTok, LinkedIn)
- Post types (feed, stories, reels)
- Adds platform-specific dimension presets

### Character/Mascot Design

```bash
/project-setup mascot-name --type=character
```

Includes:
- Expression sheet template
- Pose library checklist
- Consistency prompts for maintaining character across images

### Product Photography

```bash
/project-setup product-line --type=product
```

Adds:
- Lighting setup presets
- Background options
- Angle guide (hero, detail, lifestyle)

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
