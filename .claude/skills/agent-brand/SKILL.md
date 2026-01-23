---
name: agent-brand
description: Guided brand identity agent that orchestrates multi-step visual branding projects through research, exploration, and generation. Uses Task tool workers to research style directions, craft prompts, and generate images. Employs guided collaboration where the agent proposes options and users make decisions.
argument-hint: "brand description" | --resume
---

# Agent: Brand Identity

Orchestrates complex brand identity projects through guided collaboration. This agent researches style directions, proposes visual options, and coordinates image generation workers - but never generates images directly. All generation is delegated to specialized Task tool workers.

## How to Use

**Starting a new project:**
```
/agent brand "description of your brand"
```

**Resuming a previous session:**
```
/agent brand --resume
```

**Navigation during the session:**
Once the skill is active, you interact naturally with the agent. The agent maintains state across messages in the same conversation. You can use navigation commands at any time:
- `/agent show` - Redisplay current options
- `/agent back` - Return to previous phase and re-select

**Example:**
```
User: /agent brand "artisan coffee shop"
Agent: [Presents style directions]
User: I like option 2
Agent: [Proceeds with your selection]
```

The skill maintains context throughout the conversation, so you can refine choices and ask questions naturally.

## How This Skill Works

This skill runs in Claude Code. When invoked with `/agent brand "description"`, Claude reads this file and follows the "Process Steps" instructions exactly. The skill:

1. **Orchestrates, doesn't generate** - Never generates images directly. All generation is delegated to Task tool workers.
2. **Uses Task tool** - Spawns research workers with specific prompts to gather information.
3. **Maintains state** - Saves decisions to `.claude/local/agent-state.json` for checkpoints and resume functionality.
4. **Guided collaboration** - Proposes options to the user and executes their choices.

**Important:** The Process Steps section below is the actual implementation. Follow it exactly when the skill is invoked.

## Critical Requirements

When executing this skill:

**MUST DO:**
- ✓ Spawn Task tool workers for research (never do research directly)
- ✓ Use exact Task tool syntax: `Task(description="...", subagent_type="general-purpose", model="sonnet", prompt="...")`
- ✓ Save state to `.claude/local/agent-state.json` after user selects direction (Phase 1a) and palette (Phase 1b)
- ✓ Parse worker output to extract all 3 options with complete information (Phase 1a: directions, Phase 1b: palettes)
- ✓ Present options in the format specified in Process Steps
- ✓ Handle all user selection types (1/2/3/custom/refinement)
- ✓ After Phase 1a completes, automatically proceed to Phase 1b
- ✓ Load state with Read tool before updating in Phase 1b

**MUST NOT:**
- ✗ Generate images directly (workers do that)
- ✗ Skip spawning the research worker
- ✗ Present options without spawning worker first
- ✗ Forget to save state after selection

## Workflow Overview

```
User invokes: /agent brand "artisan coffee shop"
    ↓
★ Invoke project-setup (new projects only)
    ↓
Phase 1a: Style Direction
    ↓
Spawn Research Worker (Task tool)
    ↓
Present 3 Style Directions
    ↓
User Selects Direction
    ↓
Phase 1b: Color Palette
    ↓
Spawn Palette Worker (Task tool)
    ↓
Present 3 Palette Options
    ↓
User Selects Palette
    ↓
★ Save palette to style-library
    ↓
Phase 1c: Logo Concepts
    ↓
Spawn Logo Concept Worker (Task tool)
    ↓
For Each Concept:
    ├── ★ Invoke enhance-prompt
    ├── ★ Run taste-check
    └── Spawn Logo Generation Worker (Task tool)
    ↓
Present 3 Logo Images
    ↓
User Selects Logo
    ↓
Complete
```

★ = Skill invocation (chains to local skills)

## Architecture Principles

**Worker Model:**
- Orchestrator (this skill) never generates images directly
- All image work delegated to Task tool workers with specific prompts
- Workers cannot spawn sub-workers (flat hierarchy only)
- Workers return natural language outputs; orchestrator parses them

**Guided Collaboration:**
- Agent proposes options based on research
- User decides which direction to pursue
- Agent executes the user's choice
- Clear checkpoints at each phase

**Conversation State:**
- All user interaction flows through the skill only
- Workers receive context via their prompt
- Orchestrator maintains phase state and decisions

## Navigation Commands

These commands control the agent's workflow. Some are documented but not fully implemented yet:

| Command | Status | Description |
|---------|--------|-------------|
| `/agent brand "X"` | ✓ Active | Start new brand identity project |
| `/agent brand --resume` | ✓ Active | Resume from saved state file |
| `/agent show` | ✓ Active | Redisplay current options at this phase |
| `/agent back` | ✓ Active | Return to previous checkpoint, allow re-selection |
| `/agent tweak "X"` | 📋 Planned | Refine current options with feedback |
| `/agent status` | 📋 Planned | Show current phase and all decisions made |
| `/agent help` | 📋 Planned | List available commands and current context |

**Legend:**
- ✓ Active - Fully implemented
- 📋 Planned - Documented but not implemented

## Phase 1a: Style Direction (ACTIVE)

### Process Steps

When the skill is invoked with `/agent brand "description"`, follow these steps exactly:

**Quick Reference:**
0. First-run onboarding (if new session)
1. Parse brand description and check for `--resume` flag
2. Spawn Task tool research worker with brand description
3. Parse worker output into 3 style directions
4. Present options to user in formatted list
5. Handle user selection (1/2/3/custom/refinement)
6. Save state to `.claude/local/agent-state.json`

**Detailed Steps:**

#### Step -1: Invoke Brainstorming Skill (New Projects Only)

**For new brand identity projects** (not `--resume`), invoke the brainstorming skill to explore the brand concept before generating style directions.

**Use the Skill tool:**
```
Skill(skill="superpowers:brainstorming")
```

Follow the brainstorming skill's process to explore:
- What the brand represents
- Target audience and their aesthetic expectations
- Competitive landscape considerations
- Key differentiators to express visually

After brainstorming completes, proceed to Step 0.

**Skip condition:** When `--resume` is used, skip directly to Step 1b (Resume Flow).

#### Step 0: First-Run Onboarding (if new session)

**Use the Read tool** to check for `.claude/local/agent-state.json`:

**If state file doesn't exist (Read returns error) AND user didn't use --resume:**

Show the welcome message:

```
Welcome to the Brand Identity Agent!

I'll guide you through creating a complete brand identity in 3 phases:

1. **Style Direction** - We'll explore 3 visual style options
2. **Color Palette** - I'll create 3 palette variations for your chosen style
3. **Logo Concepts** - You'll see 3 generated logo designs

At each phase, you decide which direction to pursue. You can use:
- `/agent show` - Redisplay current options
- `/agent back` - Return to previous phase and re-select

Let's begin.
```

Then proceed to Step 1.

**If state file exists (Read succeeds):**
Skip this welcome message (user has seen it before).

#### Step 1: Parse and Acknowledge

Extract from the user's invocation:
- The brand description
- The `--resume` flag (if present)

If `--resume` is present, skip to Step 1b (Resume Flow).

Otherwise, acknowledge the request:

```
I'll help create a brand identity for [their brand]. Let me research some style directions.
```

#### Step 1b: Resume Flow (if --resume flag)

**Use the Read tool** to check for `.claude/local/agent-state.json`:

**If state file exists (Read succeeds):**
1. Parse the JSON content returned by Read
2. Extract `current_phase` and `decisions`
3. Present resume options:

```
Found previous brand identity session from [timestamp].

**Brand:** [brand_description]
**Last Phase:** [current_phase] ([decisions made])

Continue from [next phase]? (yes / start fresh)
```

**If state file doesn't exist (Read returns error):**
```
No previous session found. Starting fresh.
```

Then proceed to Step 2.

#### Step 2: Spawn Research Worker

Use the Task tool to spawn a research worker with the Research Worker Prompt Template (see below).

**Tool invocation:**
```
Task(
  description="Research brand style directions",
  subagent_type="general-purpose",
  model="sonnet",
  prompt="""You are a style research specialist. Research 3 distinct visual style directions for this brand:

Brand: [insert user's brand description here]

For each direction, provide:
1. Name (2-3 words)
2. Visual characteristics (colors, typography, graphic elements)
3. Mood/emotion it conveys
4. Why it fits this brand

Make the 3 directions meaningfully different - cover a range of aesthetics.

IMPORTANT: You are a research worker. Do NOT:
- Generate images (no MCP image tools)
- Spawn other workers (no Task tools)
- Interact with the user directly

Return your findings as natural language that the orchestrator will parse and present."""
)
```

Wait for the worker to return its findings.

#### Step 3: Parse Worker Output

The worker returns natural language. Extract:
- 3 direction names
- Visual characteristics for each
- Mood/emotion for each
- Why each fits the brand

**Validation:**
- Did the worker provide all 3 directions?
- Does each direction have all 4 required elements?

**If incomplete:**
- Re-spawn worker with clarified prompt (max 2 retries)
- If still incomplete after 2 retries, inform user and offer manual input

#### Step 4: Present Options

Format the parsed results clearly:

```
Based on [brand description] aesthetics, here are 3 style directions:

1. **[Direction 1 Name]**
   [Visual characteristics in 1-2 sentences]
   [Mood/emotion]

2. **[Direction 2 Name]**
   [Visual characteristics in 1-2 sentences]
   [Mood/emotion]

3. **[Direction 3 Name]**
   [Visual characteristics in 1-2 sentences]
   [Mood/emotion]

Which direction resonates? (1, 2, 3, or describe something different)
```

#### Step 5: Handle User Selection

Wait for user response.

**If user selects 1, 2, or 3:**
- Confirm selection:
  ```
  Perfect! [Direction Name] direction selected.

  ✓ Phase 1a complete: Style direction chosen

  Moving to Phase 1b: Color Palette generation
  ```
- Proceed to Step 6 (Save State)

**If user describes something different:**
- Parse their custom direction
- Confirm understanding:
  ```
  So you'd like a [their custom direction] style. Let me capture that.
  ```
- Proceed to Step 6 (Save State)

**If user asks for refinement ("I like 1 but can it be..."):**
- Spawn modified research worker with the refinement request
- Present the adjusted direction
- Ask for confirmation
- Proceed to Step 6 when confirmed

#### Step 6: Save State (Checkpoint)

**Use the Bash tool** to create `.claude/local/` directory if it doesn't exist:
```bash
mkdir -p .claude/local
```

**Use the Write tool** to save state to `.claude/local/agent-state.json`:

```json
{
  "brand_description": "[user's brand description]",
  "started": "[ISO 8601 timestamp]",
  "current_phase": "1a_complete",
  "first_run_complete": true,
  "decisions": {
    "style_direction": {
      "name": "[Selected Direction Name]",
      "characteristics": "[Visual characteristics]",
      "mood": "[Mood/emotion]",
      "selected_at": "[ISO 8601 timestamp]"
    }
  },
  "worker_outputs": {
    "style_research": "[Full worker output]"
  }
}
```

**State saved. Phase 1a complete. Proceed to Phase 1b.**

### Example Interaction

```
User: /agent brand "artisan coffee shop"

Agent: I'll help create a brand identity for your artisan coffee shop.
       Let me research some style directions.

       [Spawns research Task tool worker]

Agent: Based on artisan coffee shop aesthetics, here are 3 style directions:

       1. **Rustic Craftsman**
          Warm browns and burnt orange, hand-drawn illustrations,
          vintage serif typography. Evokes warmth, tradition, handmade quality.

       2. **Modern Minimal**
          Clean lines, muted earth tones (beige, sage, charcoal),
          geometric shapes, sans-serif fonts. Conveys sophistication,
          clarity, contemporary craft.

       3. **Botanical Organic**
          Forest greens and natural creams, botanical illustrations,
          organic textures, script accents. Suggests freshness,
          sustainability, connection to nature.

       Which direction resonates? (1, 2, 3, or describe something different)

User: 2

Agent: Perfect! Modern Minimal direction selected.

       ✓ Phase 1a complete: Style direction chosen

       Moving to Phase 1b: Color Palette generation

       [Saves state and proceeds to Phase 1b]
```

## Phase 1b: Color Palette (ACTIVE)

This phase generates color palette options based on the selected style direction from Phase 1a.

### Process Steps

When Phase 1a is complete and state is saved, automatically proceed to Phase 1b:

**Quick Reference:**
7. Transition from Phase 1a (confirm style direction selected)
8. Spawn Palette Worker (Task tool)
9. Parse worker output into 3 palette options
10. Present palettes to user with hex codes
11. Handle user selection and save state

**Detailed Steps:**

#### Step 7: Transition from Phase 1a

After Step 6 (Save State) in Phase 1a completes, immediately transition to Phase 1b.

Announce the transition:
```
Now let's develop color palettes that match the [Selected Direction Name] style.
```

**Validation before proceeding:**
- Confirm `decisions.style_direction` exists in state
- Extract `style_direction.name` and `style_direction.characteristics` for the worker prompt

#### Step 8: Spawn Palette Worker

Use the Task tool to spawn a palette research worker with the Palette Worker Prompt Template (see below).

**Tool invocation:**
```
Task(
  description="Generate color palette options",
  subagent_type="general-purpose",
  model="sonnet",
  prompt="""You are a color palette specialist. Create 3 color palette variations for this brand, within the selected style direction:

Brand: [insert brand_description from state]
Style Direction: [insert style_direction.name and characteristics from state]

For each palette provide:
1. Palette name (2-3 words, descriptive)
2. 5-6 colors with hex codes (e.g., #F5F5DC)
3. Usage notes for each color (primary, accent, neutral, background, text, etc.)
4. Why this palette works for the brand and style

Make the 3 palettes distinct but all aligned with the style direction. Each palette should offer a different mood or application approach within the chosen aesthetic.

IMPORTANT: You are a research worker. Do NOT:
- Generate images (no MCP image tools)
- Spawn other workers (no Task tools)
- Interact with the user directly

Return your findings as natural language that the orchestrator will parse and present."""
)
```

Wait for the worker to return its findings.

#### Step 9: Parse Worker Output

The worker returns natural language. Extract for each of the 3 palettes:
- Palette name
- 5-6 colors with hex codes
- Usage notes for each color
- Rationale (why it works)

**Validation:**
- Did the worker provide all 3 palettes?
- Does each palette have a name, colors with hex codes, usage notes, and rationale?
- Are hex codes in valid format (#RRGGBB)?

**If incomplete:**
- Re-spawn worker with clarified prompt emphasizing missing elements (max 2 retries)
- If still incomplete after 2 retries, inform user and offer manual input

#### Step 10: Present Palette Options

Format the parsed results clearly:

```
Here are 3 color palettes for the [Style Direction Name] style:

1. **[Palette 1 Name]**
   Colors:
   • [Color 1 name/usage]: #HEXCODE
   • [Color 2 name/usage]: #HEXCODE
   • [Color 3 name/usage]: #HEXCODE
   • [Color 4 name/usage]: #HEXCODE
   • [Color 5 name/usage]: #HEXCODE
   [Rationale in 1-2 sentences]

2. **[Palette 2 Name]**
   Colors:
   • [Color 1 name/usage]: #HEXCODE
   • [Color 2 name/usage]: #HEXCODE
   • [Color 3 name/usage]: #HEXCODE
   • [Color 4 name/usage]: #HEXCODE
   • [Color 5 name/usage]: #HEXCODE
   [Rationale in 1-2 sentences]

3. **[Palette 3 Name]**
   Colors:
   • [Color 1 name/usage]: #HEXCODE
   • [Color 2 name/usage]: #HEXCODE
   • [Color 3 name/usage]: #HEXCODE
   • [Color 4 name/usage]: #HEXCODE
   • [Color 5 name/usage]: #HEXCODE
   [Rationale in 1-2 sentences]

Which palette resonates? (1, 2, 3, or describe modifications)
```

#### Step 11: Handle User Selection and Save State

Wait for user response.

**If user selects 1, 2, or 3:**
- Confirm selection:
  ```
  Excellent! [Palette Name] selected.

  ✓ Phase 1b complete: Color palette chosen

  Moving to Phase 1c: Logo Concepts generation
  ```
- Proceed to save state (see State Save below)
- Then proceed to Phase 1c (Step 12)

**If user describes modifications:**
- Parse their requested changes
- Confirm understanding:
  ```
  I'll adjust [Palette Name] with [their modifications].
  ```
- Spawn modified palette worker with the refinement request
- Present the adjusted palette
- Ask for confirmation
- Proceed to save state when confirmed

**If user is unclear:**
- Ask for clarification:
  ```
  Did you mean palette [N]? Or would you like to adjust one of them?

  You can:
  - Choose 1, 2, or 3
  - Ask to modify a palette ("I like 1 but make the accent warmer")
  - Describe different colors you prefer
  ```

**State Save:**

**Use the Read tool** to load current state from `.claude/local/agent-state.json`:
- This should succeed since Phase 1a saved the state

Parse the JSON and update:
- Set `current_phase` to `"1b_complete"`
- Add palette selection to `decisions.color_palette`
- Add palette worker output to `worker_outputs.palette_research`

**Use the Write tool** to save updated state:

```json
{
  "brand_description": "[user's brand description]",
  "started": "[ISO 8601 timestamp from Phase 1a]",
  "current_phase": "1b_complete",
  "decisions": {
    "style_direction": {
      "name": "[Selected Direction Name]",
      "characteristics": "[Visual characteristics]",
      "mood": "[Mood/emotion]",
      "selected_at": "[ISO 8601 timestamp]"
    },
    "color_palette": {
      "name": "[Selected Palette Name]",
      "colors": [
        {"name": "[Color 1 usage]", "hex": "#HEXCODE"},
        {"name": "[Color 2 usage]", "hex": "#HEXCODE"},
        {"name": "[Color 3 usage]", "hex": "#HEXCODE"},
        {"name": "[Color 4 usage]", "hex": "#HEXCODE"},
        {"name": "[Color 5 usage]", "hex": "#HEXCODE"}
      ],
      "rationale": "[Why this palette works]",
      "selected_at": "[ISO 8601 timestamp]"
    }
  },
  "worker_outputs": {
    "style_research": "[Full worker output from Phase 1a]",
    "palette_research": "[Full palette worker output]"
  }
}
```

**State saved. Phase 1b complete.**

**Save Palette to Style Library:**

After saving state, persist the selected palette to the project's style library for future reuse.

**Use the Skill tool:**
```
Skill(skill="style-library", args="add [palette-slug]-palette \"[color definitions with hex codes]\"")
```

Example:
```
Skill(skill="style-library", args="add earthy-contrast-palette \"Primary: #4A5D4F (forest gray), Secondary: #D4C5B0 (sand), Accent: #8B7355 (warm brown), Background: #FAFAF8 (cream white), Text: #2B2B28 (near black)\"")
```

This creates a reusable preset in `style-library.md` that:
- Can be referenced in future image generation with `--style=[palette-slug]-palette`
- Maintains brand consistency across the project
- Is available to other skills like `enhance-prompt` and `image-prompt`

**Confirm to user:**
```
Palette "[Palette Name]" saved to style library as "[palette-slug]-palette".
You can use --style=[palette-slug]-palette in future image generation.
```

### Example Interaction

```
[Continuing from Phase 1a where Modern Minimal was selected]

Agent: Now let's develop color palettes that match the Modern Minimal style.

       [Spawns palette Task tool worker]

Agent: Here are 3 color palettes for the Modern Minimal style:

       1. **Neutral Foundation**
          Colors:
          • Primary neutral: #E8E3DB (warm beige)
          • Secondary neutral: #9C9A8F (sage gray)
          • Accent: #2C2C2A (charcoal)
          • Background: #F7F5F2 (off-white)
          • Text: #3A3A38 (dark gray)
          Creates a sophisticated, understated base with earthy warmth.

       2. **Earthy Contrast**
          Colors:
          • Primary: #4A5D4F (forest gray)
          • Secondary: #D4C5B0 (sand)
          • Accent: #8B7355 (warm brown)
          • Background: #FAFAF8 (cream white)
          • Text: #2B2B28 (near black)
          Stronger contrast with more depth, still grounded in nature.

       3. **Soft Minimalist**
          Colors:
          • Primary: #C9C5BA (light taupe)
          • Secondary: #A8A196 (warm gray)
          • Accent: #5F5E58 (medium gray)
          • Background: #FFFFFF (pure white)
          • Text: #454542 (soft black)
          Ultra-clean with subtle warmth, maximum clarity and space.

       Which palette resonates? (1, 2, 3, or describe modifications)

User: I like 2 but can the accent be a bit more terracotta?

Agent: I'll adjust Earthy Contrast with a warmer terracotta accent.

       [Spawns modified palette worker]

Agent: Here's the adjusted palette:

       **Earthy Contrast (Warm)**
       Colors:
       • Primary: #4A5D4F (forest gray)
       • Secondary: #D4C5B0 (sand)
       • Accent: #B85C42 (terracotta)
       • Background: #FAFAF8 (cream white)
       • Text: #2B2B28 (near black)
       Stronger contrast with earthy warmth from the terracotta accent.

       Does this work? (yes / adjust further / see other options)

User: yes

Agent: Excellent! Earthy Contrast (Warm) selected.

       [Saves updated state]
       [Invokes Skill(skill="style-library", args="add earthy-contrast-warm-palette ...")]

       ✓ Phase 1b complete: Color palette chosen
       Palette "Earthy Contrast (Warm)" saved to style library as "earthy-contrast-warm-palette".
       You can use --style=earthy-contrast-warm-palette in future image generation.

       Moving to Phase 1c: Logo Concepts generation
```

## Phase 1c: Logo Concepts (ACTIVE)

This phase generates logo concept descriptions and corresponding visual logos based on the selected style direction and color palette from previous phases.

### Process Steps

When Phase 1b is complete and state is saved, automatically proceed to Phase 1c:

**Quick Reference:**
12. Transition from Phase 1b (confirm palette is selected)
13. Spawn Logo Concept Worker (Task tool)
14. Parse worker output into 3 logo concepts
15. For each concept, spawn Logo Generation Worker (Task tool)
16. Present 3 logo images to user
17. Handle user selection and save final state

**Detailed Steps:**

#### Step 12: Transition from Phase 1b

After Step 11 (Handle User Selection and Save State) in Phase 1b completes, immediately transition to Phase 1c.

Announce the transition:
```
Now let's create logo concepts using the [Style Direction Name] style and [Palette Name] palette.
```

**Validation before proceeding:**
- Confirm `decisions.style_direction` exists in state
- Confirm `decisions.color_palette` exists in state
- Extract both for the workers' prompts

#### Step 13: Spawn Logo Concept Worker

Use the Task tool to spawn a logo concept worker with the Logo Concept Worker Prompt Template (see below).

**Tool invocation:**
```
Task(
  description="Generate logo concept descriptions",
  subagent_type="general-purpose",
  model="sonnet",
  prompt="""You are a logo concept designer. Create 3 distinct logo concepts for this brand:

Brand: [insert brand_description from state]
Style Direction: [insert style_direction.name and characteristics from state]
Color Palette: [insert color_palette.name and colors from state]

For each concept provide:
1. Concept name (2-4 words, descriptive)
2. Description of visual elements (shapes, symbols, imagery)
3. Typography approach (font style, weight, arrangement)
4. How it embodies the brand and chosen style
5. Which colors from the palette to emphasize

Make the 3 concepts distinct but all aligned with the style direction and palette. Each concept should offer a different visual approach or emphasis.

IMPORTANT: You are a research worker. Do NOT:
- Generate images (no MCP image tools)
- Spawn other workers (no Task tools)
- Interact with the user directly

Return your findings as natural language that the orchestrator will parse and present."""
)
```

Wait for the worker to return its findings.

#### Step 14: Parse Logo Concept Worker Output

The worker returns natural language. Extract for each of the 3 concepts:
- Concept name
- Visual elements description
- Typography approach
- Brand embodiment rationale
- Color emphasis

**Validation:**
- Did the worker provide all 3 concepts?
- Does each concept have all required elements?
- Are the descriptions clear enough for image generation?

**If incomplete:**
- Re-spawn worker with clarified prompt (max 2 retries)
- If still incomplete after 2 retries, inform user and offer manual input

#### Step 15: Enhance Prompts and Spawn Logo Generation Workers

For each of the 3 logo concepts, first enhance the prompt using the enhance-prompt skill, then spawn a generation worker.

**Use the Bash tool** first to ensure directory exists:
```bash
mkdir -p outputs/exploration/logos
```

**For each Concept (1, 2, 3), perform these sub-steps:**

**15a. Invoke Enhance-Prompt Skill**

```
Skill(skill="enhance-prompt", args="--quick")
```

Provide to the skill:
- Concept name
- Visual elements from the concept
- Typography approach
- Color palette from Phase 1b decisions
- Brand description

The skill returns an enhanced prompt optimized for logo generation.

**15b. Run Taste Check**

Before generating, validate the enhanced prompt:

```
Skill(skill="taste-check", args="--taste=medium")
```

Provide the enhanced prompt from Step 15a.

**If taste-check finds issues:**
1. Show the summary to the orchestrator (not directly to user during batch generation)
2. Apply suggested fixes automatically (use `--fix` behavior)
3. Proceed with the corrected prompt

**If taste-check passes:**
Proceed directly to Step 15c (generation).

**Note:** During batch logo generation (3 concepts), taste checks run silently. Only if ALL concepts fail taste check should the user be notified with a summary.

**15c. Spawn Logo Generation Worker**

**Tool invocation:**
```
Task(
  description="Generate logo image for concept [N]",
  subagent_type="general-purpose",
  model="sonnet",
  prompt="""You are an image generation specialist. Generate a logo using this enhanced prompt:

Brand: [brand_description]
Enhanced Prompt: [output from enhance-prompt skill]

Use the MCP generate_image tool with:
- prompt: [the enhanced prompt]
- aspect_ratio: "1:1"
- resolution: "2K"
- output_path: outputs/exploration/logos/concept-[N]-[slugified-concept-name].png

Return the saved file path and a brief confirmation.

IMPORTANT: You are a generation worker. You MUST:
- Use the generate_image MCP tool with the enhanced prompt EXACTLY as provided
- Save the image to the specified path
- Return the file path

Do NOT:
- Modify the enhanced prompt
- Spawn other workers (no Task tools)
- Interact with the user directly"""
)
```

Replace `[N]` with 1, 2, or 3 respectively.
Replace `[slugified-concept-name]` with a slug version of the concept name (lowercase, hyphens for spaces).

Wait for each worker to complete and return the image path.

**Validation after each generation:**
- Did the worker return a valid file path?
- Does the file exist at that path?

**If generation fails:**
- Retry once with clarified instructions
- If still fails, inform user and continue with other concepts

#### Step 16: Present Logo Images

Once all 3 logos are generated (or attempts completed), present them to the user.

Format the results clearly:

```
Here are 3 logo concepts for [Brand Description]:

1. **[Concept 1 Name]**
   [Brief description of visual elements and typography]
   Image: outputs/exploration/logos/concept-1-[slug].png

2. **[Concept 2 Name]**
   [Brief description of visual elements and typography]
   Image: outputs/exploration/logos/concept-2-[slug].png

3. **[Concept 3 Name]**
   [Brief description of visual elements and typography]
   Image: outputs/exploration/logos/concept-3-[slug].png

Which logo concept works best for your brand? (1, 2, 3, or describe modifications)
```

#### Step 17: Handle User Selection and Save Final State

Wait for user response.

**If user selects 1, 2, or 3:**
- Confirm selection:
  ```
  Perfect! [Concept Name] selected.

  ✓ Phase 1c complete: Logo concept chosen

  Brand identity complete! All 3 phases finished:
  • Style: [Style Direction Name]
  • Palette: [Palette Name]
  • Logo: [Logo Concept Name]

  All files saved to outputs/exploration/logos/
  ```
- Proceed to save final state (see Final State Save below)

**If user describes modifications:**
- Parse their requested changes
- Confirm understanding:
  ```
  I'll adjust [Concept Name] with [their modifications].
  ```
- Spawn modified logo generation worker with the refinement request
- Present the adjusted logo
- Ask for confirmation
- Proceed to save final state when confirmed

**If user is unclear:**
- Ask for clarification:
  ```
  Did you mean logo [N]? Or would you like to adjust one of them?

  You can:
  - Choose 1, 2, or 3
  - Ask to modify a logo ("I like 1 but make the icon more abstract")
  - Describe different visual elements you prefer
  ```

**Final State Save:**

**Use the Read tool** to load current state from `.claude/local/agent-state.json`:
- This should succeed since Phase 1b saved the state

Parse the JSON and update:
- Set `current_phase` to `"1c_complete"`
- Add logo selection to `decisions.logo_concept`
- Add worker outputs to `worker_outputs`

**Use the Write tool** to save updated state:

```json
{
  "brand_description": "[user's brand description]",
  "started": "[ISO 8601 timestamp from Phase 1a]",
  "current_phase": "1c_complete",
  "first_run_complete": true,
  "decisions": {
    "style_direction": {
      "name": "[Selected Direction Name]",
      "characteristics": "[Visual characteristics]",
      "mood": "[Mood/emotion]",
      "selected_at": "[ISO 8601 timestamp]"
    },
    "color_palette": {
      "name": "[Selected Palette Name]",
      "colors": [
        {"name": "[Color 1 usage]", "hex": "#HEXCODE"},
        {"name": "[Color 2 usage]", "hex": "#HEXCODE"},
        {"name": "[Color 3 usage]", "hex": "#HEXCODE"},
        {"name": "[Color 4 usage]", "hex": "#HEXCODE"},
        {"name": "[Color 5 usage]", "hex": "#HEXCODE"}
      ],
      "rationale": "[Why this palette works]",
      "selected_at": "[ISO 8601 timestamp]"
    },
    "logo_concept": {
      "name": "[Selected Logo Concept Name]",
      "visual_elements": "[Visual elements description]",
      "typography": "[Typography approach]",
      "rationale": "[How it embodies the brand]",
      "image_path": "outputs/exploration/logos/concept-[N]-[slug].png",
      "selected_at": "[ISO 8601 timestamp]"
    }
  },
  "worker_outputs": {
    "style_research": "[Full worker output from Phase 1a]",
    "palette_research": "[Full palette worker output from Phase 1b]",
    "logo_concepts": "[Full logo concept worker output]",
    "logo_generation": {
      "concept_1": "[Generation worker 1 output]",
      "concept_2": "[Generation worker 2 output]",
      "concept_3": "[Generation worker 3 output]"
    }
  }
}
```

**State saved. Phase 1c complete. Brand identity project complete.**

### Example Interaction

```
[Continuing from Phase 1b where Earthy Contrast palette was selected]

Agent: Now let's create logo concepts using the Modern Minimal style and
       Earthy Contrast palette.

       [Spawns logo concept Task tool worker]

Agent: I've created 3 logo concepts. Now generating the visual logos...

       [Spawns 3 logo generation workers sequentially]

Agent: Here are 3 logo concepts for your artisan coffee shop:

       1. **Bean & Geometry**
          Simple coffee bean icon with geometric facets, paired with clean
          sans-serif wordmark. Uses forest gray and terracotta.
          Image: outputs/exploration/logos/concept-1-bean-geometry.png

       2. **Minimalist Mark**
          Abstract "A" letterform incorporating negative space cup silhouette.
          Text-only design with subtle sand accent line.
          Image: outputs/exploration/logos/concept-2-minimalist-mark.png

       3. **Origin Stamp**
          Circular badge with simplified mountain/origin illustration,
          vintage-modern hybrid. Charcoal primary with terracotta accent.
          Image: outputs/exploration/logos/concept-3-origin-stamp.png

       Which logo concept works best for your brand? (1, 2, 3, or describe
       modifications)

User: I like 1 but can the bean be more stylized?

Agent: I'll adjust Bean & Geometry with a more stylized, abstract bean.

       [Spawns modified logo generation worker]

Agent: Here's the adjusted logo:

       **Bean & Geometry (Stylized)**
       Highly geometric, abstract coffee bean with angular facets,
       paired with clean sans-serif wordmark.
       Image: outputs/exploration/logos/concept-1-bean-geometry-v2.png

       Does this work? (yes / adjust further / see other options)

User: yes

Agent: Perfect! Bean & Geometry (Stylized) selected.

       ✓ Phase 1c complete: Logo concept chosen

       Brand identity complete! All 3 phases finished:
       • Style: Modern Minimal
       • Palette: Earthy Contrast
       • Logo: Bean & Geometry (Stylized)

       All files saved to outputs/exploration/logos/

       [Saves final state]
```

## Navigation Command Implementation

### `/agent show` - Redisplay Current Options

When user types `/agent show`, redisplay the options at the current phase without re-running workers.

**Implementation:**

1. **Use the Read tool** to load `.claude/local/agent-state.json`
2. Check `current_phase` value
3. Based on phase, redisplay the cached worker output:

**If `current_phase === "1a_complete"` or user is in Phase 1a:**
- Parse `worker_outputs.style_research`
- Redisplay the 3 style directions in the same format as Step 4 (Phase 1a)
- Include reminder: "Previously selected: [style_direction.name]" if already chosen

**If `current_phase === "1b_complete"` or user is in Phase 1b:**
- Parse `worker_outputs.palette_research`
- Redisplay the 3 color palettes in the same format as Step 10 (Phase 1b)
- Include reminder: "Previously selected: [color_palette.name]" if already chosen

**If user is in Phase 1c:**
- Parse `worker_outputs.logo_concepts` and `worker_outputs.logo_generation`
- Redisplay the 3 logo images in the same format as Step 16 (Phase 1c)
- Include reminder: "Previously selected: [logo_concept.name]" if already chosen

**If no state file exists:**
```
No active brand identity session found. Use `/agent brand "description"` to start.
```

**Example:**
```
User: /agent show

Agent: Here are the 3 style directions again:

       1. **Rustic Craftsman**
          Warm browns and burnt orange, hand-drawn illustrations,
          vintage serif typography. Evokes warmth, tradition, handmade quality.

       2. **Modern Minimal** (Previously selected)
          Clean lines, muted earth tones (beige, sage, charcoal),
          geometric shapes, sans-serif fonts. Conveys sophistication,
          clarity, contemporary craft.

       3. **Botanical Organic**
          Forest greens and natural creams, botanical illustrations,
          organic textures, script accents. Suggests freshness,
          sustainability, connection to nature.

       Keep "Modern Minimal" or select a different direction? (1, 2, 3, or describe)
```

### `/agent back` - Return to Previous Checkpoint

When user types `/agent back`, allow them to return to a previous phase and re-select.

**Implementation:**

1. **Use the Read tool** to load `.claude/local/agent-state.json`
2. Check `current_phase` value
3. Determine which phase to return to:

**If `current_phase === "1b_complete"` or user is in Phase 1c:**
- Return to Phase 1b (palette selection)
- Parse `worker_outputs.palette_research`
- Redisplay the 3 palette options
- Show warning:
  ```
  Returning to Phase 1b: Color Palette selection.

  Previously selected: [color_palette.name]

  Warning: If you change your palette, any logo work will be cleared.

  Here are the 3 color palettes for the [Style Direction Name] style:
  [Redisplay palettes from Step 10]

  Keep "[color_palette.name]" or select a different palette? (1, 2, 3, or describe)
  ```
- If user selects a different palette, clear `decisions.logo_concept` from state

**If `current_phase === "1a_complete"` or user is in Phase 1b:**
- Return to Phase 1a (style direction selection)
- Parse `worker_outputs.style_research`
- Redisplay the 3 style directions
- Show warning:
  ```
  Returning to Phase 1a: Style Direction selection.

  Previously selected: [style_direction.name]

  Warning: If you change your style, all palette and logo work will be cleared.

  Here are the 3 style directions again:
  [Redisplay directions from Step 4]

  Keep "[style_direction.name]" or select a different direction? (1, 2, 3, or describe)
  ```
- If user selects a different direction, clear `decisions.color_palette` and `decisions.logo_concept` from state

**If no state file exists:**
```
No active brand identity session found. Use `/agent brand "description"` to start.
```

**Advanced: `/agent back to [phase]`**

User can specify which phase to return to:
- `/agent back to style` - Jump to Phase 1a
- `/agent back to palette` - Jump to Phase 1b

Same logic as above, but skip intermediate phases.

**Example:**
```
User: /agent back

Agent: Returning to Phase 1b: Color Palette selection.

       Previously selected: Earthy Contrast

       Warning: If you change your palette, logo work will be cleared.

       Here are the 3 color palettes for the Modern Minimal style:

       1. **Neutral Foundation**
          [... palette details ...]

       2. **Earthy Contrast** (Previously selected)
          [... palette details ...]

       3. **Soft Minimalist**
          [... palette details ...]

       Keep "Earthy Contrast" or select a different palette? (1, 2, 3, or describe)

User: 3

Agent: Soft Minimalist selected.

       ✓ Phase 1b complete: Color palette changed

       Previous logo work has been cleared.

       Moving to Phase 1c: Logo Concepts generation

       [Proceeds with Phase 1c using new palette]
```

## Worker Communication Protocol

### How to Spawn a Worker

When you need to spawn a Task tool worker (see Step 2 in Phase 1a, Step 8 in Phase 1b):

```
Task(
  description="Short 3-5 word description",
  subagent_type="general-purpose",
  model="sonnet",
  prompt="[Your worker prompt here with embedded context]"
)
```

**Key points:**
- Always include `description` parameter (3-5 words describing the task)
  - Phase 1a: "Research brand style directions"
  - Phase 1b: "Generate color palette options"
  - Phase 1c (concept): "Generate logo concept descriptions"
  - Phase 1c (generation): "Generate logo image for concept [N]"
- Always use `subagent_type="general-purpose"` for all workers
- Always use `model="sonnet"` for consistency
- Embed all necessary context directly in the prompt string
- Include clear instructions about what the worker should NOT do
- Logo generation workers ARE allowed to use MCP image tools (unlike research workers)

### How to Parse Worker Output

Workers return natural language responses. You must:

1. **Extract structured information**

   **Phase 1a (Style Research):**
   - Look for the 3 direction names
   - Extract visual characteristics for each
   - Extract mood/emotion for each
   - Extract "why it fits" rationale for each

   **Phase 1b (Palette Research):**
   - Look for the 3 palette names
   - Extract 5-6 colors with hex codes for each
   - Extract usage notes for each color (primary, accent, etc.)
   - Extract rationale for each palette

   **Phase 1c (Logo Concepts):**
   - Look for the 3 concept names
   - Extract visual elements for each
   - Extract typography approach for each
   - Extract rationale for each
   - Extract color emphasis for each

   **Phase 1c (Logo Generation):**
   - Extract the image file path returned by the worker
   - Verify the file exists at that path

2. **Format for user presentation**
   - Use the format shown in Process Steps (Step 4 for Phase 1a, Step 10 for Phase 1b, Step 16 for Phase 1c)
   - Keep it concise but complete
   - Maintain the user-friendly tone

3. **Validate completeness**
   - Did the worker provide all 3 options (directions, palettes, or concepts)?
   - Does each option have all required elements?
   - For Phase 1b: Are hex codes in valid format (#RRGGBB)?
   - For Phase 1c generation: Does the image file exist?
   - If not, re-spawn with clarified instructions (max 2 retries)

### Error Handling

| Worker Issue | Orchestrator Response |
|--------------|----------------------|
| Worker returns incomplete data | Re-spawn with clarified prompt |
| Worker violates restrictions (tries to generate) | Ignore invalid actions, parse valid output |
| Worker fails entirely | Report to user, offer to retry or manual input |

## State Management

State is saved to `.claude/local/agent-state.json` to enable resuming sessions and tracking decisions.

### State File Location

Always use: `.claude/local/agent-state.json`

### When to Create/Update State

| Event | Action |
|-------|--------|
| Phase 1a selection confirmed | Use Bash tool to create `.claude/local/` (if needed), use Write tool to save full state with `first_run_complete: true` |
| Phase 1b selection confirmed | Use Read tool to load current state, update `current_phase` to "1b_complete" and add `decisions.color_palette`, use Write tool to save |
| Phase 1c selection confirmed | Use Read tool to load current state, update `current_phase` to "1c_complete" and add `decisions.logo_concept`, use Write tool to save |
| Project completes | Brand identity complete, state file preserved for reference |
| User starts fresh | Use Bash tool to delete state file |

### State File Format

**After Phase 1a:**
```json
{
  "brand_description": "artisan coffee shop",
  "started": "2026-01-23T10:30:00Z",
  "current_phase": "1a_complete",
  "first_run_complete": true,
  "decisions": {
    "style_direction": {
      "name": "Modern Minimal",
      "characteristics": "Clean lines, muted earth tones, geometric shapes, sans-serif fonts",
      "mood": "Sophistication, clarity, contemporary craft",
      "selected_at": "2026-01-23T10:32:00Z"
    },
    "color_palette": null,
    "logo_concept": null
  },
  "worker_outputs": {
    "style_research": "[Full worker output text]",
    "palette_research": null
  }
}
```

**After Phase 1b:**
```json
{
  "brand_description": "artisan coffee shop",
  "started": "2026-01-23T10:30:00Z",
  "current_phase": "1b_complete",
  "first_run_complete": true,
  "decisions": {
    "style_direction": {
      "name": "Modern Minimal",
      "characteristics": "Clean lines, muted earth tones, geometric shapes, sans-serif fonts",
      "mood": "Sophistication, clarity, contemporary craft",
      "selected_at": "2026-01-23T10:32:00Z"
    },
    "color_palette": {
      "name": "Earthy Contrast",
      "colors": [
        {"name": "Primary", "hex": "#4A5D4F"},
        {"name": "Secondary", "hex": "#D4C5B0"},
        {"name": "Accent", "hex": "#8B7355"},
        {"name": "Background", "hex": "#FAFAF8"},
        {"name": "Text", "hex": "#2B2B28"}
      ],
      "rationale": "Stronger contrast with more depth, still grounded in nature",
      "selected_at": "2026-01-23T10:35:00Z"
    },
    "logo_concept": null
  },
  "worker_outputs": {
    "style_research": "[Full worker output text]",
    "palette_research": "[Full palette worker output]"
  }
}
```

**After Phase 1c (Complete):**
```json
{
  "brand_description": "artisan coffee shop",
  "started": "2026-01-23T10:30:00Z",
  "current_phase": "1c_complete",
  "first_run_complete": true,
  "decisions": {
    "style_direction": {
      "name": "Modern Minimal",
      "characteristics": "Clean lines, muted earth tones, geometric shapes, sans-serif fonts",
      "mood": "Sophistication, clarity, contemporary craft",
      "selected_at": "2026-01-23T10:32:00Z"
    },
    "color_palette": {
      "name": "Earthy Contrast",
      "colors": [
        {"name": "Primary", "hex": "#4A5D4F"},
        {"name": "Secondary", "hex": "#D4C5B0"},
        {"name": "Accent", "hex": "#8B7355"},
        {"name": "Background", "hex": "#FAFAF8"},
        {"name": "Text", "hex": "#2B2B28"}
      ],
      "rationale": "Stronger contrast with more depth, still grounded in nature",
      "selected_at": "2026-01-23T10:35:00Z"
    },
    "logo_concept": {
      "name": "Bean & Geometry",
      "visual_elements": "Simple coffee bean icon with geometric facets",
      "typography": "Clean sans-serif wordmark",
      "rationale": "Combines modern minimalism with coffee shop identity",
      "image_path": "outputs/exploration/logos/concept-1-bean-geometry.png",
      "selected_at": "2026-01-23T10:40:00Z"
    }
  },
  "worker_outputs": {
    "style_research": "[Full worker output text]",
    "palette_research": "[Full palette worker output]",
    "logo_concepts": "[Full logo concept worker output]",
    "logo_generation": {
      "concept_1": "[Generation worker 1 output]",
      "concept_2": "[Generation worker 2 output]",
      "concept_3": "[Generation worker 3 output]"
    }
  }
}
```

### How to Read State (Resume Flow)

In Step 1b of Process Steps (Phase 1a), **use the Read tool** to read `.claude/local/agent-state.json`:

- **If Read succeeds:** Parse the JSON content and extract the fields below
- **If Read returns an error:** The file doesn't exist; inform user no previous session found

Parse the JSON to extract:
- `brand_description` - Show to user for context
- `current_phase` - Determine where to resume
  - `"1a_complete"`: Resume from Phase 1b (palette generation)
  - `"1b_complete"`: Resume from Phase 1c (logo concepts)
  - `"1c_complete"`: Brand identity already complete
- `decisions.style_direction` - Show what's already been selected
- `decisions.color_palette` - Show if Phase 1b was completed
- `decisions.logo_concept` - Show if Phase 1c was completed
- `started` - Show how long ago the session started

**Resume Logic:**
- If `current_phase === "1a_complete"`: Proceed directly to Step 7 (Phase 1b)
- If `current_phase === "1b_complete"`: Proceed directly to Step 12 (Phase 1c)
- If `current_phase === "1c_complete"`: Inform user project is complete, offer to start fresh or review
- If phase is incomplete: Resume at the last incomplete phase

## Checkpoints

Checkpoints allow users to return to previous decisions:

| Checkpoint | Data Saved | Back Action |
|------------|------------|-------------|
| After style selection (Phase 1a) | Style direction + characteristics | Return to style options, allow re-selection |
| After palette selection (Phase 1b) | Palette name + colors with hex codes | Return to palette options, allow re-selection |
| After logo selection (Phase 1c) | Logo concept + image path | Return to logo options, allow re-selection |

**Back Command Examples:**

See "Navigation Command Implementation" section above for full implementation details.

## Error Handling

How to handle common error scenarios:

### Empty or Very Short Brand Description

**If brand description is empty or < 5 characters:**

Respond with:
```
Please describe your brand. What does it do? Who is it for? What makes it unique?

Example: "artisan coffee shop focused on single-origin beans"
```

Wait for user to provide more context, then proceed to Step 2.

### Worker Returns Invalid Output

**Phase 1a: If style research worker doesn't return all 3 directions or missing required elements:**

1. First retry: Re-spawn worker with clarified prompt emphasizing the missing elements
2. Second retry: Re-spawn worker with even more explicit instructions
3. After 2 retries: Inform user and offer manual input

```
The research worker had trouble generating complete options. Would you like me to:
1. Try one more time with different approach
2. Let you describe your preferred style directions manually
```

**Phase 1b: If palette worker doesn't return all 3 palettes or missing hex codes:**

1. First retry: Re-spawn worker with clarified prompt emphasizing complete palettes with hex codes
2. Second retry: Re-spawn worker with explicit format requirements
3. After 2 retries: Inform user and offer manual input

```
The palette worker had trouble generating complete color palettes. Would you like me to:
1. Try one more time with different approach
2. Let you describe your preferred palette manually (color names and hex codes)
```

### User Provides Unclear Selection

**If user response doesn't clearly map to 1, 2, 3, or a custom direction:**

Ask for clarification:
```
Did you mean option [N]? Or would you like something different?

You can:
- Choose 1, 2, or 3
- Ask to refine an option ("I like 1 but make it warmer")
- Describe your own direction
```

### State File Corrupted

**If state file exists but JSON is malformed:**

```
Found a previous session but the state file is corrupted.

Starting fresh. Would you like to manually re-enter previous decisions? (yes / no)
```

If yes, walk through what they decided before. If no, start from Step 2.

### All Phases Complete (Future)

**When all phases are done:**

```
Brand identity complete! Here's a summary:

**Style Direction:** [name and characteristics]
**Color Palette:** [palette details] (future)
**Logo Concept:** [logo details] (future)

All decisions saved to .claude/local/agent-state.json
```

## Examples

### Complete Phase 1a + 1b Flow

```
User: /agent brand "boutique yoga studio focused on mindfulness"

Agent: I'll help create a brand identity for your boutique yoga studio
       focused on mindfulness. Let me research some style directions.

       [Spawns research worker]

Agent: Based on mindfulness-focused yoga studio aesthetics, here are 3
       style directions:

       1. **Serene Minimalist**
          Soft neutrals (cream, warm gray, pale sand), generous white space,
          simple line art, clean sans-serif fonts. Evokes calm, clarity,
          spaciousness.

       2. **Organic Earth**
          Terracotta, sage green, natural textures, hand-drawn elements,
          earthy typography. Conveys grounding, connection to nature, warmth.

       3. **Modern Zen**
          Deep navy and soft blush, geometric mandalas, balanced compositions,
          refined serif fonts. Suggests discipline, elegance, inner peace.

       Which direction resonates? (1, 2, 3, or describe something different)

User: 1

Agent: Perfect! Serene Minimalist direction selected.

       ✓ Phase 1a complete: Style direction chosen

       Moving to Phase 1b: Color Palette generation

       [Saves state]

Agent: Now let's develop color palettes that match the Serene Minimalist style.

       [Spawns palette worker]

Agent: Here are 3 color palettes for the Serene Minimalist style:

       1. **Soft Foundation**
          Colors:
          • Primary neutral: #F5F1EA (warm cream)
          • Secondary neutral: #D8D3CA (soft taupe)
          • Accent: #A89F91 (warm gray)
          • Background: #FEFDFB (off-white)
          • Text: #4A4741 (charcoal)
          Creates a gentle, inviting base with subtle warmth.

       2. **Natural Light**
          Colors:
          • Primary: #FAF7F2 (pale sand)
          • Secondary: #E6DFD5 (light beige)
          • Accent: #C9BFB3 (medium taupe)
          • Background: #FFFFFF (pure white)
          • Text: #3D3935 (soft black)
          Maximizes brightness and airy spaciousness.

       3. **Warm Minimal**
          Colors:
          • Primary: #F0EBE3 (warm white)
          • Secondary: #CFC7BC (greige)
          • Accent: #B5A393 (sand brown)
          • Background: #F8F6F3 (cream)
          • Text: #45423E (dark gray)
          Balances minimalism with inviting warmth.

       Which palette resonates? (1, 2, 3, or describe modifications)

User: 3

Agent: Excellent! Warm Minimal selected.

       ✓ Phase 1b complete: Color palette chosen

       [Phase 1c: Logo Concepts - coming soon]

       [Saves updated state]
```

### Complete Phase 1a Flow (Simple)

```
User: /agent brand "boutique yoga studio focused on mindfulness"

Agent: I'll help create a brand identity for your boutique yoga studio
       focused on mindfulness. Let me research some style directions.

       [Spawns research worker]

Agent: Based on mindfulness-focused yoga studio aesthetics, here are 3
       style directions:

       1. **Serene Minimalist**
          Soft neutrals (cream, warm gray, pale sand), generous white space,
          simple line art, clean sans-serif fonts. Evokes calm, clarity,
          spaciousness.

       2. **Organic Earth**
          Terracotta, sage green, natural textures, hand-drawn elements,
          earthy typography. Conveys grounding, connection to nature, warmth.

       3. **Modern Zen**
          Deep navy and soft blush, geometric mandalas, balanced compositions,
          refined serif fonts. Suggests discipline, elegance, inner peace.

       Which direction resonates? (1, 2, 3, or describe something different)

User: I like 1 but can it be a bit warmer?

Agent: Absolutely. Let me refine the Serene Minimalist direction with warmer tones.

       [Spawns modified research task]

Agent: Here's the adjusted direction:

       **Serene Minimalist (Warm)**
       Warm whites, soft beige, pale peach accents, generous space,
       simple line art, rounded sans-serif fonts. Evokes calm, gentle warmth,
       welcoming spaciousness.

       Does this refined direction work? (yes / adjust further / see other options)

User: yes

Agent: Perfect! Serene Minimalist (Warm) direction selected.

       ✓ Phase 1a complete: Style direction chosen

       [Phase 1b: Color Palette - coming soon]

       When Phase 1b is implemented, I'll generate palette options based
       on this warm minimalist direction.
```

### Requesting Status (Future)

**After Phase 1a:**
```
User: /agent status

Agent: ## Brand Identity Progress

       **Brand:** Boutique yoga studio focused on mindfulness
       **Started:** 2026-01-23 at 10:30 AM
       **Current Phase:** 1a complete, 1b pending

       **Decisions Made:**
       ✓ Style Direction: Serene Minimalist
         - Soft neutrals, generous white space
         - Simple line art, clean sans-serif fonts
         - Evokes calm, clarity, spaciousness

       **Next Steps:**
       Phase 1b: Color Palette generation

       Use `/agent show` to review current options
       Use `/agent back` to change previous decisions
```

**After Phase 1b:**
```
User: /agent status

Agent: ## Brand Identity Progress

       **Brand:** Boutique yoga studio focused on mindfulness
       **Started:** 2026-01-23 at 10:30 AM
       **Current Phase:** 1b complete, 1c pending

       **Decisions Made:**
       ✓ Style Direction: Serene Minimalist
         - Soft neutrals, generous white space, simple line art

       ✓ Color Palette: Warm Minimal
         - Primary: #F0EBE3 (warm white)
         - Secondary: #CFC7BC (greige)
         - Accent: #B5A393 (sand brown)
         - Background: #F8F6F3 (cream)
         - Text: #45423E (dark gray)

       **Next Steps:**
       Phase 1c: Logo Concepts (not implemented yet)

       Use `/agent show` to review current options
       Use `/agent back` to change previous decisions
```

### Resuming After Phase 1a

```
User: /agent brand --resume

Agent: Found previous brand identity session from 2 hours ago.

       **Brand:** Artisan coffee shop
       **Last Phase:** 1a complete (Style: Modern Minimal selected)

       Continue from Phase 1b: Color Palette? (yes / start fresh)

User: yes

Agent: Resuming from Phase 1b.

       Selected style: Modern Minimal (clean lines, muted earth tones,
       geometric shapes, sans-serif fonts)

       Now let's develop color palettes that match the Modern Minimal style.

       [Spawns palette worker and proceeds with Phase 1b]
```

### Resuming After Phase 1b (Future)

```
User: /agent brand --resume

Agent: Found previous brand identity session from yesterday.

       **Brand:** Artisan coffee shop
       **Last Phase:** 1b complete

       Decisions made:
       • Style: Modern Minimal
       • Palette: Earthy Contrast (forest gray, sand, warm brown)

       Continue from Phase 1c: Logo Concepts? (yes / start fresh)

User: yes

Agent: Resuming from Phase 1c.

       [Would spawn logo concept worker - not implemented yet]

       Phase 1c coming soon.
```

## Phase 2: Product Designs (ACTIVE)

After brand identity is complete (Phase 1c), this phase creates product designs using the established style and palette. **This phase MUST chain to other skills** - never generate images directly.

### Critical Requirements for Phase 2

**MUST DO:**
- ✓ Invoke `superpowers:brainstorming` skill BEFORE any creative design work
- ✓ Use `AskUserQuestion` tool to gather product type, theme, and quantity
- ✓ Invoke `enhance-prompt` skill to craft effective image prompts
- ✓ Delegate ALL image generation to Task tool workers
- ✓ Save design collection to state after completion

**MUST NOT:**
- ✗ Generate images directly with MCP tools (orchestrator never generates)
- ✗ Skip the brainstorming skill before creative work
- ✗ Skip the enhance-prompt skill for prompt crafting
- ✗ Bypass Task tool workers for generation

### Process Steps

When Phase 1c is complete and user asks "what's next?" or requests product designs:

**Quick Reference:**
18. Detect Phase 2 trigger (user wants product designs)
19. Invoke brainstorming skill for creative exploration
20. Use AskUserQuestion to gather requirements
21. Spawn Design Concept Worker (Task tool)
22. Invoke enhance-prompt skill for each design
23. Spawn Design Generation Workers (Task tool)
24. Present designs and handle selection
25. Save design collection to state

**Detailed Steps:**

#### Step 18: Detect Phase 2 Trigger

After Phase 1c completion, if user asks about next steps or product designs:

```
Brand identity complete! Ready to create product designs using your:
• Style: [Style Direction Name]
• Palette: [Palette Name]

Would you like to create product designs? (yes / not now)
```

If yes, proceed to Step 19.

#### Step 19: Invoke Brainstorming Skill

**REQUIRED:** Before any creative design work, invoke the brainstorming skill.

```
Skill(skill="superpowers:brainstorming")
```

Follow the brainstorming skill's process to explore:
- What product types make sense for this brand
- What themes align with the style direction
- What design approaches would work

**Do NOT skip this step.** The brainstorming skill ensures proper creative exploration before execution.

#### Step 20: Gather Requirements with AskUserQuestion

After brainstorming, use `AskUserQuestion` to confirm specifics:

```
AskUserQuestion(questions=[
  {
    "question": "What product type should we design for first?",
    "header": "Product",
    "options": [
      {"label": "Wall Art / Posters", "description": "High-impact visuals"},
      {"label": "T-Shirts / Apparel", "description": "Simpler compositions"},
      {"label": "Phone Cases", "description": "Vertical format"},
      {"label": "All-over prints", "description": "Seamless patterns"}
    ],
    "multiSelect": false
  },
  {
    "question": "Which theme should we explore?",
    "header": "Theme",
    "options": [
      // Options based on brainstorming output
    ],
    "multiSelect": false
  },
  {
    "question": "How many designs should we create?",
    "header": "Quantity",
    "options": [
      {"label": "3 designs", "description": "Quick test batch"},
      {"label": "5 designs", "description": "Small collection"},
      {"label": "10 designs", "description": "Full collection"}
    ],
    "multiSelect": false
  }
])
```

#### Step 21: Spawn Design Concept Worker

Based on user answers, spawn a concept worker to create design briefs:

```
Task(
  description="Create product design concepts",
  subagent_type="general-purpose",
  model="sonnet",
  prompt="""You are a product design specialist. Create [N] distinct design concepts for [product type]:

Brand: [brand_description]
Style Direction: [style_direction.name and characteristics]
Color Palette: [color_palette colors with hex codes]
Theme: [selected theme]

For each design concept provide:
1. Concept name (2-4 words)
2. Visual description (what the design depicts)
3. Composition approach (layout, focal points)
4. Which palette colors to emphasize
5. Mood/emotion it conveys

Make each concept distinct but all aligned with the brand identity.

IMPORTANT: You are a research worker. Do NOT:
- Generate images (no MCP image tools)
- Spawn other workers (no Task tools)
- Interact with the user directly

Return your findings as natural language."""
)
```

#### Step 22: Invoke Enhance-Prompt Skill

For each design concept, **invoke the enhance-prompt skill** to craft an effective image prompt:

```
Skill(skill="enhance-prompt")
```

Provide the design concept details and let enhance-prompt transform it into an optimal image generation prompt.

**Do NOT skip this step.** The enhance-prompt skill ensures high-quality image generation prompts.

#### Step 23: Spawn Design Generation Workers

For each enhanced prompt, spawn a generation worker:

**Use the Bash tool** first to ensure directory exists:
```bash
mkdir -p outputs/designs/[product-type]
```

**For each design, spawn worker:**
```
Task(
  description="Generate product design [N]",
  subagent_type="general-purpose",
  model="sonnet",
  prompt="""You are an image generation specialist. Generate a product design:

Brand: [brand_description]
Style Direction: [style_direction characteristics]
Color Palette: [hex codes]

Design Concept: [concept name]
Enhanced Prompt: [output from enhance-prompt skill]

Use the MCP generate_image tool to create this design.

Save to: outputs/designs/[product-type]/[NN]-[slugified-name].png

Return the saved file path.

IMPORTANT: You are a generation worker. You MUST:
- Use the generate_image MCP tool
- Save the image to the specified path
- Return the file path

Do NOT:
- Spawn other workers (no Task tools)
- Research or interact with the user directly"""
)
```

#### Step 24: Present Designs and Handle Selection

Present completed designs:

```
Here are [N] [product type] designs for [Brand]:

1. **[Design 1 Name]**
   [Brief description]
   Image: outputs/designs/[product-type]/01-[slug].png

2. **[Design 2 Name]**
   ...

[Continue for all designs]

Review the designs. You can:
- Request regeneration of specific designs
- Create more designs in this collection
- Move to a different product type
- Export the collection
```

#### Step 25: Save Design Collection to State

**Use the Read tool** to load current state, then update:

```json
{
  "current_phase": "2_complete",
  "decisions": {
    // ... existing Phase 1 decisions ...
    "product_designs": {
      "product_type": "[selected product type]",
      "theme": "[selected theme]",
      "designs": [
        {
          "name": "[Design 1 Name]",
          "description": "[description]",
          "image_path": "outputs/designs/...",
          "created_at": "[timestamp]"
        }
        // ... more designs ...
      ],
      "completed_at": "[timestamp]"
    }
  }
}
```

### Example Interaction

```
[After Phase 1c completion]

Agent: Brand identity complete! Ready to create product designs using your:
       • Style: Cosmic Glitch
       • Palette: Nebula Fracture

       Would you like to create product designs? (yes / not now)

User: yes

Agent: I'm invoking the brainstorming skill to explore design directions.

       [Invokes Skill(skill="superpowers:brainstorming")]
       [Follows brainstorming process]

Agent: Based on our exploration, let me gather specifics.

       [Uses AskUserQuestion for product type, theme, quantity]

User: [Selects T-Shirts, Extra Celestial theme, 10 designs]

Agent: Creating 10 t-shirt design concepts...

       [Spawns Design Concept Worker]

Agent: I have 10 concepts. Now enhancing prompts for optimal generation.

       [Invokes Skill(skill="enhance-prompt") for each]

Agent: Generating designs with enhanced prompts...

       [Spawns 10 Design Generation Workers sequentially]

Agent: Here are 10 t-shirt designs for your AI Art POD store:

       1. **Nebula Burst** ...
       [... presents all designs ...]

       [Saves collection to state]
```

### Skill Chaining Requirements

Phase 2 REQUIRES invoking these skills in order:

| Order | Skill | Purpose |
|-------|-------|---------|
| 1 | `superpowers:brainstorming` | Creative exploration before design |
| 2 | `enhance-prompt` | Craft effective image prompts |

**Never skip skill invocations.** The orchestrator coordinates but delegates specialized work to appropriate skills.

### Red Flags - STOP If You Notice

- About to generate an image directly → STOP, spawn a Task tool worker instead
- About to write an image prompt without enhance-prompt → STOP, invoke the skill first
- About to start designing without brainstorming → STOP, invoke brainstorming first
- Rationalizing "this is simple enough to skip skills" → This is ALWAYS wrong

## Extension Points

Phase 1a, 1b, 1c, and Phase 2 are now complete. Future phases can follow the same pattern:

**The architecture is designed to extend naturally:**
- Each phase follows the same pattern (research → present → select → checkpoint)
- Worker prompts are templates with clear boundaries
- State management is centralized and consistent
- All 3 phases demonstrate the full pattern

**To add a new phase:**
1. Create worker prompt template(s) following Phase 1a/1b/1c examples
2. Add Process Steps with numbered instructions
3. Update state file format to include new decision
4. Add parsing logic for worker outputs
5. Update resume logic to handle new phase
6. Update `/agent show` and `/agent back` to support new phase
7. Add error handling for phase-specific issues

## Technical Notes

**Why Task Tool Workers?**
- Isolation: Workers can't accidentally interfere with orchestrator state
- Clarity: Clear separation between research and execution
- Scalability: Easy to add new worker types (palette, logo, etc.)
- Safety: Workers have advisory restrictions to prevent cross-contamination

**Why Not Direct Tool Calls?**
- Brand identity requires multi-step reasoning and exploration
- Workers provide natural language explanations, not just outputs
- Orchestrator needs to parse, validate, and present information
- Maintains conversational flow with user

**Worker Restrictions:**
- Advisory only (in prompts), not enforced by system
- Research workers (Phase 1a style, Phase 1b palette, Phase 1c concept) should not generate images
- Generation workers (Phase 1c logo generation) ARE allowed to use MCP image tools
- Workers should not spawn sub-workers (flat hierarchy)
- Workers return findings to orchestrator, not to user directly

## Future Enhancements

Beyond Phase 1c:

- **Phase 2: Supporting Materials** - Business card, letterhead concepts
- **Phase 3: Digital Assets** - Social media templates, website hero
- **Export Package** - ZIP with all finals, style guide, asset log
- **Variation Generator** - Spawn workers to create 3 variations of any concept
- **Feedback Loop** - "Why did you choose X?" reflection prompts
