---
name: enhance-prompt
description: Transform naive image prompts into effective ones. Accepts text concepts,
  reference images, style presets, or combinations. Guides users interactively through
  input gathering, intent clarification, and prompt enhancement using the 6-element
  formula.
argument-hint: "your concept" [--quick] [--style=preset] [--generate] [--dry-run]
---

# Enhance Prompt

Transform vague image concepts into effective prompts using the 6-element formula.

## Project Context

**Style Library Resolution** (in order):
1. `--project=<path>` flag → `<path>/style-library.md`
2. Current/parent directory with project markers → that project's `style-library.md`
3. Repository root `style-library.md`

**Project markers**: `style-guide.md`, `style-library.md`, `outputs/`, `references/`

**Project presets override root presets** of the same name.

If `style-guide.md` exists, apply its brand constraints, color restrictions, and "don't" rules.

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

### Step 1 - Gather Input (if no argument)

Ask: "What are you starting with?" → text concept / image / multiple images / style preset

Collect based on answer:
- **Text** → "What's your concept?"
- **Image** → "Drop the image path"
- **Multiple** → "Share the image paths"
- **Style** → "Which preset?" (show available)

### Step 2 - Intent Clarification (if image provided)

Ask: "What do you want from this image?"
- **Recreate** → extract all 6 elements
- **Extract style** → pull visual treatment only
- **Inspiration** → blend with your concept

**Auto-detect intent from phrasing:**
- "like this", "similar to", "recreate" → Recreation
- "in this style", "this aesthetic", "this vibe" → Style extraction
- "inspired by", "combined with" → Inspiration

### Step 3 - Refinement Questions

| Input Type | Questions |
|------------|-----------|
| Text | Mood? Style preference? What to emphasize? |
| Single Image | What to change/add? Constraints? |
| Multiple Images | How to combine? Which sets mood vs subject? |
| Style-First | Subject? Action? Setting? |
| Hybrid | Image influence (style/composition/both)? Mood? What to preserve? |

### Step 4 - Resolution (if --generate)

Ask: "What resolution?" → 1K (draft) / **2K (default)** / 4K (final)

Skip if: `--quick` flag (use 1K) or `start_image_chat` recommended (use 1K)

### Step 5 - Output

Enhanced prompt as flowing prose, 2-4 sentences. Include tool recommendation.

## Image Analysis

Extract using the 6-element framework: Subject, Composition, Action, Location, Style, Constraints (aspect ratio from dimensions).

**Elements used by intent:**
- **Recreation** → all 6 elements
- **Style extraction** → Style + Composition only
- **Inspiration** → user concept + borrowed Style/Mood

**Multiple images:** Analyze each, ask which elements to take from which.

## MCP Tool Selection

| Content Type | Tool | Why |
|--------------|------|-----|
| General creative | `generate_image` | Standard generation |
| Current events, weather, data | `search_grounded_image` | Needs real-time data |
| Editing existing image | `edit_image` | Modification workflow |
| Combining multiple refs | `compose_images` | Multi-source composition |
| Iterative refinement | `start_image_chat` | Back-and-forth session |

**Use `search_grounded_image` when prompt contains:** "current", "today's", "latest", "2026", "recent", "weather in", "forecast", "stock price", "chart", "statistics", news topics, elections, brand + "latest product"

## Arguments and Flags

| Invocation | Behavior |
|------------|----------|
| `/enhance-prompt` | Full interactive flow |
| `/enhance-prompt a coffee shop` | Skip to refinement questions |
| `/enhance-prompt ./photo.jpg` | Skip to intent clarification |
| `/enhance-prompt --quick a dog` | Direct output, no questions |

| Flag | Effect |
|------|--------|
| `--generate` | Call recommended MCP tool after enhancing |
| `--explain` | Show enhancement notes table |
| `--style=<preset>` | Apply preset from style-library.md |
| `--quick` | Skip questions, enhance directly |
| `--project=<path>` | Use specific project's style files |
| `--dry-run` | Show result without generating |

## Anti-Patterns

Avoid these in enhanced prompts:
- Quality spam: "4k, masterpiece, trending on artstation"
- Filler words: "highly detailed, ultra realistic, best quality"
- Keyword lists: use natural sentences instead
- Generic adjectives: "cobalt blue" not "colorful"

## Constraint Language

Image models respond better to positive descriptions than negations ("empty street at dawn" beats "no cars").

| Goal | Weak | Strong |
|------|------|--------|
| No people | "no people" | "deserted scene, empty space, solitary [subject]" |
| No text | "no text" | "clean design without lettering or signage" |
| Plain background | "simple background" | "solid [color] backdrop, seamless studio background" |

**When user says "no X":** Replace with positive description of what they want instead.

Example: "a park with no people" → "A tranquil, deserted park in early morning. Empty benches line the winding paths, with only fallen leaves scattered across the grass."

## Flag Behaviors

### --explain
Append enhancement notes table showing what was added to each element:

| Element | Original | Added |
|---------|----------|-------|
| Subject | "coffee shop" | Independent, exposed brick, vintage chairs |
| Composition | (missing) | Medium shot, eye level |
| ... | ... | ... |

### --generate
1. Show enhanced prompt
2. Call recommended MCP tool with: `prompt`, `model: "pro"`, `aspect_ratio` (infer or "1:1"), `resolution: "2K"`

### --style
1. Load preset from style-library.md
2. Append style definition to enhanced prompt
3. Allow combining: `--style=neo-deco --palette=vamp-darks`
4. If not found, list available presets

## Skill Handoffs

| Situation | Suggest |
|-----------|---------|
| User wants to save extracted style | `/capture-trends --preview` |
| User provides raw trend source | `/capture-trends` first |
| User wants formula explanation | `/prompt-anatomy` |
| No style-library exists | `/capture-trends` to create one |

## Example Flows

### Text Concept (Full Interactive)

```
User: /enhance-prompt
Bot: What are you starting with?
User: text
Bot: What's your concept?
User: a coffee shop
Bot: Mood? Style? What to emphasize?
User: cozy, photo, the morning light
Bot: "A cozy independent coffee shop with exposed brick walls and mismatched
     vintage chairs. Morning light streaming through large storefront windows,
     casting warm golden shadows across worn wooden floors. Medium shot at eye
     level. Film photography style with shallow depth of field and subtle grain."

     Recommended: `generate_image`
```

### Quick Mode

```
User: /enhance-prompt a dog in a park --quick
Bot: "A golden retriever mid-stride across a sun-dappled meadow..."
     Recommended: `generate_image`
```

### Image with Intent

```
User: /enhance-prompt ./moody-portrait.jpg
Bot: What do you want from this image? (recreate / extract style / inspiration)
User: recreate it, but more dramatic
Bot: Constraints?
User: 16:9
Bot: "A contemplative portrait of a young woman gazing through a rain-streaked
     window. Dramatic side lighting casting half her face in deep shadow...
     16:9 aspect ratio."
     Recommended: `generate_image`
```

### Style Extraction

```
User: /enhance-prompt ./vintage-ad.jpg
Bot: What do you want from this image?
User: extract the style
Bot: What subject to apply it to?
User: a modern smartphone, floating product shot
Bot: "A sleek modern smartphone floating against a solid cream background.
     Mid-century advertising illustration style with halftone dots, limited
     color palette of coral and teal, hand-drawn quality linework..."
     Recommended: `generate_image`
```

### Multiple Images

```
User: /enhance-prompt ./sunset.jpg ./portrait.jpg
Bot: How to combine? Which sets mood? Which provides subject?
User: pick elements, sunset for mood, portrait for subject
Bot: "A silhouetted portrait of a woman against a vivid sunset sky. Warm
     golden and coral light creating a rim-lit effect around her profile..."
     Recommended: `compose_images`
```

### Search-Grounded (Current Events)

```
User: /enhance-prompt today's weather in Paris as a watercolor
Bot: "Today's weather in Paris depicted as a watercolor painting. The Eiffel
     Tower standing peacefully against the current sky conditions..."
     Recommended: `search_grounded_image`
```
