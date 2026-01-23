---
name: project-setup
description: Scaffold an image generation project with style guide, references,
  and output directories. Use when starting a new visual project, brand work,
  or any multi-image effort requiring consistency. Creates project structure
  and style-guide.md template.
argument-hint: "[project-name] [--type=brand|campaign|character|product] [--quick] | validate [path] | update [path]"
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

## Project Types

| Type | Focus | Extra content |
|------|-------|---------------|
| `brand` | Visual identity | Color system section, typography notes, logo usage guidelines |
| `campaign` | Marketing assets | Moodboard template, shot list, deliverables checklist |
| `character` | Character design | Character sheet template, pose library section, expression guide |
| `product` | Product photography | Lighting setup notes, background options, angle guide |

## Process

### Step 1: Parse Input

Check for project name and type in the command:
- `/project-setup my-brand --type=brand`
- `/project-setup` (will prompt for details)

### Quick Mode (--quick flag)

When `--quick` is passed, skip the interview and use these defaults:

| Parameter | Default Value |
|-----------|---------------|
| Project Type | `brand` |
| Visual Style | "clean and modern" |
| Color Preferences | "neutral palette with one accent color" |
| Reference Medium | Photography |

**Usage:**
```bash
/project-setup my-project --quick
/project-setup my-project --type=character --quick
```

When `--type` is also provided, only that parameter is set—others use defaults above.

### Step 2: Interactive Interview (if details missing)

Ask these questions to gather project requirements:

**Question 1: Project Name**
> "What's the project name? (This creates the folder)"

**Question 2: Project Type**
> "What type of project is this?"
> - Brand identity (logos, colors, visual system)
> - Marketing campaign (ads, social, promotional)
> - Character design (characters, expressions, poses)
> - Product photography (product shots, lifestyle images)

**Question 3: Visual Style Direction**
> "Describe the visual style you're going for in a few words"
> (Examples: "minimal and modern", "warm and nostalgic", "bold and energetic")

**Question 4: Color Preferences**
> "Any specific colors or color mood?"
> (Examples: "earth tones", "neon accents on dark", "pastel palette")

**Question 5: Reference Medium**
> "What visual medium fits best?"
> - Photography (realistic)
> - Illustration (artistic)
> - 3D Render (digital)
> - Mixed/Flexible

**Question 6: Visual Constraints**
> "Anything to specifically avoid? (competitors, styles, elements)"
> (Examples: "no corporate blue", "avoid stock photo look", "don't look like Apple")

### Step 3: Generate Structure

Create all directories and files based on answers.

### Step 4: Confirm

Show what was created and suggest next steps.

## File Templates

> **Note:** Templates are defined inline below rather than as separate files. This keeps the skill self-contained and makes customization visible.

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

## Art Styles

- **project-main**: "[Style description]. [Medium]. Consistent [lighting style] lighting. [Color mood] color palette. [Key visual characteristic]."

  Example: "Clean minimalist aesthetic. Professional photography. Consistent soft natural lighting. Neutral palette with warm accents. Emphasis on negative space and clean lines."

## Color Palettes

- **project-colors**: "[Primary color description], [secondary color], [accent color]. [Overall mood]. Avoid [colors to avoid]."

  Example: "Warm ivory backgrounds, deep forest green accents, touches of brass metallic. Organic and premium feel. Avoid pure white and saturated primaries."

## Lighting

- **project-lighting**: "[Light quality] [light direction] lighting. [Shadow characteristic]. [Time of day or studio setup reference]."

  Example: "Soft diffused side lighting. Gentle shadows with visible detail. Golden hour warmth without harsh sun."

## Moods

- **project-mood**: "[Emotional quality]. [Energy level]. [Atmosphere]. Evokes [feeling or association]."

  Example: "Calm and confident. Quiet energy. Intimate but not cramped. Evokes a peaceful morning in a well-designed space."

## Compositions

- **project-composition**: "[Framing style]. [Subject placement]. [Background treatment]. [Depth of field]."

  Example: "Generous breathing room around subjects. Rule of thirds placement. Clean uncluttered backgrounds. Shallow depth of field isolating subject."
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

After scaffolding, display:

```
## Project Created: [project-name]

### Structure
✓ style-guide.md - Ready for customization
✓ style-library.md - 3 starter presets added
✓ references/moodboards/
✓ references/characters/
✓ references/inspiration/
✓ outputs/exploration/
✓ outputs/finals/
✓ asset-log.md - Ready for tracking

### Next Steps
1. Add reference images to `references/inspiration/`
2. Review and customize `style-guide.md`
3. Use `/capture-trends` on references to populate style library
4. Start generating with `/image-prompt`

### Quick Start
Try: `/image-prompt a hero image for this project --style=project-main`
```

## Integration with Other Skills

This skill creates files that other skills detect and use:

| File Created | Used By |
|--------------|---------|
| `style-library.md` | `/enhance-prompt --style=`, `/image-prompt --style=`, `/style-library` |
| `style-guide.md` | `/image-prompt` (reads for constraints) |
| `references/` | `/image-prompt --refs=`, `/capture-trends` |
| `outputs/` | `/image-prompt` (saves here) |
| `asset-log.md` | `/image-prompt` (logs generations) |

## Error Handling

| Situation | Response |
|-----------|----------|
| Directory exists | "Project `[name]` already exists. Use a different name or delete the existing folder." |
| Invalid type | "Unknown type `[type]`. Valid types: brand, campaign, character, product" |
| No write permission | "Cannot create project here. Check folder permissions." |
| Nothing to update | "Project `[name]` is already complete. No changes needed." |

## Subcommands

### /project-setup validate

Check project structure integrity and report issues.

**Usage:**
```bash
/project-setup validate
/project-setup validate ./my-project
```

**Checks performed:**

| Check | Pass | Fail |
|-------|------|------|
| style-guide.md exists | ✓ Found | ⚠ Missing — run `/project-setup` to create |
| style-library.md exists | ✓ Found | ⚠ Missing — will use root library |
| outputs/ directory | ✓ Found | ⚠ Missing — will be created on first generation |
| references/ directory | ✓ Found | ℹ Missing — optional, create if using `--refs` |
| asset-log.md exists | ✓ Found | ⚠ Missing — create for tracking |
| style-guide.md has content | ✓ Populated | ⚠ Template only — customize for your project |
| style-library.md has presets | ✓ Has presets | ℹ Empty — use `/capture-trends` to populate |

**Output format:**

```
## Project Validation: [project-name]

✓ style-guide.md — Found, customized
✓ style-library.md — Found, 3 presets
✓ outputs/exploration/ — Found
✓ outputs/finals/ — Found
⚠ references/ — Missing (optional)
✓ asset-log.md — Found

**Status: Ready** (1 optional item missing)

Suggestions:
- Create `references/` if you plan to use reference images
```

**Validation states:**

| State | Meaning |
|-------|---------|
| ✓ Ready | All required files present and populated |
| ⚠ Needs attention | Missing required files or uncustomized templates |
| ✗ Not a project | No project markers found |

### /project-setup update

Refresh project structure while preserving customizations.

**Usage:**
```bash
/project-setup update
/project-setup update ./my-project
```

**Behavior:**

| Item | Action |
|------|--------|
| Missing directories | Create them |
| Missing files | Create with template |
| Existing style-guide.md | **Preserve** (never overwrite) |
| Existing style-library.md | **Merge** new presets, keep existing |
| Existing asset-log.md | **Preserve** (never overwrite) |

**Update checks:**

1. Detect project type from existing style-guide.md
2. Compare current structure against expected structure
3. Add missing pieces only
4. Report what was added

**Output format:**

```
## Project Updated: [project-name]

### Added
✓ references/moodboards/ — Created (was missing)
✓ outputs/finals/ — Created (was missing)

### Preserved
- style-guide.md — Kept existing (customized)
- style-library.md — Kept existing (has 5 presets)
- asset-log.md — Kept existing (has 12 entries)

### No Changes Needed
- outputs/exploration/ — Already exists
- references/inspiration/ — Already exists
```

**Merge behavior for style-library.md:**

When updating, check if starter presets exist. If missing, append:

```markdown
## Added by update

- **project-main**: "[detect from style-guide or use default]"
- **project-colors**: "[detect from style-guide or use default]"
- **project-mood**: "[detect from style-guide or use default]"
```
