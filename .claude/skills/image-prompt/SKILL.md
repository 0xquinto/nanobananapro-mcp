---
name: image-prompt
description: Full image generation workflow from rough concept to final image.
  Use when user wants to generate an image, create visuals, or says "make me
  an image of...". Enhances prompts, selects appropriate MCP tool, handles
  iteration. The primary skill for image creation.
argument-hint: "your image idea" [--chat] [--refs=path] [--style=preset] [--dry-run] [--format=json]
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

| Flag | Usage | Description |
|------|-------|-------------|
| `--chat` | `--chat` | Use multi-turn session for iterative refinement |
| `--refs=<path>` | `--refs=./references/` | Include reference images for composition |
| `--style=<preset>` | `--style=cinematic` | Apply preset from style-library.md |
| `--output=<path>` | `--output=./hero.png` | Save to specific location |
| `--resolution=<res>` | `--resolution=4K` | Set output resolution (1K, 2K, 4K) |
| `--aspect=<ratio>` | `--aspect=16:9` | Set aspect ratio |
| `--grounded` | `--grounded` | Use search-grounded generation for real-world data |
| `--project=<path>` | `--project=demo-campaign` | Use specific project's context (style-guide, style-library, outputs) |
| `--taste=<level>` | `--taste=high` | Cliche detection sensitivity (low/medium/high, default: medium) |
| `--learn` | `--learn` | Show reasoning for taste suggestions |
| `--no-taste` | `--no-taste` | Skip taste checks entirely (speed mode) |
| `--dry-run` | `--dry-run` | Preview enhanced prompt and settings without generating |
| `--format=<fmt>` | `--format=json` | Output format: human (default), json |

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

## MCP Tool Selection

### Decision Tree

```
Is there an existing image to work with?
├── NO → Fresh generation
│   ├── Has --refs flag? → compose_images
│   ├── Has --grounded flag? → search_grounded_image
│   ├── Has --chat flag? → start_image_chat
│   └── Default → generate_image
│
└── YES → Modifying existing image
    ├── Already in active chat session? → continue_image_chat
    ├── User expects multiple rounds of refinement? → start_image_chat (with image context)
    └── Single specific edit? → edit_image
```

### When to Use Each Tool

| Tool | Use When | Key Indicator |
|------|----------|---------------|
| `generate_image` | Fresh image, no iteration expected | One-shot request, user seems satisfied with single output |
| `edit_image` | **Single specific change** to existing image | "make it bluer", "remove the background", "add a hat" — discrete modification |
| `start_image_chat` | User wants to **explore and iterate** | `--chat` flag, OR phrases like "let's try", "I want to refine", "help me get this right" |
| `continue_image_chat` | **Already in active session**, user requests changes | Session ID exists from previous `start_image_chat` |
| `compose_images` | Combining/referencing multiple images | `--refs` flag, user provides reference images |
| `search_grounded_image` | Needs real-world current data | `--grounded` flag, weather, stocks, current events |

### Chat Session vs Edit Image — The Key Distinction

| Aspect | `edit_image` | Chat Session |
|--------|--------------|--------------|
| **Context** | Stateless — each edit is independent | Stateful — model remembers previous iterations |
| **Use case** | "Change X to Y" (single modification) | "Let's explore variations" (creative iteration) |
| **Rounds** | One | Multiple back-and-forth |
| **When to choose** | User knows exactly what they want changed | User is experimenting/refining |

**Rule of thumb:**
- If user will likely ask for 2+ changes → start a chat session
- If user has one specific edit → use edit_image

### Auto-Suggest Chat Mode

When the user requests changes after initial generation (without `--chat`), suggest upgrading:

> "Want to continue refining? I can start a chat session for faster iteration, or make this single edit."

### State Tracking

Claude Code maintains conversation context. Use that context to remember:
- Last generated image path (for `edit_image`)
- Active session ID (for `continue_image_chat`)
- Current version number (for file naming)

**Required state for each tool:**

| Tool | Required State |
|------|----------------|
| `edit_image` | Path to existing image |
| `continue_image_chat` | Session ID from `start_image_chat` |
| `end_image_chat` | Session ID |

**Persistence:** Active session state is also saved to `.nanobananapro-session` for recovery. See [Session Persistence](#session-persistence).

**When in an active chat session, always display:**
```
**Session:** Active (ID: [id]) — say "done" to end
```

This reminds the user (and future context) that a session is open.

## Session Persistence

Chat sessions can be lost if Claude Code disconnects. To prevent work loss:

### Session File

When a chat session starts, create `.nanobananapro-session` in the project root (or current directory):

```json
{
  "session_id": "abc123",
  "started": "2026-01-22T10:30:00Z",
  "last_image": "outputs/exploration/wizard-v3.png",
  "iteration": 3,
  "last_prompt": "An elderly wizard with silver beard..."
}
```

### Session Lifecycle

| Event | Action |
|-------|--------|
| `start_image_chat` called | Create/update `.nanobananapro-session` |
| `continue_image_chat` called | Update `last_image`, increment `iteration`, update `last_prompt` |
| `end_image_chat` called | Delete `.nanobananapro-session` |
| User says "done" | Delete `.nanobananapro-session` |

### Session Recovery

On startup of `/image-prompt`, check for `.nanobananapro-session`:

**If session file exists:**

```
Found a previous session from [timestamp].
Last image: [last_image]
Iteration: [iteration]

Options:
1. Continue where you left off (describe your next change)
2. Start fresh with the last image as reference
3. Start completely fresh
```

**Recovery logic:**

| User Choice | Action |
|-------------|--------|
| Continue | Try `list_chat_sessions` to check if session still active. If yes, use `continue_image_chat`. If no, use option 2. |
| Start with last image | Use `start_image_chat` with `last_image` as context, delete old session file |
| Start fresh | Delete session file, proceed normally |

### Session File Location

| Context | Location |
|---------|----------|
| In project directory | `[project]/.nanobananapro-session` |
| No project | `./.nanobananapro-session` (current directory) |

### Cleanup

The session file should be deleted:
- When user explicitly ends session ("done")
- When `end_image_chat` is called
- When user chooses "start fresh" during recovery
- When a new session starts (after prompting about existing)

### MCP Tool Signatures

```python
# One-shot generation
generate_image(
    prompt: str,
    model: str = "pro",           # Always use "pro"
    aspect_ratio: str = "1:1",    # 1:1, 16:9, 9:16, 4:3, 3:4, 21:9
    resolution: str = "2K",       # 1K, 2K, 4K
    output_path: str = None       # Optional save path
)

# Multi-turn chat session
start_image_chat(
    initial_prompt: str,
    model: str = "pro"
)
# Returns: session_id

continue_image_chat(
    session_id: str,
    prompt: str,
    aspect_ratio: str = None,
    resolution: str = None
)

end_image_chat(session_id: str)

# Composition from references
compose_images(
    prompt: str,
    image_paths: list[str],       # Up to 14 reference images
    model: str = "pro",
    aspect_ratio: str = "1:1",
    resolution: str = "2K",
    output_path: str = None
)

# Edit existing image
edit_image(
    prompt: str,                  # Editing instructions
    image_path: str,              # Image to edit
    model: str = "pro",
    aspect_ratio: str = None,     # Optional, defaults to input
    resolution: str = "2K",
    output_path: str = None
)

# Search-grounded (real-world data)
search_grounded_image(
    prompt: str,                  # Include real-time data needs
    aspect_ratio: str = "16:9",
    resolution: str = "2K",
    output_path: str = None
)
```

## The 6-Element Formula (Embedded)

Every effective prompt addresses these elements:

| Element | What it defines | Enhancement approach |
|---------|-----------------|---------------------|
| **Subject** | Who/what is the main focus | Add specifics: breed, age, material, condition, distinguishing features |
| **Composition** | How the frame is arranged | Add shot type (close-up, wide) and angle (eye level, low, high) |
| **Action** | What's happening | Add movement, interaction, or dynamic state |
| **Location** | Where it takes place | Add environment, setting, atmosphere, time of day |
| **Style** | Visual treatment | Add medium, art style, lighting quality, color treatment |
| **Constraints** | Text, ratio, requirements | Add any specific requirements, aspect ratio implications |

### Gap Analysis

Before enhancing, quickly assess what's present:

- ✓ Present and specific
- △ Present but vague
- ✗ Missing entirely

Focus enhancement on ✗ and △ elements. Don't over-elaborate ✓ elements.

### Enhancement Output

Write as natural flowing prose, 2-4 sentences. Group related elements. Never use:
- Keyword spam ("4k, masterpiece, trending")
- Comma-separated lists
- Generic quality words

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

This skill is project-aware and determines context based on detection priority:

#### Detection Priority

1. **`--project=<path>` flag** → Use that project's files
2. **Current directory has project markers** → Use current project
3. **Parent directory has project markers** → Use parent project
4. **No project context** → Use root `style-library.md` only, save to `./output/`

#### Project Markers

A directory is considered a "project" if it contains ANY of:
- `style-guide.md`
- `style-library.md`
- `outputs/` directory
- `references/` directory

#### Style Library Resolution

When `--style=<preset>` is specified:
1. First check **project** `style-library.md` (if in project)
2. Then check **root** `style-library.md`
3. Project presets override root presets of the same name

#### Files to Check

| File | If found | Action |
|------|----------|--------|
| `style-guide.md` | Read for brand constraints, color palette, style requirements |
| `style-library.md` | Load available presets, check if `--style` preset exists |
| `references/` | Note available reference images, suggest `--refs` if relevant |
| `outputs/` | Plan to save there (exploration/ for WIP, finals/ for approved) |
| `asset-log.md` | Plan to log generation metadata |

#### Save Location Logic

| Context | Save To |
|---------|---------|
| In project with `outputs/` | `[project]/outputs/exploration/` |
| In project, no `outputs/` | Create `[project]/outputs/exploration/` |
| No project, `--output` flag | Use specified path |
| No project, no flag | `./output/` in current directory |

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

After enhancement, before showing the prompt, run taste analysis.

**What Gets Checked:**

| Check | Trigger | Response |
|-------|---------|----------|
| **Cliché detection** | Matches patterns in `.claude/taste-patterns.md` | Suggest concrete replacement |
| **Specificity score** | Prompt > 150 words OR > 3 modifiers per element | Warn about over-specification |
| **Intent contradiction** | Enhancement conflicts with stated intent | Flag the mismatch |

**Sensitivity Levels (via --taste flag):**

| Level | What's Flagged |
|-------|----------------|
| **Low** | Only egregious patterns (ArtStation spam, 8K quality spam) |
| **Medium** (default) | Common clichés + mild specificity warnings |
| **High** | Any generic tendency + strict specificity limits |

**If Issues Found:**

Show a summary block before proceeding:

```
## Taste Check

Found 2 clichés, prompt is 165 words (approaching over-specified).

**Clichés:**
- "epic lighting" → "Low sun backlighting with long shadows"
- "trending on ArtStation" → Remove (causes token collisions)

**Specificity:** Consider leaving composition or atmosphere more ambiguous.

Fix these? [yes / skip / show details]
```

**User Responses:**
- **yes** — Apply suggestions automatically, proceed to approval
- **skip** — Proceed with original enhancement unchanged
- **show details** — Explain why each pattern is problematic (auto-enabled with `--learn`)

**With --learn Flag:**

After each cliché, show explanation:
> **Why this matters:** "Epic lighting" is vague — the model defaults to its most common interpretation. Specifying angle, quality, and source gives intentional results.

**If No Issues:**

Proceed directly to Step 6 without interruption.

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

### When style-guide.md Exists

Read and apply:
- Color palette restrictions
- Style requirements
- Brand voice indicators
- Any "don't" rules

Example integration:
```
User: "a hero banner for the website"

[Reads style-guide.md, finds: warm earth tones, photography style, cozy mood]

Enhanced prompt includes: "...warm earth tone palette with terracotta and sage accents, photography style, inviting and cozy atmosphere..."
```

### When style-library.md Exists

- If `--style=<preset>` specified, load and append that preset
- If no style specified but relevant preset exists, suggest it
- Show available presets if user asks "what styles do I have?"

### When references/ Has Images

- If user's concept could benefit from reference images, suggest:
  > "I see reference images in `references/`. Would you like to use them for style consistency? (Use `--refs=references/`)"
- If `--refs` specified, use `compose_images` instead of `generate_image`

## Reference Calibration

When the project has a `references/` folder with images, automatically extract a taste profile.

### Automatic Extraction

1. Scan `references/` for image files
2. Analyze each for taste signals (palette, lighting, composition, texture, mood)
3. Extract commonalities into a taste profile
4. Cache to `.nanobananapro-taste-cache.json`

### What Gets Extracted

| Signal | Example Output |
|--------|----------------|
| **Dominant palette** | "Muted earth tones, desaturated greens" |
| **Lighting tendency** | "Soft diffused light, minimal harsh shadows" |
| **Composition patterns** | "Centered subjects, generous negative space" |
| **Texture/finish** | "Film grain, organic imperfections" |
| **Mood consistency** | "Contemplative, quiet, intimate" |

### How It's Applied

During enhancement, the extracted profile acts as soft constraints:

- **Flag contradictions:** "Your references are muted — 'vibrant saturated colors' may clash with your established aesthetic."
- **Suggest alignment:** "Consider 'desaturated earth tones' to match your reference palette."

### Cache Storage

Cache extracted profile to `.nanobananapro-taste-cache.json` in project root:

```json
{
  "extracted_from": ["ref1.jpg", "ref2.jpg", "ref3.jpg"],
  "last_updated": "2026-01-23T10:30:00Z",
  "profile": {
    "palette": "muted earth tones, desaturated",
    "lighting": "soft diffused, minimal shadows",
    "composition": "centered subjects, negative space",
    "texture": "film grain, organic",
    "mood": "contemplative, quiet"
  }
}
```

### Re-extraction Triggers

Re-extract automatically if:
- Files in `references/` change (add/remove/modify)
- Cache is older than 7 days
- User runs with `--recalibrate` flag

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
