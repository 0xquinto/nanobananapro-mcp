# Taste Patterns Reference

This document defines patterns, thresholds, and mappings used by the taste layer for image prompt enhancement. Referenced by both `/taste-check` and `/image-prompt` skills.

---

## Pattern Universality

Patterns in this file are tagged:
- `[UNIVERSAL]` — Applies to all major image models
- `[GEMINI]` — Specific to Gemini 3 Pro behavior
- `[LEGACY]` — From older models, may not apply

When in doubt, prefer universal patterns.

---

## Cliche Patterns

Patterns are organized by severity level. Each includes the problem it causes and a suggested replacement.

### High Severity (Always Flag)

These patterns should always be flagged regardless of sensitivity setting.

| Pattern | Problem | Replacement | Tag |
|---------|---------|-------------|-----|
| "trending on ArtStation" | 47% token collision rate | Remove, or specify actual artist technique | `[UNIVERSAL]` |
| "hyper-realistic" + "8K/4K" | Quality spam, adds nothing | "Photographic with sharp focus" | `[UNIVERSAL]` |
| "masterpiece, best quality" | Filler tokens | Remove entirely | `[UNIVERSAL]` |
| "ultra detailed" | Meaningless intensifier | Describe specific details instead | `[UNIVERSAL]` |

### Medium Severity (Flag at Medium+ Sensitivity)

These patterns are flagged when sensitivity is set to medium or higher.

| Pattern | Problem | Replacement | Tag |
|---------|---------|-------------|-----|
| "epic lighting" | Vague, overused | "Rembrandt lighting at 45 degrees with deep shadows" | `[UNIVERSAL]` |
| "dramatic lighting" | Means nothing specific | "Single key light from upper left, no fill" | `[UNIVERSAL]` |
| "cinematic" (alone) | Too broad | "Anamorphic lens, 2.39:1 ratio, teal-orange grade" | `[UNIVERSAL]` |
| "beautiful woman/man" | Generic | Specific features, age, expression, distinguishing marks | `[UNIVERSAL]` |
| Artist name in isolation | Pastiche without technique | Add specific technique: "Moebius-style clean linework" | `[UNIVERSAL]` |
| "highly detailed" | Filler | Describe what details matter | `[UNIVERSAL]` |

### Low Severity (Flag at High Sensitivity Only)

These patterns are only flagged when sensitivity is set to high.

| Pattern | Problem | Replacement | Tag |
|---------|---------|-------------|-----|
| "ethereal" | Overused in AI art | Describe specific light quality | `[UNIVERSAL]` |
| "mysterious" | Telling not showing | Describe what creates the mystery | `[UNIVERSAL]` |
| "glowing" | AI art cliche | Specify light source and behavior | `[UNIVERSAL]` |
| "stunning" | Empty superlative | Remove or specify what makes it striking | `[UNIVERSAL]` |

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

## Intent Mappings

Translate emotional intents to concrete visual techniques. Multiple intents can combine if compatible.

| Intent | Techniques |
|--------|------------|
| peaceful | Soft light, muted colors, open space, horizontal lines |
| tense | High contrast, tight framing, diagonal lines, shadows |
| nostalgic | Warm tones, film grain, soft focus, golden hour |
| energetic | Saturated colors, dynamic angles, motion blur |
| mysterious | Low key lighting, partial reveals, fog/atmosphere |
| intimate | Close framing, shallow DOF, warm palette |
| epic | Wide angle, dramatic scale, strong verticals |
| joyful | Bright colors, open composition, upward angles |
| melancholic | Desaturated, cool tones, empty space, downward gaze |
| dramatic | High contrast, rim lighting, strong shadows |

---

## Accessibility Patterns

| Pattern | Severity | Concern |
|---------|----------|---------|
| "tiny text" | High | Likely illegible |
| "low contrast" | Medium | Hard to see |
| "intricate small details" | Medium | May not render clearly |
| "complex typography" | Medium | Accessibility risk |
| "subtle tones" | Low | May reduce readability |
| "monochromatic" | Low | Check for sufficient variation |

---

## Content Consideration Patterns

| Pattern | Flag | Note |
|---------|------|------|
| "portrait", "face", "person" | [FACE] | Human face generation |
| "crowd", "group of people" | [CROWD] | Multiple faces |
| "child", "kid", "baby" | [SENSITIVE] | Extra care |
| "logo", brand names | [BRAND] | Trademark |
