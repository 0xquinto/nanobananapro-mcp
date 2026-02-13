# Nano Banana Pro — Cheatsheet

**IMPORTANT: When the user asks to generate, edit, compose, or work with images, you MUST use the `mcp__nanobananapro__*` tools listed below. Do NOT use any other image tools.**

## Tool Routing

| Task | Tool to call |
|------|------|
| Single image from text | `mcp__nanobananapro__generate_image` |
| Modify an existing image | `mcp__nanobananapro__edit_image` |
| Combine multiple reference images | `mcp__nanobananapro__compose_images` |
| Real-time data or factual imagery | `mcp__nanobananapro__search_grounded_image` |
| Mixed text + image content (recipes, tutorials, stories) | `mcp__nanobananapro__generate_interleaved` |
| Iterative refinement (multiple rounds) | `mcp__nanobananapro__start_image_chat` → `mcp__nanobananapro__continue_image_chat` |
| Done iterating | `mcp__nanobananapro__end_image_chat` |
| List active sessions | `mcp__nanobananapro__list_chat_sessions` |

**Decision flow:** New image from scratch → `mcp__nanobananapro__generate_image`. Need to tweak an existing file → `mcp__nanobananapro__edit_image`. Merging style/pose/background from separate references → `mcp__nanobananapro__compose_images`. Need current facts or data → `mcp__nanobananapro__search_grounded_image`. Want paragraphs interspersed with visuals → `mcp__nanobananapro__generate_interleaved`. Expect 2+ rounds of revision → use a chat session.

## Prompt Engineering

**Structure:** Use the 6-component formula — Subject + Action + Environment + Style + Lighting + Details. Write full descriptive sentences, not comma-separated keywords.

**Context:** Include purpose ("for a Brazilian gourmet cookbook cover") so the model infers style. Overly simple prompts get over-thought by the reasoning engine — add detail to guide it.

**Text rendering:** Enclose exact text in double quotes. Keep rendered text under 25 characters. Describe font style ("bold white sans-serif"), not font names. Use 3-level hierarchy (headline, subheader, body). Allocate 30%+ white space.

**Aspect ratio:** State it in the prompt ("a 9:16 vertical poster") AND via the `aspect_ratio` parameter.

## Parameters

**Resolution:**
- `1K` — iteration and prototyping (default for generate/edit)
- `2K` — balanced quality (default for compose/search_grounded)
- `4K` — final production assets only (~79% more tokens)

**Safety:** Optional `safety` parameter on all generation tools. Values: `block_none`, `block_low`, `block_medium`, `block_high`. Omit for API defaults.

**Model:** `"pro"` or `"nano-banana-pro"` (aliases for `gemini-3-pro-image-preview`). Use Pro for production assets, text-heavy graphics, character-consistent series, and 4K output.

**Seed:** Integer 0–2147483647 for reproducible output. Same seed + same prompt = same result.

## Workflows

**Iterative editing:** If an image is 80%+ right, use `edit_image` or a chat session for targeted fixes — don't regenerate from scratch. Complex multi-object edits may need multiple chat turns. When retrying after failure, refine the prompt — never retry verbatim.

**Character consistency:** State "Keep facial features exactly the same as the reference." Reuse identical descriptive language for fixed traits across prompts. Build 360° character sheets (front, left, right, back) first, then use as anchors. Up to 5 people in group shots, up to 6 high-fidelity references (14 total).

**Multi-image composition:** Assign each reference a role: "Image A: character pose; Image B: art style; Image C: background." Control layers allow separate references for face, pose, clothing, setting.

**Structural control:** Upload sketches, wireframes, or grid layouts as input to control composition — the model uses them as layout guides.

**Storyboarding:** Request "generate images one at a time" with identity consistency constraints. Specify aspect ratio per frame.

**Search grounding:** Use `search_grounded_image` for infographics with real-time data. Always verify facts in output.

**Infographics:** S-curve/zigzag for step-by-step, bento grids for modular overviews. Sequential palettes (light-to-dark) for numbers, qualitative palettes (distinct colors) for categories.

## Avoid

- Tag-soup prompts (comma-separated keywords instead of sentences)
- Long text strings (>25 chars) in rendered text
- 4K resolution for drafts or iteration
- Re-rolling instead of editing when image is close
- Vague prompts without purpose or context
- Retrying the exact same prompt after failure
- Dates without explicit year (model defaults to 2023)
