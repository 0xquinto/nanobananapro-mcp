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

## Moodboard Best Practices

Professional practices compiled from UX and design research:

| Practice | Why It Matters | How to Apply |
|----------|----------------|--------------|
| **Define mood statements first** | Anchors all visual decisions | Write "User should feel [emotion] when [action]" before collecting images |
| **Limit to 4 style keywords** | Too many = unfocused direction | Brainstorm many, then ruthlessly cut to 4 that complement each other |
| **Apply consistent color palette** | Creates brand recognition | Pick 3 colors max (60/30/10 rule) and use across all boards |
| **Match lighting across elements** | Incoherent lighting = amateur feel | All reference images should have similar light quality/direction |
| **Document what worked** | Builds reusable knowledge | Save successful boards with notes on why they work |
| **Align with target audience** | Design serves users, not ego | Reference your personas when selecting visual elements |
| **Use current sources** | Dated references = dated design | Search design sites by "most recent", not "most popular" |
| **Balance visual weight** | Prevents chaotic layouts | Distribute light/dark, dense/sparse across the composition |
| **Include texture variety** | Adds depth and interest | Mix 2-3 complementary textures (smooth/rough, matte/glossy) |
| **Save before presenting** | Moodboards evolve | Keep versions as your understanding develops |

### The Voice and Tone Test

Your moodboard should pass this consistency check:

| Element | Should Align With |
|---------|-------------------|
| Colors | Emotional response you want |
| Textures | Brand personality (playful, serious, organic, tech) |
| Typography feel | Voice (loud, quiet, formal, casual) |
| Imagery style | Target audience expectations |
| White space | Energy level (dense = energetic, sparse = calm) |

---

## Extracting Style from Moodboards

When you create a moodboard you love, extract its essence for reuse. Use this template:

### Style Extraction Template

```markdown
## Moodboard Analysis: [filename]

### Summary
One-sentence description of the overall feel.

### Colors
- **Primary**: [color name] ([hex code]) - [where/how used]
- **Secondary**: [color name] ([hex code]) - [where/how used]
- **Accent**: [color name] ([hex code]) - [where/how used]
- **Neutrals**: [color names] - [background, text, etc.]

### Color Relationships
- Temperature: [warm/cool/mixed]
- Saturation: [vivid/muted/mixed]
- Contrast level: [high/medium/low]

### Textures & Materials
- [texture 1]: [material name, e.g., "raw linen weave"]
- [texture 2]: [material name]
- [texture 3]: [material name]
- Surface finish: [matte/glossy/mixed]

### Lighting
- Quality: [soft/hard/mixed]
- Direction: [e.g., "upper left", "diffused overhead"]
- Color temperature: [warm/neutral/cool]
- Shadow depth: [deep/soft/minimal]

### Composition
- Layout: [grid/organic/asymmetric]
- Density: [minimal/balanced/dense]
- Visual weight: [top-heavy/bottom-heavy/centered/balanced]

### Mood & Emotion
- Primary feeling: [one word]
- Secondary feelings: [2-3 words]
- Energy: [calm/neutral/energetic]
- Formality: [casual/neutral/formal]

### Style Keywords (for prompts)
"[5-10 keywords that capture this style, comma-separated]"

### What Makes This Work
[2-3 sentences on why this combination succeeds]

### Potential Applications
- [ ] Hero images
- [ ] Product photography
- [ ] Social media
- [ ] Packaging
- [ ] Environmental design
```

### Example Extraction

```markdown
## Moodboard Analysis: sustainable-fashion-brand.png

### Summary
Modern earth tones with natural textures, feeling grounded but contemporary.

### Colors
- **Primary**: Dusty terracotta (#C4A484) - large color blocks, backgrounds
- **Secondary**: Olive (#808000) - accent elements, text
- **Accent**: Sand (#C2B280) - highlights, borders
- **Neutrals**: Warm cream (#FFFDD0), soft charcoal - backgrounds, text

### Color Relationships
- Temperature: Warm
- Saturation: Muted (desaturated by ~30%)
- Contrast level: Medium-low (harmonious)

### Textures & Materials
- Linen weave: visible thread pattern, natural imperfections
- Raw cotton: soft, unbleached, slightly nubby
- Light wood grain: blonde oak, visible but subtle grain
- Surface finish: Predominantly matte

### Lighting
- Quality: Soft, diffused
- Direction: Upper left, mimicking morning window light
- Color temperature: Warm (slight golden cast)
- Shadow depth: Soft, gradient shadows

### Composition
- Layout: Asymmetric but balanced
- Density: Minimal with breathing room
- Visual weight: Slightly bottom-heavy (grounded)

### Mood & Emotion
- Primary feeling: Grounded
- Secondary feelings: Calm, authentic, approachable
- Energy: Calm
- Formality: Casual-neutral

### Style Keywords (for prompts)
"dusty terracotta palette, natural linen textures, soft morning light,
organic minimalist, muted earth tones, raw cotton, blonde wood accents,
warm matte finish, contemporary natural aesthetic"

### What Makes This Work
The muted saturation prevents the warm tones from feeling aggressive.
Natural textures add depth without visual noise. The soft lighting
unifies all elements and creates an inviting, approachable feel.

### Potential Applications
- [x] Hero images
- [x] Product photography
- [x] Social media
- [ ] Packaging (needs more contrast for shelf impact)
- [ ] Environmental design
```

---

## Using Moodboards as References

Once you have a moodboard, use it to guide actual image generation with `compose_images`.

### Save Location

Store moodboards where skills can find them:

```
project/
├── references/
│   └── moodboards/
│       ├── brand-moodboard.png       # Primary brand direction
│       ├── summer-campaign.png       # Seasonal variant
│       └── product-style.png         # Product photography guide
```

### Reference Prompt Patterns

**Basic pattern:**
```
Using the attached moodboard as style reference, generate [subject].
Maintain the same color palette, lighting quality, and [specific element]
from the moodboard.
```

**Detailed pattern:**
```
Using the attached moodboard as style reference, generate [subject].

Match these elements from the moodboard:
- Color palette: [describe the colors you want carried over]
- Lighting: [describe the lighting quality]
- Texture feel: [describe the texture approach]
- Mood: [describe the emotional tone]

Scene-specific details:
- [Additional context for this specific image]
```

### compose_images Examples

**Product shot guided by moodboard:**
```python
compose_images(
    prompt="""
    Using the attached moodboard as style reference, generate a product shot
    of a ceramic coffee mug. Maintain the same:
    - Warm terracotta and cream color palette
    - Soft, diffused morning lighting
    - Natural linen and wood textures in background
    - Calm, grounded mood

    The mug should be cream-colored with a matte finish.
    Composition: centered, eye-level, with soft shadows.
    """,
    image_paths=["./references/moodboards/brand-moodboard.png"],
    aspect_ratio="4:5",
    resolution="2K"
)
```

**Hero image guided by moodboard:**
```python
compose_images(
    prompt="""
    Using the attached moodboard as style reference, generate a lifestyle
    hero image for a sustainable fashion brand.

    Match the moodboard's:
    - Muted earth tone palette
    - Natural fiber textures
    - Soft natural lighting
    - Contemporary-organic aesthetic

    Scene: Model in linen clothing, standing in a sunlit studio space.
    Composition: Wide shot, model off-center, negative space for text overlay.
    """,
    image_paths=["./references/moodboards/sustainable-fashion.png"],
    aspect_ratio="16:9",
    resolution="2K"
)
```

**Multi-reference composition:**
```python
compose_images(
    prompt="""
    Combine elements from the attached references:
    - Reference 1 (moodboard): Overall color palette and mood
    - Reference 2 (product): The actual product to feature

    Generate a product photography scene that places the product
    in an environment matching the moodboard's aesthetic.
    """,
    image_paths=[
        "./references/moodboards/brand-moodboard.png",
        "./references/products/coffee-mug.png"
    ],
    aspect_ratio="1:1",
    resolution="2K"
)
```

### What to Specify vs. What to Inherit

| Specify in Prompt | Inherit from Moodboard |
|-------------------|------------------------|
| Subject (what to generate) | Color palette |
| Composition (framing, angle) | Lighting quality |
| Specific props or elements | Texture vocabulary |
| Text overlay requirements | Mood and atmosphere |
| Aspect ratio | Material finishes |

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