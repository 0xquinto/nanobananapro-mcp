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

See `/enhance-prompt` for the authoritative element definitions. Elements: **Subject**, **Composition**, **Action**, **Location**, **Style**, **Constraints**.

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

| Element | ✓ Present | △ Weak | ✗ Missing |
|---------|-----------|--------|-----------|
| Subject | Specific noun with details ("weathered wooden fishing boat with peeling blue paint") | Generic ("a boat", "a person") | No clear subject |
| Composition | Shot type AND angle ("close-up from low angle") | Only one aspect ("close-up") | No framing info |
| Action | Dynamic state ("leaping through morning mist") | Static/implied ("sitting") | No indication |
| Location | Environment + atmosphere ("misty harbor with old stone walls at dawn") | Generic ("in a park") | No context |
| Style | Clear treatment ("oil painting, Dutch masters style, warm palette") | Vague ("artistic", "beautiful") | No style |
| Constraints | Explicit requirements ("text reading 'OPEN', square format") | Implied or ineffective | Usually fine if none needed |

### Constraint Language

Negative prompting works better when you specify what you *do* want instead.

| Goal | Weak | Strong |
|------|------|--------|
| No text | "no text" | "without any text or lettering" |
| No people | "no people" | "empty scene, unoccupied space" |
| Plain background | "simple background" | "solid white background, no distractions" |
| No specific object | "no [object]" | "scene without [object], [alternative focus]" |

**Example:** "a park with no people" → "Empty street at dawn"

## Options

| Flag | Behavior |
|------|----------|
| `--fix` | Append a complete rewritten prompt addressing all gaps |
| `--verbose` | Add "Why X matters" educational notes after each element row |
| `--format=json` | Output structured JSON instead of markdown |

## JSON Output

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

## Example

User: `/prompt-anatomy "cyberpunk city at night" --verbose --fix`

```
## Prompt Analysis

**Original prompt:** "cyberpunk city at night"

| Element | Status | Found | Suggestion |
|---------|--------|-------|------------|
| Subject | △ | "cyberpunk city" | Add: specific elements—neon signs, flying cars, crowds |

> **Why Subject matters:** "Cyberpunk city" is a genre descriptor, not a specific subject. The AI needs anchor points: a specific building, street scene, or character to focus on.

| Composition | ✗ | — | Add: street-level view, aerial shot, window POV |

> **Why Composition matters:** Without framing guidance, the AI chooses arbitrarily. A street-level shot creates intimacy; an aerial view shows scale.

| Action | ✗ | — | Add: rain falling, crowds moving, vehicles flying |

> **Why Action matters:** Static cityscapes feel lifeless. Movement—rain, people, vehicles—adds energy and story.

| Location | ✓ | "city at night" | Solid foundation. Could specify district type |

> **Why Location matters:** "At night" establishes mood. Consider: slum, corporate district, market area?

| Style | △ | "cyberpunk" | Genre implies style. Add: Blade Runner? Anime? Photorealistic? |

> **Why Style matters:** "Cyberpunk" suggests neon and tech, but there's huge visual variety—from gritty realism to clean anime.

| Constraints | ✗ | — | Consider: aspect ratio (9:16 for towers, 21:9 for panorama) |

> **Why Constraints matter:** Aspect ratio shapes composition. Vertical emphasizes height; ultrawide creates cinematic scope.

**Score: 2/6 elements defined**

### What's Working
Clear genre and time of day. "At night" provides lighting context.

### Key Improvements
1. **Anchor the subject** — Focus on a specific element: street corner, building, character
2. **Add movement** — Rain, crowds, flying vehicles bring the scene to life
3. **Specify style** — Blade Runner grit? Anime neon? This choice shapes everything

## Fixed Prompt

"A rain-slicked street corner in a cyberpunk megacity at night. Neon signs in Japanese and English cast pink and cyan reflections on wet pavement. Crowds with umbrellas hurry past steaming food stalls while flying vehicles streak overhead. Street-level shot looking up at towering corporate spires disappearing into smog. Blade Runner-inspired cinematography with film grain. 21:9 aspect ratio."
```

**Note:** Without `--verbose`, the "Why X matters" blocks are omitted. Without `--fix`, the fixed prompt is omitted.

## Tips for Users

When reviewing analysis results:
- Start with ✗ Missing elements — these have the biggest impact
- △ Weak elements need more specific language, not more words
- Don't feel obligated to fill Constraints unless you have specific needs
- Style is often the difference between generic and striking results
