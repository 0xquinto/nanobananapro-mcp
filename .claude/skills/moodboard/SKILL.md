---
name: moodboard
description: Learn design thinking through guided moodboard creation. For vibecoders who want to develop visual design skills.
---

# Moodboard Skill

A guided skill for learning design fundamentals through moodboard creation. Designed for developers and vibecoders who want to build visual design intuition.

## What This Skill Teaches

Moodboards aren't just pretty collages - they're **design thinking made visible**. This skill helps you:

1. **Articulate visual preferences** - Move from "I like this" to "I like warm tones with organic textures"
2. **Build design vocabulary** - Learn to name what you see
3. **Make intentional choices** - Understand why certain combinations work
4. **Create consistency** - Apply learned principles across a project

## Commands

```bash
# Guided moodboard creation (recommended for learning)
/moodboard

# Create for a specific project
/moodboard "coffee shop brand"

# Quick mode (skip explanations)
/moodboard "summer campaign" --quick

# Analyze an existing image to learn from it
/moodboard analyze ./reference.png

# Learn about a specific design concept
/moodboard learn colors
/moodboard learn textures
/moodboard learn composition
```

## Workflow

### Phase 1: Define Your Intent

Before any generation, you'll answer questions that build design thinking:

**Intent Questions:**
1. "What feeling should someone get when they see this?"
2. "Is this energetic or calm? Luxurious or accessible? Modern or timeless?"
3. "Think of a place, time of day, or season that captures this vibe"

These questions aren't just for the AI - they're training you to think about design intentionally.

### Phase 2: Build Your Palette

You'll make choices about:

**Colors:**
| Question | Design Concept You're Learning |
|----------|-------------------------------|
| Warm or cool? | Color temperature |
| Saturated or muted? | Color intensity |
| High contrast or harmonious? | Color relationships |
| 2-3 colors or more? | Color restraint |

**Textures:**
| Question | Design Concept You're Learning |
|----------|-------------------------------|
| Smooth or rough? | Tactile quality |
| Natural or synthetic? | Material origin |
| Matte or glossy? | Surface finish |
| Consistent or varied? | Texture rhythm |

**Mood:**
| Question | Design Concept You're Learning |
|----------|-------------------------------|
| Light or dark? | Value/luminosity |
| Minimal or dense? | Visual weight |
| Ordered or organic? | Compositional structure |
| Static or dynamic? | Energy and movement |

### Phase 3: Generate and Reflect

After generating, you'll be asked to reflect:

1. "What works about this? What specific element?"
2. "What doesn't match your vision? Why?"
3. "If you could change one thing, what would it be?"

This reflection builds your ability to critique and iterate.

### Phase 4: Extract and Save

Convert your successful moodboard into reusable knowledge:

1. **Name the style** - Give it a memorable name
2. **Document the palette** - Specific colors, not just "warm"
3. **Note the textures** - What materials appear?
4. **Capture the mood** - Keywords that describe the feeling
5. **Save as preset** - Add to style-library for reuse

---

## The Four Moodboard Types

### Brand Moodboard

**Purpose:** Establish overall visual identity

**You'll Learn:**
- How colors convey personality
- Typography "feeling" (even without rendering text)
- Consistency across touchpoints

**Example Prompt Pattern:**
```
A brand moodboard for [business type] that feels [personality traits].
Color palette: [specific colors].
Materials: [textures/surfaces].
Mood: [emotional qualities].
Magazine-quality layout, cohesive aesthetic.
```

### Project Moodboard

**Purpose:** Guide a specific campaign or collection

**You'll Learn:**
- Seasonal and thematic color shifts
- How context shapes aesthetic choices
- Balancing brand consistency with project freshness

**Example Prompt Pattern:**
```
A project moodboard for [campaign/season] with [theme].
Building on [brand palette] but adding [seasonal element].
Key objects: [relevant items].
Setting: [environment that supports theme].
Editorial layout, cohesive vision.
```

### Product Moodboard

**Purpose:** Direct product photography style

**You'll Learn:**
- How background affects product perception
- Lighting as a storytelling tool
- Props and staging principles

**Example Prompt Pattern:**
```
A product photography moodboard for [product category].
Background style: [surface/setting].
Lighting: [quality and direction].
Props: [supporting elements].
Color palette: [specific colors].
Clean layout, commercial quality.
```

### Character Moodboard

**Purpose:** Guide character design

**You'll Learn:**
- Visual personality expression
- Color as character trait
- Costume and accessory storytelling

**Example Prompt Pattern:**
```
A character design moodboard for [character description].
Art style: [specific style reference].
Color palette: [character's colors].
Costume elements: [clothing/accessories].
Environment hints: [where they exist].
Reference sheet layout.
```

---

## Design Concepts Explained

### Color Temperature

**Warm colors** (reds, oranges, yellows): Energetic, welcoming, appetizing
**Cool colors** (blues, greens, purples): Calm, professional, refreshing

**Exercise:** Generate two moodboards for the same concept - one warm, one cool. Notice how the feeling changes completely.

### Visual Weight

**Heavy:** Dark colors, dense textures, large elements, bottom-weighted
**Light:** Bright colors, airy spacing, small elements, top-weighted

**Exercise:** Create a "heavy" moodboard (luxury, grounded) then a "light" one (minimal, ethereal) for the same brand.

### Texture Rhythm

Mixing textures creates visual interest:
- **Contrast:** Smooth glass against rough concrete
- **Harmony:** Natural wood with linen fabric
- **Tension:** Industrial metal with organic plants

**Exercise:** Create a moodboard with intentional texture contrast. Name each texture you included.

### Color Restraint

Fewer colors = stronger identity. Professional design often uses:
- 1 dominant color (60%)
- 1 secondary color (30%)
- 1 accent color (10%)

**Exercise:** Create a moodboard with only 3 colors. Notice how the constraint forces intentionality.

---

## Analyzing Existing Images

Use `/moodboard analyze` to learn from references:

```bash
/moodboard analyze ./inspiration.png
```

The skill will extract and name:
- **Colors** with approximate hex codes
- **Textures** with material names
- **Lighting** quality and direction
- **Mood** keywords
- **Composition** structure

This builds your vocabulary by connecting what you see to design language.

---

## Integration with Other Skills

### After Creating a Moodboard

```bash
# Extract the style you created
/capture-trends ./references/moodboards/my-moodboard.png --name=project-style

# Save as reusable preset
/style-library add project-style "warm terracotta palette, linen textures, soft morning light"

# Use for actual image generation
/image-prompt "product shot of coffee mug" --style=project-style
```

### Project Workflow

```
/project-setup my-brand --type=brand
    ↓
/moodboard "artisan coffee roaster"     ← You are here
    ↓
/capture-trends ./references/moodboards/brand-moodboard.png
    ↓
/style-library add brand-main "..."
    ↓
/image-prompt "hero image" --style=brand-main
```

---

## Common Mistakes (and What They Teach)

| Mistake | What It Teaches |
|---------|-----------------|
| "Make it look good" | Design requires specific intent |
| "Colorful palette" | Vague = generic results |
| Too many competing elements | Restraint is a skill |
| No clear mood | Emotion drives connection |
| Single-use moodboard | Good design is systematic |

---

## Progress Tracking

As you use this skill, you're building:

1. **Vocabulary** - Can you name what you see?
2. **Intent** - Can you articulate what you want before generating?
3. **Critique** - Can you identify what works and why?
4. **Iteration** - Can you make targeted improvements?
5. **Consistency** - Can you apply a style across multiple images?

---

## MCP Tools Used

| Tool | When Used |
|------|-----------|
| `generate_image` | Create moodboard images |
| `edit_image` | Refine specific elements |
| `compose_images` | Use moodboard as reference for other generations |
| `start_image_chat` | Iterate on moodboard design |

### Tool Selection

```
Creating a moodboard from scratch?
  → generate_image

Refining an existing moodboard?
  → edit_image OR start_image_chat

Using moodboard to guide new generation?
  → compose_images with moodboard as reference
```

### MCP Tool Signatures

```python
generate_image(
    prompt,
    model="pro",
    aspect_ratio="4:3",  # Good for moodboard layouts
    resolution="2K",
    output_path="./references/moodboards/[name].png"
)

compose_images(
    prompt="Using the attached moodboard as style reference...",
    image_paths=["./references/moodboards/project-moodboard.png"],
    model="pro",
    aspect_ratio="1:1",
    resolution="2K"
)
```

---

## Example Session

```
User: /moodboard "sustainable fashion brand"

Claude: Let's create a moodboard for your sustainable fashion brand.
        First, some questions to build your design intent:

        1. What feeling should someone get when they see this brand?
           (e.g., trustworthy, innovative, earthy, luxurious)

User: Earthy but modern, not crunchy granola

Claude: Good distinction. You want natural without looking dated.

        2. Color temperature - warm (terracotta, sage) or cool (ocean, slate)?

User: Warm I think, but not too orange

Claude: Warm earth tones, avoiding orange. Think terracotta, olive, sand.

        3. Textures - what materials represent your brand?
           (linen, raw cotton, recycled materials, natural dyes)

User: Linen, undyed cotton, maybe some natural wood

Claude: Natural fibers with wood accents. Matte finishes, organic textures.

        Building your moodboard prompt with what you've described:
        - Mood: Modern earth, approachable sustainability
        - Colors: Warm neutrals (terracotta, olive, sand, cream)
        - Textures: Linen, raw cotton, natural wood grain
        - Feeling: Grounded but contemporary

        [Generates moodboard]

Claude: Here's your moodboard. Let's reflect:

        1. What element works best for you?
        2. Anything that doesn't feel right?

User: I love the linen texture but the terracotta is too red

Claude: Let's shift that terracotta toward a dustier, more muted tone.
        [Uses edit_image to adjust]

        Better? This is teaching you about color saturation -
        the original was too saturated for the "modern earth" feel
        you described.

User: Yes, that's it

Claude: Great. Let's save this:

        Extracted style: "modern-earth"
        - Colors: dusty terracotta (#C4A484), olive (#808000),
          sand (#C2B280), cream (#FFFDD0)
        - Textures: linen weave, raw cotton, light wood grain
        - Mood: grounded, contemporary, natural without crunchy

        Saved to references/moodboards/sustainable-fashion-moodboard.png
        Added preset "modern-earth" to style-library.md

        You can now use: /image-prompt "product shot" --style=modern-earth
```

---

## Learning Milestones

Track your progress as a designer:

| Milestone | You Can... |
|-----------|-----------|
| **Beginner** | Answer intent questions, recognize what you like |
| **Intermediate** | Name colors/textures specifically, critique your own work |
| **Confident** | Create consistent styles, iterate purposefully |
| **Fluent** | Predict what will work, teach others your approach |

This skill is designed to move you from "I know it when I see it" to "I can create it on purpose."