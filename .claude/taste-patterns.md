# Taste Patterns Reference

This document defines patterns, thresholds, and mappings used by the taste layer for image prompt enhancement. Referenced by both `/taste-check` and `/image-prompt` skills.

---

## Cliche Patterns

Patterns are organized by severity level. Each includes the problem it causes and a suggested replacement.

### High Severity (Always Flag)

These patterns should always be flagged regardless of sensitivity setting.

| Pattern | Problem | Replacement |
|---------|---------|-------------|
| "trending on ArtStation" | 47% token collision rate | Remove, or specify actual artist technique |
| "hyper-realistic" + "8K/4K" | Quality spam, adds nothing | "Photographic with sharp focus" |
| "masterpiece, best quality" | Filler tokens | Remove entirely |
| "ultra detailed" | Meaningless intensifier | Describe specific details instead |

### Medium Severity (Flag at Medium+ Sensitivity)

These patterns are flagged when sensitivity is set to medium or higher.

| Pattern | Problem | Replacement |
|---------|---------|-------------|
| "epic lighting" | Vague, overused | "Rembrandt lighting at 45 degrees with deep shadows" |
| "dramatic lighting" | Means nothing specific | "Single key light from upper left, no fill" |
| "cinematic" (alone) | Too broad | "Anamorphic lens, 2.39:1 ratio, teal-orange grade" |
| "beautiful woman/man" | Generic | Specific features, age, expression, distinguishing marks |
| Artist name in isolation | Pastiche without technique | Add specific technique: "Moebius-style clean linework" |
| "highly detailed" | Filler | Describe what details matter |

### Low Severity (Flag at High Sensitivity Only)

These patterns are only flagged when sensitivity is set to high.

| Pattern | Problem | Replacement |
|---------|---------|-------------|
| "ethereal" | Overused in AI art | Describe specific light quality |
| "mysterious" | Telling not showing | Describe what creates the mystery |
| "glowing" | AI art cliche | Specify light source and behavior |
| "stunning" | Empty superlative | Remove or specify what makes it striking |

---

## Specificity Thresholds

Guidelines for prompt length and modifier density to avoid over-specification.

| Level | Word Count | Modifiers per Element | Action |
|-------|------------|----------------------|--------|
| Acceptable | < 120 words | <= 2 | No warning |
| Warning | 120-180 words | 3 | Soft warning |
| Over-specified | > 180 words | > 3 | Strong warning |

**Notes:**
- Word count refers to the total prompt length
- "Modifiers per element" means adjectives/adverbs stacked on a single noun or concept
- Over-specification often leads to model confusion and inconsistent outputs

---

## Sensitivity Levels

Controls which patterns are flagged during taste checks.

| Level | What's Flagged |
|-------|----------------|
| **Low** | Only high-severity patterns |
| **Medium** (default) | High + medium severity, mild specificity warnings |
| **High** | All patterns, strict specificity limits |

**Usage:**
- Use **low** for experienced users who want minimal intervention
- Use **medium** (default) for balanced guidance
- Use **high** for learning mode or when quality is paramount

---

## Intent Mappings

Maps emotional/atmospheric intents to concrete visual techniques.

| Intent | Enhancement Direction |
|--------|----------------------|
| "peaceful" | Soft light, muted colors, open space, horizontal lines |
| "tense" | High contrast, tight framing, diagonal lines, shadows |
| "nostalgic" | Warm tones, film grain, soft focus, golden hour |
| "energetic" | Saturated colors, dynamic angles, motion blur |
| "mysterious" | Low key lighting, partial reveals, fog/atmosphere |
| "intimate" | Close framing, shallow DOF, warm palette |
| "epic" | Wide angle, dramatic scale, strong verticals |
| "joyful" | Bright colors, open composition, upward angles |
| "melancholic" | Desaturated, cool tones, empty space, downward gaze |
| "dramatic" | High contrast, rim lighting, strong shadows |

**Usage:**
- When a user specifies an intent, translate it to these concrete techniques
- Multiple intents can be combined if they don't conflict
- Prefer specific techniques over abstract mood words in final prompts
