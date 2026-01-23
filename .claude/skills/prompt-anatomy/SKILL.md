---
name: prompt-anatomy
description: Analyze image prompts against the 6-element framework. Use when
  user asks "why isn't this working?", "what's wrong with my prompt?", or
  wants to understand prompt structure. Educational tool that shows gaps
  and suggests improvements.
argument-hint: '"your prompt" [--fix] [--verbose] [--format=json]'
---

# Prompt Anatomy

Analyze image prompts against the 6-element framework. Educational tool that shows what's present, missing, and how to improve.

## The 6-Element Framework

| Element | What it defines | Strong indicators |
|---------|-----------------|-------------------|
| **Subject** | Who/what is the main focus | Specific nouns, adjectives describing appearance, materials, condition |
| **Composition** | How the frame is arranged | Shot types (close-up, wide), angles (low, eye-level), framing rules |
| **Action** | What's happening | Verbs, gerunds (-ing), movement words, states of being |
| **Location** | Where it takes place | Environment words, settings, "in a...", "at the...", backgrounds |
| **Style** | Visual treatment | Art movements, mediums, lighting descriptors, artist references |
| **Constraints** | Text, aspect ratio, specifics | Quoted text, ratios, "no X", explicit requirements |

## Process

1. **Parse** the input prompt word by word
2. **Classify** each phrase into one of the 6 elements
3. **Score** each element:
   - ✓ **Present** — clearly defined with specifics
   - △ **Weak** — mentioned but vague or generic
   - ✗ **Missing** — not addressed at all
4. **Explain** what's working and why
5. **Suggest** specific improvements for weak/missing elements

## Output Format

Always output in this structure:

```
## Prompt Analysis

**Original prompt:** "[user's prompt here]"

| Element | Status | Found | Suggestion |
|---------|--------|-------|------------|
| Subject | ✓/△/✗ | "quoted text found" | Specific improvement |
| Composition | ✓/△/✗ | "quoted text" or — | Specific improvement |
| Action | ✓/△/✗ | "quoted text" or — | Specific improvement |
| Location | ✓/△/✗ | "quoted text" or — | Specific improvement |
| Style | ✓/△/✗ | "quoted text" or — | Specific improvement |
| Constraints | ✓/△/✗ | "quoted text" or — | Specific improvement |

**Score: X/6 elements defined**

### What's Working
[Explain the strong points]

### Key Improvements
[2-3 most impactful suggestions]
```

## Scoring Criteria

### Subject
- ✓ Present: Specific noun with descriptive details ("a weathered wooden fishing boat with peeling blue paint")
- △ Weak: Generic or vague ("a boat", "a person")
- ✗ Missing: No clear subject

### Composition
- ✓ Present: Shot type AND camera angle ("close-up portrait from low angle")
- △ Weak: Only one aspect mentioned ("close-up")
- ✗ Missing: No framing information

### Action
- ✓ Present: Clear action or dynamic state ("leaping through morning mist")
- △ Weak: Static or implied ("sitting", "standing")
- ✗ Missing: No indication of what's happening

### Location
- ✓ Present: Specific environment with atmosphere ("in a misty harbor with old stone walls at dawn")
- △ Weak: Generic location ("in a park", "outside")
- ✗ Missing: No environmental context

### Style
- ✓ Present: Clear visual treatment ("oil painting in the style of the Dutch masters, warm palette")
- △ Weak: Vague style words ("artistic", "beautiful")
- ✗ Missing: No style indication

### Constraints
- ✓ Present: Explicit requirements stated ("text reading 'OPEN', no people, square format")
- △ Weak: Implied constraints or ineffective language
- ✗ Missing: Usually fine if none needed

**Effective constraint language:**

| Want to Avoid | Effective | Ineffective |
|---------------|-----------|-------------|
| No text | "without any text or lettering" | "no text" (too brief) |
| No people | "empty scene, unoccupied space" | "no people" (model may ignore) |
| Simple background | "solid white background, no distractions" | "simple background" (vague) |
| No specific object | "scene without [object], [alternative focus]" | "no [object]" (negative alone) |

**Key insight:** Negative prompting works better when you specify what you *do* want instead. "Empty street at dawn" is more effective than "street with no cars".

## Options

| Flag | Behavior |
|------|----------|
| `--fix` | After analysis, output an improved version of the prompt |
| `--verbose` | Include explanations of why each element matters for AI generation |

## With --fix Flag

After the analysis table, add:

```
## Fixed Prompt

"[Complete rewritten prompt addressing all gaps]"
```

## With --verbose Flag

Add educational notes after each element:

```
| Element | Status | Found | Suggestion |
|---------|--------|-------|------------|
| Subject | △ | "a cat" | Add: breed, coloring, age, distinguishing features |

> **Why Subject matters:** The AI needs specifics to generate consistent, interesting results. "A cat" could be any of thousands of interpretations. "A sleepy marmalade tabby with white paws" dramatically narrows the output space.
```

## JSON Output (`--format=json`)

```json
{
  "prompt": "analyzed prompt",
  "elements": {
    "subject": {"status": "present|vague|missing", "content": "extracted text"},
    "composition": {"status": "...", "content": "..."},
    "action": {"status": "...", "content": "..."},
    "location": {"status": "...", "content": "..."},
    "style": {"status": "...", "content": "..."},
    "constraints": {"status": "...", "content": "..."}
  },
  "score": 4,
  "max_score": 6,
  "suggestions": ["Add composition details", "Specify style"]
}
```

## Examples

### Basic Analysis

User: `/prompt-anatomy a cat sitting`

Response:

```
## Prompt Analysis

**Original prompt:** "a cat sitting"

| Element | Status | Found | Suggestion |
|---------|--------|-------|------------|
| Subject | △ | "a cat" | Add descriptors: breed, color, age, markings |
| Composition | ✗ | — | Add: shot type (portrait, full body), angle |
| Action | ✓ | "sitting" | Good! Could enhance: "sitting on...", "sitting alertly" |
| Location | ✗ | — | Add environment: windowsill, garden, studio backdrop |
| Style | ✗ | — | Add: photograph, illustration, painting style |
| Constraints | ✗ | — | Optional: aspect ratio, no-text requirement |

**Score: 2/6 elements defined**

### What's Working
You have a clear subject (cat) and action (sitting). This is a good foundation.

### Key Improvements
1. **Specify the cat** — "a fluffy gray Persian" or "a sleek black shorthair"
2. **Add location** — Where is it sitting? This contextualizes the entire image
3. **Choose a style** — Photography? Illustration? This dramatically affects the output
```

### Analysis with --fix

User: `/prompt-anatomy "a mountain landscape" --fix`

Response:

```
## Prompt Analysis

**Original prompt:** "a mountain landscape"

| Element | Status | Found | Suggestion |
|---------|--------|-------|------------|
| Subject | △ | "mountain" | Add: specific range, season, conditions |
| Composition | ✗ | — | Add: wide panorama, foreground interest, rule of thirds |
| Action | ✗ | — | Add: weather movement, light changes, wildlife |
| Location | △ | "landscape" | Already implied; add region or biome specifics |
| Style | ✗ | — | Add: photography style, time of day, color treatment |
| Constraints | ✗ | — | Consider: aspect ratio for landscape (16:9?) |

**Score: 2/6 elements defined**

### What's Working
Clear subject matter. "Landscape" suggests composition intent.

### Key Improvements
1. **Specify the mountains** — Alpine? Desert range? Snow-capped?
2. **Add dramatic lighting** — Golden hour, stormy sky, misty dawn
3. **Include foreground** — Wildflowers, rocky outcrop, winding path

## Fixed Prompt

"A dramatic alpine mountain range with snow-capped peaks piercing through morning clouds. Golden sunrise light illuminating the eastern faces while western slopes remain in cool shadow. Wide panoramic composition with a meadow of wildflowers in the foreground leading the eye toward the distant summits. Landscape photography style with rich, saturated colors and sharp detail throughout."
```

### Verbose Analysis

User: `/prompt-anatomy "cyberpunk city at night" --verbose`

Response:

```
## Prompt Analysis

**Original prompt:** "cyberpunk city at night"

| Element | Status | Found | Suggestion |
|---------|--------|-------|------------|
| Subject | △ | "cyberpunk city" | Good genre. Add: specific elements—neon signs, flying cars, crowds |

> **Why Subject matters:** "Cyberpunk city" is a genre descriptor, not a specific subject. The AI needs anchor points: a specific building, street scene, or character to focus on.

| Composition | ✗ | — | Add: street-level view, aerial shot, window POV |

> **Why Composition matters:** Without framing guidance, the AI chooses arbitrarily. A street-level shot creates intimacy; an aerial view shows scale. This choice fundamentally shapes the image.

| Action | ✗ | — | Add: rain falling, crowds moving, vehicles flying |

> **Why Action matters:** Static cityscapes feel lifeless. Movement—rain, people, vehicles—adds energy and story to the scene.

| Location | ✓ | "city at night" | Solid foundation. Could specify district type |

> **Why Location matters:** "At night" establishes mood and lighting. Consider: is this a slum, corporate district, market area?

| Style | △ | "cyberpunk" | Genre implies style, but add: Blade Runner influence? Anime? Photorealistic? |

> **Why Style matters:** "Cyberpunk" suggests neon and tech, but there's huge visual variety—from gritty photorealism to clean anime aesthetics.

| Constraints | ✗ | — | Consider: aspect ratio (vertical for towers, wide for panorama) |

> **Why Constraints matter:** Aspect ratio shapes composition. A vertical 9:16 emphasizes towering buildings; 21:9 ultrawide creates cinematic scope.

**Score: 2/6 elements defined**
```

## Tips for Users

When reviewing analysis results:
- Start with ✗ Missing elements — these have the biggest impact
- △ Weak elements need more specific language, not more words
- Don't feel obligated to fill Constraints unless you have specific needs
- Style is often the difference between generic and striking results
