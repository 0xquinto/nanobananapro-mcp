---
name: taste-check
description: Analyze prompts for aesthetic quality, accessibility, and content considerations.
  Detects clichés, checks specificity, evaluates intent clarity, and flags potential issues.
argument-hint: '"your prompt here" [--learn] [--taste=low|medium|high] [--fix] [--accessibility] [--format=json]'
---

# /taste-check

Analyze image prompts for aesthetic quality before generation.

## What It Checks

| Check | What It Detects |
|-------|-----------------|
| **Intent clarity** | Does the prompt convey what the viewer should feel? |
| **Clichés** | Generic AI-art patterns that produce homogeneous results |
| **Specificity** | Is the prompt over-specified (mode collapse risk) or under-specified (vague)? |
| **Accessibility hints** | Prompts that may produce low-contrast or hard-to-read images |
| **Content flags** | Potentially problematic patterns (faces, crowds, sensitive topics) |

## Flags

| Flag | Behavior |
|------|----------|
| `--learn` | Add explanations for why each issue matters |
| `--taste=low\|medium\|high` | Adjust detection sensitivity (default: medium) |
| `--fix` | Output only the improved prompt, skip analysis |
| `--accessibility` | Include accessibility-focused checks (contrast, readability) |

## Output Format

```
TASTE CHECK                        # With --learn: "TASTE CHECK (Learning Mode)"
===========

Prompt: [original prompt]

INTENT CLARITY: [Clear / Vague / Missing]
[Brief assessment]
  # With --learn: "Why this matters: [explanation]"

CLICHÉS DETECTED: [count]
- [cliché]: [where it appears]
  # With --learn: "Why this matters: [explanation]"

SPECIFICITY: [Under-specified / Good / Warning / Over-specified]
Word count: [N] words
[Assessment]
  # With --learn: "Why this matters: [explanation]"

OVERALL: [Pass / Needs Work / Rethink]
[One-line summary]
```

**With --fix**: Returns only the improved prompt, no analysis.

## JSON Output (`--format=json`)

```json
{
  "status": "pass|warn|fail",
  "prompt": "analyzed prompt",
  "intent_clarity": {
    "detected": true|false,
    "inferred_intent": "string or null"
  },
  "cliches": [
    {
      "pattern": "epic lighting",
      "severity": "high|medium|low",
      "suggestion": "Low sun backlighting with long shadows"
    }
  ],
  "specificity": {
    "word_count": 87,
    "status": "good|warning|over-specified",
    "threshold": 120
  },
  "accessibility_hints": [
    {
      "pattern": "low contrast",
      "severity": "medium",
      "suggestion": "Add ensuring readable contrast"
    }
  ],
  "content_flags": ["FACE", "SENSITIVE"],
  "improved_prompt": "fixed version if --fix"
}
```

## Sensitivity Levels

| Level | Flags |
|-------|-------|
| **low** | High-severity clichés only |
| **medium** (default) | High + medium severity |
| **high** | All patterns, strict specificity |

See `taste-patterns.md` for complete pattern definitions.

## Extended Checks

Accessibility and content patterns are defined in `taste-patterns.md`. Key behaviors:

- **Accessibility hints** (`--accessibility`): Flags contrast, readability, and color blindness concerns
- **Content flags**: `[FACE]`, `[CROWD]`, `[SENSITIVE]`, `[BRAND]` - informational only, does not block generation

## Specificity Assessment

| Level | Word Count | Notes |
|-------|------------|-------|
| Under-specified | < 30 | Generic results likely |
| Good | 30-120 | Balanced |
| Warning | 120-180 | Approaching over-specified |
| Over-specified | > 180 | Mode collapse risk |

Word count is a heuristic. A 50-word prompt of pure adjectives may be under-specified for *meaning* while a 25-word narrative prompt may suffice.

## Intent Clarity

| Clear Intent | Vague Intent |
|--------------|--------------|
| Emotional target ("evoke melancholy") | Pure description without direction |
| Viewer relationship ("intimate close-up") | Listing elements without relationship |
| Narrative moment ("before the storm") | Generic mood words ("beautiful", "epic") |
| Atmosphere anchored to references | No sense of moment |

See `taste-patterns.md` for intent-to-technique mappings.

## Example

```
> /taste-check "A beautiful sunset over mountains with dramatic lighting,
  cinematic composition, highly detailed, 8k"

TASTE CHECK
===========

Prompt: A beautiful sunset over mountains with dramatic lighting...

INTENT CLARITY: Vague
Generic "beautiful" scene with no emotional target or narrative moment.

CLICHÉS DETECTED: 4
- "beautiful": Empty superlative
- "dramatic lighting": Over-used, non-specific
- "cinematic composition": Meaningless without reference
- "highly detailed, 8k": Technical suffix that adds nothing

SPECIFICITY: Under-specified
Word count: 14 words
All description, no substance. Which mountains? What time of year?

OVERALL: Rethink
This prompt will produce a generic AI sunset.
```

**With --fix** on the same prompt:

```
Late autumn sunset over the Dolomites, the last light catching fresh
snow on the Tre Cime while the valleys below sink into blue shadow.
A solitary rifugio glows warm against the cold peaks. The moment before
the alpenglow fades completely, that held-breath stillness.
```

## Usage Tips

1. Run taste-check BEFORE generation to catch issues early
2. Use `--learn` when building prompt intuition
3. Use `--fix` for quick iteration
4. Adjust `--taste` based on output criticality
5. See `taste-patterns.md` for cliché dictionary, intent mappings, and accessibility patterns