---
name: taste-check
description: Analyze prompts for aesthetic quality. Detects clichés, checks specificity,
  evaluates intent clarity. Use when reviewing a prompt before generation or learning
  what makes prompts generic.
argument-hint: '"your prompt here" [--learn] [--taste=low|medium|high] [--fix]'
---

# /taste-check

Analyze image prompts for aesthetic quality before generation.

## What It Checks

| Check | What It Detects |
|-------|-----------------|
| **Intent clarity** | Does the prompt convey what the viewer should feel? |
| **Clichés** | Generic AI-art patterns that produce homogeneous results |
| **Specificity** | Is the prompt over-specified (mode collapse risk) or under-specified (vague)? |

## Flags

| Flag | Behavior |
|------|----------|
| `--learn` | Add explanations for why each issue matters |
| `--taste=low\|medium\|high` | Adjust detection sensitivity (default: medium) |
| `--fix` | Output only the improved prompt, skip analysis |

## Output Format

### Standard Output

```
TASTE CHECK
===========

Prompt: [original prompt]

INTENT CLARITY: [Clear / Vague / Missing]
[Brief assessment of what emotion/response the prompt targets]

CLICHÉS DETECTED: [count]
- [cliché 1]: [where it appears]
- [cliché 2]: [where it appears]

SPECIFICITY: [Under-specified / Good / Warning / Over-specified]
Word count: [N] words
[Assessment of balance]

OVERALL: [Pass / Needs Work / Rethink]
[One-line summary]
```

### With --learn Flag

```
TASTE CHECK (Learning Mode)
===========================

Prompt: [original prompt]

INTENT CLARITY: [Clear / Vague / Missing]
[Brief assessment]

  Why this matters: Intent clarity determines whether the image will
  evoke the response you want. Vague intent leads to technically correct
  but emotionally flat images.

CLICHÉS DETECTED: [count]
- [cliché]: [where it appears]

  Why this matters: [Explanation of why this cliché produces generic
  results and what alternatives exist]

SPECIFICITY: [Level]
Word count: [N] words

  Why this matters: Under-specified prompts rely on model defaults
  (often generic). Over-specified prompts cause mode collapse where
  the model struggles to satisfy all constraints.

OVERALL: [Rating]
[Summary with learning takeaways]
```

### With --fix Flag

```
[Improved prompt only - no analysis, no explanation]
```

## Sensitivity Levels

- **low**: Only flag the most egregious issues. Best for experienced users who want a quick sanity check.
- **medium** (default): Balanced detection. Flags common clichés and clear specificity issues.
- **high**: Strict mode. Flags subtle clichés, borderline specificity, and any ambiguous intent. Best for learning or high-stakes generations.

## Specificity Assessment

| Level | Word Count | Assessment |
|-------|------------|------------|
| Under-specified | < 30 words | May produce generic results |
| Good | 30-120 words | Balanced |
| Warning | 120-180 words | Approaching over-specified |
| Over-specified | > 180 words | Risk of mode collapse |

Word count alone is not determinitive. A 50-word prompt with only adjectives may be under-specified for *meaning* while a 25-word prompt with strong narrative elements may be sufficient.

## Intent Clarity Indicators

**Clear intent signals:**
- Emotional target stated ("evoke melancholy", "create tension")
- Viewer relationship defined ("intimate close-up", "voyeuristic distance")
- Narrative moment specified ("just before the storm breaks")
- Atmosphere/mood anchored to concrete references

**Vague intent signals:**
- Pure description without emotional direction
- Listing visual elements without relationship
- Generic mood words without grounding ("beautiful", "epic", "stunning")
- No sense of moment or narrative

## Examples

### Basic Analysis

```
> /taste-check "A beautiful sunset over mountains with dramatic lighting,
  cinematic composition, highly detailed, 8k"

TASTE CHECK
===========

Prompt: A beautiful sunset over mountains with dramatic lighting,
cinematic composition, highly detailed, 8k

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
What should the viewer feel?

OVERALL: Rethink
This prompt will produce a generic AI sunset. Consider: What makes THIS
sunset different from every other AI sunset?
```

### With --learn

```
> /taste-check --learn "ethereal goddess in flowing robes"

TASTE CHECK (Learning Mode)
===========================

Prompt: ethereal goddess in flowing robes

INTENT CLARITY: Vague
No emotional target beyond "impressive figure."

  Why this matters: Without intent, the model defaults to its most
  common interpretation of "goddess" - typically a generic beautiful
  woman in white fabric. The image will be technically competent but
  indistinguishable from thousands of similar generations.

CLICHÉS DETECTED: 2
- "ethereal": AI-art staple that triggers homogeneous soft-glow aesthetic
- "flowing robes": Default goddess attire, signals nothing specific

  Why this matters: These terms appear in millions of AI prompts. The
  model has learned to map them to a narrow visual range. Using them
  guarantees your image looks like everyone else's "ethereal goddess."

SPECIFICITY: Under-specified
Word count: 5 words

  Why this matters: Five words cannot differentiate your vision from
  the model's defaults. You're essentially asking for "the average of
  all goddess images in training data."

OVERALL: Rethink
Ask yourself: What goddess? From what culture? In what moment?
Feeling what emotion? Why should anyone care about this image?
```

### With --fix

```
> /taste-check --fix "A beautiful sunset over mountains with dramatic
  lighting, cinematic composition, highly detailed, 8k"

Late autumn sunset over the Dolomites, the last light catching fresh
snow on the Tre Cime while the valleys below sink into blue shadow.
A solitary rifugio glows warm against the cold peaks. The moment before
the alpenglow fades completely, that held-breath stillness.
```

## Integration

Pattern definitions are maintained in `.claude/taste-patterns.md`. The taste-check skill references this file for:

- Cliché dictionary and severity levels
- Cultural and temporal context for patterns
- Positive alternatives for common clichés
- Domain-specific pattern variations (portrait, landscape, abstract, etc.)

## Usage Tips

1. Run taste-check BEFORE generation to catch issues early
2. Use `--learn` when building prompt intuition
3. Use `--fix` for quick iteration when you trust the suggestions
4. Adjust `--taste` based on how critical the output is
5. Check patterns file for domain-specific cliché lists
