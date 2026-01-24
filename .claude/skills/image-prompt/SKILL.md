---
name: image-prompt
description: Full image generation workflow from rough concept to final image.
  Use when user wants to generate an image, create visuals, or says "make me
  an image of...". Enhances prompts, selects appropriate MCP tool, handles
  iteration. The primary skill for image creation.
argument-hint: "your image idea" [--chat] [--refs=path] [--style=preset] [--dry-run] [--format=json] [--seed=N]
---

# Image Prompt

The master skill for image generation. Takes a rough concept through enhancement, generation, and iteration.

## Workflow Overview

```
Rough concept
    ↓
Parse intent & detect flags
    ↓
★ INTENT QUESTION ★              ← "What should the viewer feel?"
    ↓
Check project context (style-guide.md, style-library.md, references/)
    ↓
★ REFERENCE CALIBRATION ★        ← Extract taste from references/ if present
    ↓
Gap analysis (6-element check)
    ↓
Clarify if needed (missing critical elements)
    ↓
Enhance prompt (embed 6-element formula)
    ↓
★ TASTE CHECK ★                  ← Clichés, specificity (unless --no-taste)
    ↓
If issues found → Summary block (fix/skip/details)
    ↓
Show enhanced prompt for approval
    ↓
Select MCP tool based on scenario
    ↓
Generate image
    ↓
★ CRITIQUE OFFER ★               ← "critique" to reflect on result
    ↓
Offer iteration options
    ↓
Save and log (if in project)
```

## Options

| Flag | Description |
|------|-------------|
| `--chat` | Use multi-turn session for iterative refinement |
| `--refs=<path>` | Include reference images for composition |
| `--style=<preset>` | Apply preset from style-library.md |
| `--output=<path>` | Save to specific location |
| `--resolution=1K\|2K\|4K` | Set output resolution (default: 2K) |
| `--aspect=<ratio>` | Set aspect ratio (e.g., 16:9, 3:4) |
| `--grounded` | Use search-grounded generation for real-world data |
| `--project=<path>` | Use specific project's context |
| `--taste=low\|medium\|high` | Cliche detection sensitivity (default: medium) |
| `--learn` | Show reasoning for taste suggestions |
| `--no-taste` | Skip taste checks (speed mode) |
| `--dry-run` | Preview prompt and settings without generating |
| `--format=json` | Machine-readable JSON output |
| `--seed=<n>` | Seed for reproducible generation (0-2147483647) |

## Dry Run Mode

When `--dry-run` is specified, the skill performs all analysis and enhancement steps but stops before calling any MCP tool.

**Output includes:**
- Enhanced prompt (final version after taste check)
- Gap analysis results
- Taste check summary
- Tool that would be called
- All parameters that would be passed

**Use cases:**
- Review prompt enhancement before spending API credits
- Debug prompt issues without generating images
- Script validation in CI/CD pipelines
- Training/learning prompt engineering

**Example:**
```
User: /image-prompt a wizard --dry-run

[Performs all steps through Step 6]

## Dry Run Summary

**Would call:** `generate_image`
**Enhanced prompt:** "An elderly wizard with..."
**Parameters:**
- aspect_ratio: 3:4
- resolution: 2K
- output_path: ./output/wizard-001.png

No image generated (dry run mode).
```

## Output Formats

### Human (default)

Markdown-formatted output with headers, tables, and prose. Designed for interactive use.

### JSON (`--format=json`)

Machine-readable JSON output for scripting and automation. Structure:

```json
{
  "status": "success|error",
  "original_prompt": "user input",
  "enhanced_prompt": "enhanced version",
  "intent": "stated emotional intent or null",
  "gap_analysis": {
    "subject": "present|vague|missing",
    "composition": "present|vague|missing",
    "action": "present|vague|missing",
    "location": "present|vague|missing",
    "style": "present|vague|missing",
    "constraints": "present|vague|missing"
  },
  "taste_check": {
    "cliches_found": ["pattern1", "pattern2"],
    "specificity_score": 87,
    "issues": []
  },
  "tool": "generate_image",
  "parameters": {
    "prompt": "...",
    "aspect_ratio": "3:4",
    "resolution": "2K",
    "output_path": "./output/..."
  },
  "result": {
    "saved_path": "/absolute/path/to/image.png",
    "text": "model response"
  }
}
```

**Error format:**
```json
{
  "status": "error",
  "error_type": "validation|api|file",
  "message": "Human-readable error",
  "original_prompt": "user input"
}
```

## Reproducibility

Use `--seed=<n>` for deterministic generation. Same seed + same prompt = same image (within model constraints).

**Use cases:** A/B testing, regenerating approved concepts, debugging, batch generation.

Seed is logged in asset-log.md. Note: actual reproducibility depends on Gemini API behavior.

## MCP Tool Selection

### Decision Tree

```
Has existing image?
├── NO (fresh generation)
│   ├── --refs flag      → compose_images
│   ├── --grounded flag  → search_grounded_image
│   ├── --chat flag      → start_image_chat
│   └── default          → generate_image
│
└── YES (modifying)
    ├── Active session?  → continue_image_chat
    ├── Multiple rounds? → start_image_chat
    └── Single edit?     → edit_image
```

### Tool Selection Guide

| Tool | When | Indicator |
|------|------|-----------|
| `generate_image` | One-shot generation | No special flags or context |
| `edit_image` | Single discrete change | "make it bluer", "add a hat" |
| `start_image_chat` | Iterative exploration | `--chat` flag, "let's try", "help me refine" |
| `continue_image_chat` | Already in session | Active session ID exists |
| `compose_images` | Multiple references | `--refs` flag |
| `search_grounded_image` | Real-time data | `--grounded` flag, weather, stocks |

**Key distinction:** `edit_image` is stateless (single change), chat sessions are stateful (model remembers history). Use chat when user will likely request 2+ changes.

### State Tracking

Track in conversation context:
- Last generated image path
- Active session ID
- Current version number

**When in active session, display:** `**Session:** Active (ID: [id]) — say "done" to end`

## Session Persistence

Persist chat sessions to `.nanobananapro-session` (project root or current directory) to recover from disconnects.

### Session File Format

```json
{
  "session_id": "abc123",
  "started": "2026-01-22T10:30:00Z",
  "last_image": "outputs/exploration/wizard-v3.png",
  "iteration": 3,
  "last_prompt": "An elderly wizard with silver beard..."
}
```

### Lifecycle

- **Create/update** on `start_image_chat` and `continue_image_chat`
- **Delete** on `end_image_chat`, user says "done", or starts fresh

### Recovery

On skill startup, if session file exists, offer:
1. **Continue** — Check if session active via `list_chat_sessions`, use `continue_image_chat` or fall back to option 2
2. **Use last image** — Start new session with `last_image` as reference
3. **Start fresh** — Delete session file, proceed normally

### MCP Tool Reference

| Tool | Required | Optional |
|------|----------|----------|
| `generate_image` | `prompt` | `aspect_ratio`, `resolution`, `output_path`, `seed` |
| `edit_image` | `prompt`, `image_path` | `aspect_ratio`, `resolution`, `output_path`, `seed` |
| `compose_images` | `prompt`, `image_paths` (max 14) | `aspect_ratio`, `resolution`, `output_path`, `seed` |
| `search_grounded_image` | `prompt` | `aspect_ratio`, `resolution`, `output_path` |
| `start_image_chat` | `initial_prompt` | `seed` |
| `continue_image_chat` | `session_id`, `prompt` | `aspect_ratio`, `resolution` |
| `end_image_chat` | `session_id` | — |

**Defaults:** `model="pro"`, `aspect_ratio="1:1"`, `resolution="2K"`. Seed range: 0-2147483647.

## The 6-Element Formula

Every prompt should address: **Subject**, **Composition**, **Action**, **Location**, **Style**, **Constraints**.

See `/enhance-prompt` skill for detailed element definitions and examples.

### Gap Analysis

Mark each element: ✓ (specific), △ (vague), ✗ (missing). Focus enhancement on ✗ and △.

### Enhancement Output

Write as natural prose (2-4 sentences). Avoid keyword spam, comma lists, and generic quality words ("4k, masterpiece, trending").

## Process Steps

### Step 0: Intent Extraction

**Always ask first**, before any other processing:

> "What should the viewer feel when they see this image?"

This question surfaces emotional intent before diving into technical details. Store the response for use in:
- Enhancement (bias choices toward stated intent)
- Taste check (flag contradictions)
- Post-generation critique (evaluate against intent)

**Common responses and enhancement bias:**

| Intent | Enhancement Direction |
|--------|----------------------|
| "peaceful" | Soft light, muted colors, open space, horizontal lines |
| "tense" | High contrast, tight framing, diagonal lines, shadows |
| "nostalgic" | Warm tones, film grain, soft focus, golden hour |
| "energetic" | Saturated colors, dynamic angles, motion blur |
| "mysterious" | Low key lighting, partial reveals, fog/atmosphere |
| "intimate" | Close framing, shallow DOF, warm palette |
| "epic" | Wide angle, dramatic scale, strong verticals |

**If user skips or says "I don't know":**
- Proceed with gap analysis
- Infer intent from concept if possible
- Note that intent was not explicitly stated (affects critique step)

**Example:**

```
User: /image-prompt a lighthouse

Bot: What should the viewer feel when they see this image?

User: lonely but hopeful

[Proceeds to gap analysis, biasing toward: isolated subject,
cool tones with warm accent (lighthouse light), wide composition
with negative space, dusk/dawn timing]
```

### Step 1: Parse Input

Extract from the user's request:
- The core concept
- Any flags (--chat, --refs, --style, etc.)
- Explicit preferences mentioned

### Step 2: Check Project Context

Detect project context (see `/enhance-prompt` for shared detection logic):

**Priority:** `--project` flag > current directory > parent directory > no project

**Project markers:** `style-guide.md`, `style-library.md`, `outputs/`, `references/`

**Files to load:**
- `style-guide.md` — brand constraints, palette, requirements (if `locked: true`, show indicator and skip update suggestions)
- `style-library.md` — presets for `--style` flag (project overrides root)
- `references/` — suggest `--refs` if relevant
- `outputs/` — save location for generated images
- `asset-log.md` — log generation metadata

**Save location:** project `outputs/exploration/` > `--output` path > `./output/`

### Step 3: Gap Analysis

Apply 6-element check to user's concept:

```
User concept: "a wizard"

Subject:     △ "wizard" — needs age, appearance, clothing details
Composition: ✗ missing — needs shot type and angle
Action:      ✗ missing — what is the wizard doing?
Location:    ✗ missing — where is this scene?
Style:       ✗ missing — photo? illustration? painting?
Constraints: ✗ none specified
```

### Step 4: Clarify if Needed

If multiple critical elements are missing, ask 1-2 focused questions:

> "Quick questions to make this great:
> 1. What's the wizard doing? (casting spell / reading / walking)
> 2. What style? (realistic photo / fantasy illustration / painted)"

Only ask if truly ambiguous. If you can make reasonable creative choices, proceed.

### Step 5: Enhance Prompt

Transform the concept using the 6-element formula:

**Input:** "a wizard"

**Enhanced:**
"An elderly wizard with a long silver beard and weathered face, wearing deep blue robes embroidered with silver constellations. Standing at the edge of a cliff at twilight, arms raised as swirling magical energy gathers between his hands. Dramatic lighting from the magic illuminates his face from below. Fantasy illustration style with rich colors and painterly brushwork."

### Step 5b: Taste Check (unless --no-taste)

After enhancement, run taste analysis. See `/taste-check` skill for detailed pattern definitions.

**Checks:** Clichés (from `taste-check/taste-patterns.md`), specificity (>150 words warns), intent contradictions.

**Sensitivity (--taste flag):** low (egregious only), medium (default), high (strict).

**If issues found, show summary:**
```
## Taste Check
Found 2 clichés, prompt is 165 words.
- "epic lighting" → "Low sun backlighting with long shadows"
Fix these? [yes / skip / show details]
```

**Responses:** yes (apply fixes), skip (keep original), show details (explain issues, auto-enabled with `--learn`).

If no issues, proceed directly to Step 6.

### Step 6: Show for Approval

Present the enhanced prompt before generating:

```
## Enhanced Prompt

"[Your enhanced prompt here]"

**Settings:**
- Aspect ratio: [ratio]
- Resolution: [resolution]
- Style preset: [if applied]

Generate this image? (yes / adjust / change style)
```

### Step 7: Generate

Call the appropriate MCP tool with:
- The enhanced prompt
- Selected aspect ratio (infer from content or use flag)
- Resolution (from flag or default 2K)
- Output path (from flag or project structure)

### Step 8: Offer Iteration

After generation, offer quick adjustment options:

```
Image generated!

**Quick adjustments:**
- "warmer" / "cooler" — color temperature
- "brighter" / "darker" — exposure
- "closer" / "wider" — framing
- "more dramatic" / "softer" — contrast/mood

**Or describe changes:** "make the background blurrier"
**Or:** "critique" to reflect on this | "done" to finish
```

**Tool selection for iteration:**

| Current State | User Request | Action |
|---------------|--------------|--------|
| In chat session | Any change | `continue_image_chat` |
| Not in chat | Single edit ("add X", "change Y") | `edit_image` |
| Not in chat | First change requested | `edit_image` + suggest chat mode |
| Not in chat | Second+ change requested | Suggest starting chat session |

**After first edit (not in chat), add:**
> "Want to keep refining? I can start a chat session for smoother back-and-forth."

### Critique Mode

When user says "critique", run VTS-inspired 4-step reflection framework:

```
## Critique

**1. Description** — What's in the image?
[Brief factual description of what was generated]

**2. Analysis** — How do elements relate?
[Composition, color relationships, visual hierarchy]

**3. Interpretation** — What does it communicate?
[Mood, feeling, narrative the image conveys]

**4. Evaluation** — Does it match your intent?
Your stated intent was: "[their answer from Step 0]"

Does this image achieve that? (yes / partially / no)
```

**Follow-up Based on Response:**

| Response | Action |
|----------|--------|
| **yes** | "Great! Continue iterating or say 'done' to finish." |
| **partially** | "What's missing? I'll suggest targeted adjustments." |
| **no** | "What feels wrong? Let's identify the gap between intent and result." |

**With --learn Flag:**

Add brief explanations connecting observations to the 6-element formula and taste principles.

**If Intent Was Not Stated:**

Skip the evaluation step, or note: "You didn't specify an intent earlier — what were you hoping to achieve?"

### Step 9: Save and Log

If in a project with proper structure:

**Save location:**
- During iteration: `outputs/exploration/[name]-v[n].png`
- When user says "done" or "approved": move/copy to `outputs/finals/`

**Log to asset-log.md:**
```markdown
| 2026-01-21 | wizard-hero | Elderly wizard casting spell at twilight... | generate_image | approved | internal | outputs/finals/wizard-hero-v3.png |
```

**Approval column values:**
- `—` — No approval yet (exploration)
- `internal` — Team approved
- `client` — Client/external approved
- `[name]` — Specific approver name

When user says "approved" or "client approved", update both Status and Approval columns.

## Project Awareness Details

**style-guide.md:** Apply color palette, style requirements, brand voice, and "don't" rules to enhancement.

**style-library.md:** Load `--style` preset, suggest relevant presets, respond to "what styles do I have?"

**references/:** Suggest `--refs` if concept could benefit; use `compose_images` when `--refs` specified.

## Reference Calibration

When `references/` folder exists, automatically extract a taste profile from images.

### Extraction Process

Analyze reference images for: palette, lighting, composition, texture, mood. Cache results to `.nanobananapro-taste-cache.json`.

### Application

Use extracted profile as soft constraints during enhancement:
- **Flag contradictions:** "Your references are muted — 'vibrant saturated colors' may clash."
- **Suggest alignment:** "Consider 'desaturated earth tones' to match your reference palette."

### Cache Refresh

Re-extract when: files in `references/` change, cache older than 7 days, or `--recalibrate` flag used.

## Examples

### Basic Generation

```
User: /image-prompt a coffee shop

[Gap analysis: Subject △, Composition ✗, Action ✗, Location △, Style ✗]

## Enhanced Prompt

"A cozy independent coffee shop with exposed brick walls and mismatched vintage furniture. Morning light streaming through large storefront windows, casting warm golden patterns across worn wooden floors. A barista in a canvas apron steams milk behind a copper espresso machine. Medium shot at eye level. Film photography style with shallow depth of field and subtle grain."

**Settings:**
- Aspect ratio: 16:9 (scene composition)
- Resolution: 2K

Generate this image?
```

### With Style Preset

```
User: /image-prompt a portrait of a musician --style=cinematic

[Loads "cinematic" from style-library.md: "Cinematic lighting, anamorphic lens flare, film grain, dramatic shadows"]

## Enhanced Prompt

"A jazz saxophonist in a smoky club, eyes closed in concentration, fingers poised on brass keys worn smooth from years of play. Dramatic side lighting catches the curve of the instrument and the musician's weathered hands. Cinematic lighting with anamorphic lens flare, subtle film grain, dramatic shadows falling across the scene. Close-up portrait, shallow depth of field."

**Settings:**
- Aspect ratio: 2.39:1 (cinematic)
- Resolution: 2K
- Style: cinematic

Generate this image?
```

### With Chat for Iteration

```
User: /image-prompt a fantasy landscape --chat

[Starts chat session for iteration]

## Enhanced Prompt

"A vast fantasy kingdom viewed from a mountain pass, with crystalline spires rising from a valley shrouded in morning mist. Waterfalls cascade from floating islands, catching rainbow light. Ancient stone bridges connect impossible peaks. Epic fantasy illustration style with rich saturated colors and intricate detail."

**Settings:**
- Aspect ratio: 21:9 (panoramic)
- Resolution: 2K
- Mode: Chat session (iterative)

Generate this image?

---

[After generation]

Image generated! Session active for refinement.

Quick adjustments: warmer, cooler, brighter, darker, closer, wider
Or describe: "add a dragon in the distance"
Or: "done" to end session
```

### With References

```
User: /image-prompt character portrait --refs=./references/characters/

[Detects reference images, will use compose_images]

Found 3 reference images in ./references/characters/
- hero-sketch.png
- color-palette.jpg
- pose-reference.png

## Enhanced Prompt

"Character portrait maintaining the design from references: [subject details inferred from refs]. Three-quarter view, dramatic lighting from upper left. Digital painting style with clean lines and vibrant colors matching the reference palette."

**Settings:**
- Aspect ratio: 3:4 (portrait)
- Resolution: 2K
- References: 3 images
- Tool: compose_images

Generate this image?
```

### Search-Grounded

```
User: /image-prompt today's weather in Tokyo visualized --grounded

[Uses search_grounded_image for real-time data]

## Enhanced Prompt

"Visualization of current weather conditions in Tokyo, Japan. [Real-time weather data will be incorporated]. Stylized infographic illustration showing temperature, conditions, and atmosphere over the Tokyo skyline. Clean modern design with weather iconography."

**Settings:**
- Aspect ratio: 16:9
- Resolution: 2K
- Tool: search_grounded_image (real-time data)

Generate this image?
```

### With Taste Layer

```
User: /image-prompt a wizard

Bot: What should the viewer feel when they see this image?

User: mysterious and powerful

[Gap analysis: Subject △, Composition ✗, Action ✗, Location ✗, Style ✗]

[Enhancement biased toward mysterious/powerful: low-key lighting,
strong verticals, deep shadows, hints of hidden knowledge]

## Taste Check

Found 0 clichés, prompt is 87 words (good).

No issues detected. Proceeding to approval.

## Enhanced Prompt

"An ancient wizard stands at the threshold of a dark stone chamber,
staff raised with arcane symbols glowing faintly along its length.
Deep hood shadows most of his face, but his eyes gleam with inner light.
Stone pillars frame him in stark verticals. Low-key lighting with a single
source from below, casting dramatic upward shadows. Fantasy illustration
style with muted colors except for the magical glow."

**Settings:**
- Aspect ratio: 3:4 (portrait)
- Resolution: 2K

Generate this image? (yes / adjust / change style)

User: yes

[Generates image]

Image generated!

**Quick adjustments:** warmer, cooler, brighter, darker, closer, wider
**Or describe changes:** "make the background blurrier"
**Or:** "critique" to reflect on this | "done" to finish

User: critique

## Critique

**1. Description** — The image shows an elderly robed figure in a dark
stone chamber, holding a glowing staff, with dramatic upward lighting.

**2. Analysis** — Strong vertical composition from the pillars and staff.
Color palette is muted grays and blues with warm accent from the magical
glow. Visual hierarchy draws eye to the glowing staff, then to the
partially hidden face.

**3. Interpretation** — Conveys age, hidden knowledge, and restrained
power. The obscured face suggests secrets, while the controlled magical
glow implies mastery rather than chaos.

**4. Evaluation** — Your stated intent was: "mysterious and powerful"

Does this image achieve that? (yes / partially / no)

User: yes

Great! Continue iterating or say "done" to finish.

User: done
```

## Aspect Ratio Guidelines

Infer appropriate ratio from content:

| Content Type | Suggested Ratio |
|--------------|-----------------|
| Portrait, character | 3:4 or 4:5 |
| Landscape, scene | 16:9 or 21:9 |
| Square, icon, avatar | 1:1 |
| Social media story | 9:16 |
| Cinematic | 2.39:1 or 21:9 |
| Product shot | 1:1 or 4:3 |

User's explicit `--aspect` flag always overrides inference.

## Error Handling

| Situation | Response |
|-----------|----------|
| Generation fails | Show error, suggest prompt adjustments, offer retry |
| Style preset not found | List available presets, suggest similar |
| References not found | Confirm path, fall back to generate_image |
| Chat session lost | Check for `.nanobananapro-session`, offer recovery options |
| Unclear concept | Ask 1-2 clarifying questions before proceeding |
