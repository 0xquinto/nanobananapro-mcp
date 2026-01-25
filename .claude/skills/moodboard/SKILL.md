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

# Research-driven moodboard (for trend mashups, unfamiliar aesthetics)
/moodboard research "gimme gummy + extra celestial"

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

### Research-Driven Moodboard

**Purpose:** Explore unfamiliar aesthetics, trend mashups, or styles you can't fully articulate yet.

**When to Use:**
- Combining multiple trends (e.g., "Gimme Gummy + Extra Celestial")
- Exploring an aesthetic you've heard of but haven't internalized
- When you don't know exactly what you want but have keywords

**You'll Learn:**
- How to research visual trends systematically
- Translating text descriptions into visual understanding
- Building references before generating final designs

**Workflow:**

#### Step 1: Research

Use web search to find real-world examples of the aesthetic:

```
Search for:
- "[trend name] aesthetic examples"
- "[trend name] jewelry/fashion/decor" (specific applications)
- "Pinterest Predicts [year] [trend name]" (official definitions)
- "[trend name] + [trend name] mashup" (combinations)
```

**What to extract from research:**
| Element | Look For |
|---------|----------|
| Colors | Specific hex codes, color names, palettes |
| Materials | Textures, surfaces, finishes (glossy, matte, translucent) |
| Objects | Real products that embody the aesthetic |
| Mood | Emotional keywords, ASMR triggers, feelings |
| Search terms | What people actually search for (+50%, +130% etc.) |

#### Step 2: Synthesize into Moodboard Prompt

Build a moodboard prompt that includes **specific objects** from your research, not generic descriptions:

```
Moodboard collage for "[Aesthetic Name]" combining [Trend 1] and [Trend 2].

Include specific objects from research:
- [Real product type 1 with material details]
- [Real product type 2 with finish/texture]
- [Real product type 3 with color specifics]

Material qualities: [textures found in research]
Color palette: [specific colors with hex codes if found]
Mood: [emotional keywords from trend descriptions]

Magazine-quality layout, cohesive aesthetic board, editorial arrangement.
```

**Example (Alien Candy = Gimme Gummy + Extra Celestial):**
```
Moodboard collage for "Alien Candy" aesthetic combining Gimme Gummy and Extra Celestial trends.

Include:
- Translucent resin gummy bear jewelry with holographic shimmer
- Jelly-textured phone case with opalescent finish
- Rubberized 3D nail art in candy colors
- Iridescent glass objects glowing with inner light
- Bendy silicone sculptures with cosmic bioluminescence

Material qualities: squishy, spring-back, ASMR-tactile
Color palette: watermelon pink (#FF6B9D), lime green (#7FFF00), lemon yellow (#FFD700), holographic iridescence
Mood: satisfying, tactile, weirdly edible, otherworldly

Magazine-quality layout, cohesive aesthetic board.
```

#### Step 3: Generate Moodboard

Generate the moodboard using `/image-prompt`:

```bash
/image-prompt [moodboard prompt] --aspect=4:3
```

Save to: `references/moodboards/[aesthetic-name]-moodboard.png`

#### Step 4: Use Moodboard for Final Design

Use `compose_images` with the moodboard as reference. **Be specific about which elements to pull:**

```
Using the attached moodboard as style reference, create [final design subject].

Match these specific elements from moodboard:
- [Material quality from specific object in moodboard]
- [Color treatment from specific object]
- [Texture/finish from specific object]

Do NOT create: [what to avoid]
```

**Key insight:** Reference specific objects IN the moodboard, not generic aesthetic descriptions. "Like the silicone octopus sculpture" not "squishy and alien."

#### Step 5: Iterate on Final Design

If the composed design still feels generic:
1. Identify which moodboard element is missing
2. Call out that specific element in the next compose prompt
3. Or try a different subject entirely — the aesthetic might not suit "creatures"

---

## Research-Driven Moodboard: Example Session

```
User: /moodboard research "gimme gummy + extra celestial"

Claude: Starting research-driven moodboard for Gimme Gummy + Extra Celestial mashup.

        **Step 1: Research**

        [Searches for trend definitions and real examples]

        **Gimme Gummy** (from Pinterest Predicts):
        - "ASMR overload" — bendy phone cases, jelly blush, rubberized nail art
        - Materials: resin, translucent colored shapes, spring-back textures
        - Searches: gummy bears aesthetic +50%, jelly candy aesthetic +100%

        **Extra Celestial**:
        - "Going intergalactic" — holographic home accents, opalescent eyeshadow
        - Searches: alien core aesthetic +80%, opalescent +115%

        **Step 2: Building moodboard prompt**

        [Shows synthesized prompt with specific objects]

        Generate this moodboard?

User: yes

Claude: [Generates moodboard, saves to references/moodboards/]

        Moodboard created. Key elements captured:
        - Gummy bear earrings with holographic shimmer
        - Opalescent alien phone case
        - Bendy bioluminescent sculpture
        - Translucent candy-colored furniture

        **Step 3: Ready for final design**

        What do you want to create using this aesthetic?
        - A creature/character
        - A product design
        - An abstract pattern
        - Something else

User: A creature for POD t-shirts

Claude: Using moodboard as reference...

        [Composes with specific element callouts]

        "Create a creature design matching the tactile quality of the
        bioluminescent octopus sculpture in the moodboard — that squishy,
        silicone-like texture. Holographic shimmer like the glass orbs.
        Candy colors from the gummy bear earrings..."
```

---

## Design Concepts Explained

| Concept | Definition | Exercise |
|---------|------------|----------|
| **Color Temperature** | Warm (reds, oranges, yellows) = energetic, welcoming. Cool (blues, greens, purples) = calm, professional. | Generate two moodboards for the same concept - one warm, one cool. |
| **Visual Weight** | Heavy = dark, dense, bottom-weighted (luxury feel). Light = bright, airy, top-weighted (minimal feel). | Create a "heavy" then "light" moodboard for the same brand. |
| **Texture Rhythm** | Contrast (glass vs concrete), Harmony (wood + linen), Tension (metal + plants). | Create a moodboard with intentional texture contrast. Name each texture. |
| **Color Restraint** | 60/30/10 rule: dominant, secondary, accent. Fewer colors = stronger identity. | Create a 3-color moodboard. Notice how constraint forces intentionality. |

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

| Practice | Guidance |
|----------|----------|
| **Define mood first** | Write "User should feel [emotion] when [action]" before collecting images |
| **Limit to 4 keywords** | Brainstorm many, ruthlessly cut to 4 that complement each other |
| **3-color palette** | Use 60/30/10 rule across all boards for brand recognition |
| **Match lighting** | All reference images should have similar light quality/direction |
| **Document successes** | Save boards with notes on why they work |
| **Balance visual weight** | Distribute light/dark, dense/sparse across composition |
| **Include texture variety** | Mix 2-3 complementary textures (smooth/rough, matte/glossy) |

### Voice and Tone Alignment

| Element | Should Match |
|---------|--------------|
| Colors | Emotional response you want |
| Textures | Brand personality |
| Typography feel | Voice (loud, quiet, formal, casual) |
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

Use `compose_images` to apply your moodboard's style to new generations.

### Save Location

```
project/references/moodboards/
├── brand-moodboard.png       # Primary brand direction
├── summer-campaign.png       # Seasonal variant
└── product-style.png         # Product photography guide
```

### Prompt Pattern

```
Using the attached moodboard as style reference, generate [subject].

Match from moodboard: [color palette, lighting, textures, mood]

Scene-specific: [composition, props, framing]
```

### What to Specify vs. What to Inherit

| Specify in Prompt | Inherit from Moodboard |
|-------------------|------------------------|
| Subject (what to generate) | Color palette |
| Composition (framing, angle) | Lighting quality |
| Specific props or elements | Texture vocabulary |
| Aspect ratio | Mood and atmosphere |

---

## Progress Tracking

As you use this skill, you're building:

1. **Vocabulary** - Can you name what you see?
2. **Intent** - Can you articulate what you want before generating?
3. **Critique** - Can you identify what works and why?
4. **Iteration** - Can you make targeted improvements?
5. **Consistency** - Can you apply a style across multiple images?

---

## Image Generation

**IMPORTANT:** Never call MCP tools directly. Always chain through `/image-prompt` skill.

| Task | Invoke | Notes |
|------|--------|-------|
| Create moodboard | `/image-prompt [concept] --aspect=4:3` | Moodboard layouts |
| Refine elements | `/image-prompt` iteration flow | Use "adjust" options |
| Iterate design | `/image-prompt [concept] --chat` | Multi-turn refinement |
| Apply style | `/image-prompt [subject] --refs=[moodboard]` | Pass moodboard as reference |

The `/image-prompt` skill handles enhancement, taste checks, and proper tool selection internally.

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