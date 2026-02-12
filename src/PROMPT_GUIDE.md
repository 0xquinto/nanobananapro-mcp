# Nano Banana Pro — Prompt Engineering Rules

**Prompt structure:** Always use the 6-component formula: Subject + Action + Environment + Style + Lighting + Details. Write full descriptive sentences, not comma-separated keywords. Specify aspect ratio explicitly in the prompt ("a 9:16 vertical poster") or via parameter.

**Provide context:** Include the purpose ("for a Brazilian gourmet cookbook cover") so the model can infer appropriate style choices. Overly simple prompts get "over-thought" by the reasoning engine — add detail to guide it.

**Text rendering:** Enclose exact text in double quotes. Keep rendered text under 25 characters for reliability. Describe font style ("bold white sans-serif"), not font names. Use 3-level text hierarchy: Level 1 headline, Level 2 subheaders, Level 3 body copy. Allocate 30%+ white space for professional look.

**Editing workflow:** If an image is 80%+ right, use `edit_image` or chat sessions for targeted fixes. Don't regenerate from scratch. Complex multi-object edits may need multiple conversational turns. When retrying after failure, refine the prompt — don't retry verbatim.

**Resolution:**
- 1K — iteration and prototyping
- 2K — balanced quality (default)
- 4K — final production assets only (~79% more tokens)

**Model selection:** Use Flash for quick edits, style transfers, and high-volume low-cost work. Use Pro for production assets, text-heavy graphics, character-consistent series, and 4K output.

**Character consistency:** When using reference images, state "Keep facial features exactly the same as the reference." Reuse identical descriptive language for fixed traits across prompts. Build 360-degree character sheets first (front, left, right, back views), then use as anchors for new scenes. Supports up to 5 people in group shots, up to 6 high-fidelity reference images (14 total).

**Multi-image composition:** Assign each reference image a role: "Image A: character pose; Image B: art style; Image C: background." Control layers allow separate references for face, pose, clothing, and setting.

**Structural control:** Upload sketches, wireframes, or grid layouts as input images to control composition. The model treats them as layout guides, not content to reproduce.

**Storyboarding:** For sequential narrative art, request "generate images one at a time" with identity consistency constraints. Specify aspect ratio per frame.

**Search grounding:** Use `search_grounded_image` for infographics with real-time data, current events, or factual imagery. Always verify facts in output.

**Infographic patterns:** Use S-curve/zigzag layouts for step-by-step processes, bento grids for modular overviews. Use sequential palettes (light-to-dark) for numerical data, qualitative palettes (distinct colors) for categories.

**Date bias:** The model defaults to dates within 2023 — specify dates explicitly when needed.

**Avoid:** Tag soup prompts, long text strings, 4K for drafts, re-rolling instead of editing, vague prompts without context, using Pro for simple edits.
