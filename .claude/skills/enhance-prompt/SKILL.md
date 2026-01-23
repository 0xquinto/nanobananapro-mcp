---
name: enhance-prompt
description: Transform naive image prompts into effective ones. Accepts text concepts,
  reference images, style presets, or combinations. Guides users interactively through
  input gathering, intent clarification, and prompt enhancement using the 6-element
  formula.
argument-hint: "your concept" [--quick] [--style=preset] [--generate] [--dry-run]
---

# Enhance Prompt

Transform vague image concepts into effective prompts. Accepts multiple input types and guides you interactively.

## Project Context Detection

This skill is project-aware when looking up style presets:

### Detection Priority

1. **`--project=<path>` flag** → Use `<path>/style-library.md`
2. **Current directory has project markers** → Use current project's `style-library.md`
3. **Parent directory has project markers** → Use that project's `style-library.md`
4. **No project context** → Use repository root `style-library.md`

### Project Markers

A directory is considered a "project" if it contains ANY of:
- `style-guide.md`
- `style-library.md`
- `outputs/` directory
- `references/` directory

### Style Lookup Order

When `--style=<preset>` is used:
1. First check **project** `style-library.md` (if in project context)
2. Then check **root** `style-library.md`
3. Project presets override root presets of the same name

### Project Context for Enhancement

If in a project with `style-guide.md`:
- Read brand constraints and apply them to enhancement
- Note color palette restrictions
- Apply any "don't" rules from the guide

## Input Types

| Input Type | Example | Behavior |
|------------|---------|----------|
| Text concept | "a coffee shop" | Enhance the idea |
| Reference image | `./photo.jpg` | Analyze image, ask intent |
| Multiple images | `./img1.jpg ./img2.jpg` | Composite analysis |
| Style preset only | `--style=neo-deco` | Build prompt around the style |
| Hybrid | concept + image | Blend user concept with image analysis |

## The 6-Element Formula

Every effective image prompt addresses these elements:

| Element | What it defines | Example |
|---------|-----------------|---------|
| **Subject** | Who/what is the main focus. Be specific: breed, age, material, condition | "A weathered wooden fishing boat" not "a boat" |
| **Composition** | How the frame is arranged. Shot type, camera angle, focus | "Medium shot, eye level, rule of thirds" |
| **Action** | What's happening. Movement, interaction, state | "Resting on calm waters at dawn" |
| **Location** | Where it takes place. Environment, setting, context | "In a misty harbor with old stone walls" |
| **Style** | Visual treatment. Art style, medium, era, artist reference | "Oil painting style, impressionist brushwork" |
| **Constraints** | Text, aspect ratio, specific requirements | "No text, 16:9 aspect ratio" |

## Interactive Flow

### Step 1 - Input Gathering (if no argument provided)

Ask:
> "What are you starting with?"
> - A text concept or idea
> - An image to analyze
> - Multiple images to combine
> - A style preset to build around

### Step 2 - Collect Input

Based on answer:
- **Text** → "What's your concept?"
- **Image** → "Drop the image path or paste it"
- **Multiple** → "Share the image paths"
- **Style** → "Which preset?" (show available from style-library.md)

### Step 3 - Intent Clarification (if image provided)

Ask:
> "What do you want from this image?"
> - Recreate it (extract all 6 elements)
> - Extract the style (pull visual treatment only)
> - Use as inspiration for your own concept (blend with your idea)

**Intent detection from phrasing:**

| Phrase Pattern | Detected Intent |
|----------------|-----------------|
| "like this", "similar to", "recreate" | Recreation |
| "in this style", "this aesthetic", "this vibe" | Style extraction |
| "inspired by", "combined with" | Inspiration |

### Step 4 - Refinement Questions

Context-appropriate questions based on input type:

**Text Input:**
1. What mood are you going for? (cozy / dramatic / peaceful / energetic / mysterious)
2. Any particular style preference? (photograph / illustration / painting / 3D render)
3. What's the most important element to emphasize?

**Single Image Input:**
1. What should I change or add?
2. Any constraints? (aspect ratio, no text, etc.)

**Multiple Images Input:**
1. How should I combine these? (blend / pick elements / create series)
2. Which image sets the mood? Which sets the subject?
3. What's the final output? (single image / variations)

**Style-First Input:**
1. What subject should I apply this style to?
2. What's happening in the scene?
3. Any specific setting or location?

**Hybrid Input (concept + image):**
1. Should the image influence style, composition, or both?
2. What mood are you going for?
3. What's most important to preserve from the image?

### Step 4b - Resolution Question (if --generate flag)

When `--generate` is used, ask before generating:

> "What resolution do you need?"
> - Quick draft (1K) - fastest, good for iteration
> - Standard (2K) - balanced quality/speed *(default)*
> - High quality (4K) - final output, slower

**Skip conditions:**
- `--quick` flag → default to 1K
- `start_image_chat` recommended → default to 1K (iteration workflow)

### Step 5 - Output Enhanced Prompt

Output as flowing prose, 2-4 sentences. Include tool recommendation.

## Image Analysis Pipeline

When analyzing images, extract using the same 6-element framework:

1. **Subject**: Main focus (person, object, scene)
2. **Composition**: Shot type, framing, camera angle
3. **Action**: What's happening, movement, state
4. **Location**: Setting, environment, context
5. **Style**: Medium, lighting, color palette, texture
6. **Constraints**: Aspect ratio (detected from dimensions)

**Intent-based output:**

| Intent | Elements Used |
|--------|---------------|
| Recreation | All 6 elements → full prompt |
| Style extraction | Style + Composition only |
| Inspiration | User concept + borrowed Style/Mood |

**Multiple images:** Analyze each, ask which elements to take from which.

## MCP Tool Recommendations

Recommend the appropriate generation tool based on prompt content:

| Prompt Content | Recommended Tool | Reason |
|----------------|------------------|--------|
| General creative concepts | `generate_image` | Standard generation |
| Current events, news, trends | `search_grounded_image` | Needs real-time data |
| Weather visualization | `search_grounded_image` | Live weather data |
| Data/charts (stocks, stats) | `search_grounded_image` | Accurate current info |
| Editing existing image | `edit_image` | Modification workflow |
| Combining multiple refs | `compose_images` | Multi-source composition |
| Iterative refinement | `start_image_chat` | Back-and-forth session |

**Detection keywords for `search_grounded_image`:**
- "current", "today's", "latest", "2026", "recent"
- "weather in [location]", "forecast"
- "stock price", "chart", "statistics"
- Brand names + "latest product"
- News topics, elections, events

## Shortcut Arguments

Arguments skip directly to relevant steps:

| Invocation | Skips To |
|------------|----------|
| `/enhance-prompt` | Step 1 (full interactive) |
| `/enhance-prompt a coffee shop` | Step 4 (refinement questions) |
| `/enhance-prompt ./photo.jpg` | Step 3 (intent clarification) |
| `/enhance-prompt --quick a dog` | Step 5 (direct output) |

## Flags

| Flag | Behavior |
|------|----------|
| `--generate` | After enhancing, call recommended MCP tool |
| `--explain` | After the enhanced prompt, show enhancement notes |
| `--style=<preset>` | Apply preset from style-library.md (checks project first, then root) |
| `--quick` | Skip all questions, enhance directly |
| `--project=<path>` | Use specific project's style-library.md and style-guide.md |
| `--dry-run` | Show enhancement result without generating (implies no `--generate`) |

## Anti-Patterns to Avoid

- "4k, masterpiece, trending on artstation" - meaningless quality spam
- "highly detailed, ultra realistic, best quality" - filler words
- Comma-separated keyword lists - use natural sentences instead
- Generic adjectives - be specific ("cobalt blue" not "colorful")

## Constraint Language

When users want to exclude elements:

### Effective Patterns

| Goal | Weak | Strong |
|------|------|--------|
| No people | "no people" | "deserted scene, empty space, solitary [subject]" |
| No text | "no text" | "clean design without lettering or signage" |
| Plain background | "simple background" | "solid [color] backdrop, seamless studio background" |
| No specific element | "no X" | "scene focused on [Y] without X, emphasizing [Z]" |

### Why This Matters

Image models respond better to positive descriptions than negations:
- "no cars" → model may still include cars
- "empty street at dawn, only streetlights visible" → clearer instruction

### Enhancement Strategy

When user input includes "no X" or "without X":
1. Identify what they want instead
2. Replace negation with positive description
3. Keep the original intent

**Example:**
- Input: "a park with no people"
- Enhanced: "A tranquil, deserted park in early morning. Empty benches line the winding paths, with only fallen leaves scattered across the grass. Peaceful solitude, soft dawn light."

## With --explain Flag

When `--explain` is used, append this after the enhanced prompt:

```
## Enhancement Notes

| Element | Original | Added |
|---------|----------|-------|
| Subject | "coffee shop" | Independent, exposed brick, vintage chairs |
| Composition | (missing) | Medium shot, eye level |
| Action | (missing) | Morning light streaming, casting shadows |
| Location | (missing) | Large storefront windows, worn wooden floors |
| Style | (missing) | Film photography, shallow DOF, subtle grain |
| Constraints | (missing) | None specified |
```

## With --generate Flag

After producing the enhanced prompt:

1. Show the enhanced prompt to the user
2. Call the recommended MCP tool with appropriate parameters
3. Default to `generate_image` with:
   - `prompt`: the enhanced prompt
   - `model`: "pro"
   - `aspect_ratio`: infer from content or use "1:1" default
   - `resolution`: "2K" default

## With --style Flag

1. Check if `style-library.md` exists in project root
2. If preset exists, append its style definition to the enhanced prompt
3. Allow combining: `--style=neo-deco --palette=vamp-darks --mood=bold-confidence`
4. If preset not found, mention available presets or that no style library exists

## Integration with Other Skills

### Style Library
- Show categories from `style-library.md` when selecting presets
- If no style-library exists, suggest `/capture-trends`

### Skill Handoffs
- User wants to save extracted style → suggest `/capture-trends --preview`
- User provides raw trend source → suggest `/capture-trends` first
- User wants formula explanation → link to `/prompt-anatomy`

## Example Flows

### Full Interactive (No Arguments)

```
User: /enhance-prompt
Bot: What are you starting with?
     - A text concept or idea
     - An image to analyze
     - Multiple images to combine
     - A style preset to build around
User: text
Bot: What's your concept?
User: a coffee shop
Bot: What mood? (cozy / dramatic / peaceful / energetic / mysterious)
User: cozy
Bot: Style preference? (photograph / illustration / painting / 3D render)
User: photo
Bot: What to emphasize?
User: the morning light
Bot: [Enhanced prompt]

     "A cozy independent coffee shop with exposed brick walls and mismatched
     vintage chairs. Morning light streaming through large storefront windows,
     casting warm golden shadows across worn wooden floors. Medium shot at eye
     level. Film photography style with shallow depth of field and subtle grain."

     Recommended: `generate_image` for standard creative generation.
```

### Text Concept (Direct Argument)

```
User: /enhance-prompt a dog in a park
Bot: What mood? (cozy / dramatic / peaceful / energetic / mysterious)
User: energetic
Bot: Style preference? (photograph / illustration / painting / 3D render)
User: photograph
Bot: What to emphasize?
User: the dog's movement
Bot: [Enhanced prompt]

     "A golden retriever mid-stride across a sun-dappled meadow in an urban
     park. Late afternoon light filtering through mature oak trees, creating
     pools of warmth on the grass. Wide shot capturing both the joyful movement
     and the peaceful park setting. Natural photography style with vibrant
     colors and crisp focus on the dog."
```

### Quick Mode

```
User: /enhance-prompt a dog in a park --quick
Bot: "A golden retriever mid-stride across a sun-dappled meadow in an urban
     park. Late afternoon light filtering through mature oak trees, creating
     pools of warmth on the grass. Wide shot capturing both the joyful movement
     and the peaceful park setting. Natural photography style with vibrant
     colors and crisp focus on the dog."

     Recommended: `generate_image`
```

### Image Recreation

```
User: /enhance-prompt ./moody-portrait.jpg
Bot: [Analyzes image]
     What do you want from this image?
     - Recreate it
     - Extract the style
     - Use as inspiration
User: recreate it
Bot: What should I change or add?
User: make it more dramatic
Bot: Any constraints?
User: 16:9
Bot: [Enhanced prompt based on full 6-element analysis]

     "A contemplative portrait of a young woman gazing through a rain-streaked
     window. Dramatic side lighting casting half her face in deep shadow, with
     subtle reflections in her eyes. Close-up composition, slightly elevated
     angle. Moody photography with desaturated tones, high contrast, and film
     grain. 16:9 aspect ratio, no text."

     Recommended: `generate_image`
```

### Style Extraction

```
User: /enhance-prompt ./vintage-ad.jpg
Bot: What do you want from this image?
User: extract the style
Bot: [Analyzes style elements only]
     What subject should I apply this style to?
User: a modern smartphone
Bot: What's happening in the scene?
User: product shot, floating
Bot: [Enhanced prompt with extracted style applied]

     "A sleek modern smartphone floating against a solid cream background.
     Dramatic product lighting with soft shadows. Centered composition with
     generous negative space. Mid-century advertising illustration style with
     halftone dots, limited color palette of coral and teal, hand-drawn quality
     linework, vintage paper texture."

     Recommended: `generate_image`
```

### Current Events (Search Grounded)

```
User: /enhance-prompt today's weather in Paris as a watercolor
Bot: I'll use search-grounded generation for accurate weather data.
     What mood? (cozy / dramatic / peaceful / energetic / mysterious)
User: peaceful
Bot: What to emphasize?
User: the Eiffel Tower
Bot: [Enhanced prompt]

     "Today's weather in Paris depicted as a watercolor painting. The Eiffel
     Tower standing peacefully against the current sky conditions. Loose,
     flowing brushstrokes with soft edges and bleeding colors. Impressionist
     watercolor style with visible paper texture and subtle color gradients."

     Recommended: `search_grounded_image` for accurate real-time weather data.
```

### Multiple Images

```
User: /enhance-prompt ./sunset.jpg ./portrait.jpg
Bot: [Analyzes both images]
     How should I combine these?
     - Blend into one scene
     - Pick elements from each
     - Create a series
User: pick elements
Bot: Which image sets the mood?
User: sunset
Bot: Which provides the subject?
User: portrait
Bot: [Enhanced prompt combining elements]

     "A silhouetted portrait of a woman against a vivid sunset sky. Warm
     golden and coral light from behind creating a rim-lit effect around her
     profile. Medium shot, low angle looking up. Dramatic photography with
     high contrast between the dark figure and brilliant sky colors."

     Recommended: `compose_images` for multi-reference composition.
```

### With Style Preset

```
User: /enhance-prompt a portrait --style=cinematic
Bot: [Loads cinematic preset from style-library.md]
     What mood? (cozy / dramatic / peaceful / energetic / mysterious)
User: dramatic
Bot: What to emphasize?
User: the lighting
Bot: [Enhanced prompt with style incorporated]

     "A contemplative portrait of a middle-aged woman gazing through a
     rain-streaked window. Dramatic side lighting casting half her face in
     shadow, subtle reflections in her eyes. Close-up composition with shallow
     depth of field. Cinematic lighting, anamorphic lens flare, film grain,
     dramatic shadows, teal and orange color grade."

     Recommended: `generate_image`
```

## MCP Tools Available

- `generate_image(prompt, model, aspect_ratio, resolution)` - Standard generation
- `edit_image(prompt, image_path, model, aspect_ratio, resolution)` - Edit existing image
- `compose_images(prompt, image_paths, model, aspect_ratio, resolution)` - Combine multiple images
- `search_grounded_image(prompt, aspect_ratio, resolution)` - Generation with live web data
- `start_image_chat(initial_prompt, model)` - Start iterative session for refinement
