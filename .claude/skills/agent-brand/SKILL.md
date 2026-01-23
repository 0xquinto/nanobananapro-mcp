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
Once the skill is active, you interact naturally with the agent. The agent maintains state across messages in the same conversation. Navigation commands (like `/agent show`, `/agent back`, `/agent status`) are planned but not yet implemented - for now, simply respond to the agent's prompts.

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
- ✗ Generate images directly (workers do that in future phases)
- ✗ Skip spawning the research worker
- ✗ Present options without spawning worker first
- ✗ Forget to save state after selection
- ✗ Move to Phase 1c (it's not implemented yet)

## Workflow Overview

```
User invokes: /agent brand "artisan coffee shop"
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
[Phase 1c: Logo Concepts - Not implemented yet]
    ↓
Complete
```

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
| `/agent show` | 📋 Planned | Redisplay current options at this phase |
| `/agent back` | 📋 Planned | Return to previous checkpoint |
| `/agent tweak "X"` | 📋 Planned | Refine current options with feedback |
| `/agent status` | 📋 Planned | Show current phase and all decisions made |
| `/agent help` | 📋 Planned | List available commands and current context |

**Legend:**
- ✓ Active - Fully implemented
- 📋 Planned - Documented but not implemented

## Phase 1a: Style Direction (ACTIVE)

This is the only phase currently active. Later phases (1b: Palette, 1c: Logo) are placeholders.

### Process Steps

When the skill is invoked with `/agent brand "description"`, follow these steps exactly:

**Quick Reference:**
1. Parse brand description and check for `--resume` flag
2. Spawn Task tool research worker with brand description
3. Parse worker output into 3 style directions
4. Present options to user in formatted list
5. Handle user selection (1/2/3/custom/refinement)
6. Save state to `.claude/local/agent-state.json`

**Detailed Steps:**

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

  [Phase 1c: Logo Concepts - coming soon]
  ```
- Proceed to save state (see State Save below)

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

       ✓ Phase 1b complete: Color palette chosen

       [Phase 1c: Logo Concepts - coming soon]

       When Phase 1c is implemented, I'll generate logo concepts using
       this palette and the Modern Minimal style.

       [Saves updated state]
```

## Phase 1c: Logo Concepts (PLACEHOLDER)

Not implemented yet. Future functionality:

- Brief logo concept worker on brand + style + palette
- Worker generates 3 logo concept descriptions
- For each concept, spawn image generation worker
- Present 3 visual options
- User selects or requests variations
- Checkpoint saved

### Logo Concept Worker Prompt Template (Future)

```
You are a logo concept designer. Create 3 distinct logo concepts for this brand:

Brand: [brand description]
Style: [selected direction]
Palette: [selected colors]

For each concept provide:
1. Concept name
2. Description of visual elements
3. Typography approach
4. How it embodies the brand

IMPORTANT: Describe concepts only. Do NOT generate images or spawn workers.
Return findings as natural language.
```

### Logo Generation Worker Prompt Template (Future)

```
You are an image generation specialist. Generate this logo concept:

Concept: [concept description from concept worker]
Style: [style direction]
Palette: [color palette]

Use the appropriate MCP image generation tool to create the logo.
Return the generated image path and a brief description of what was created.

IMPORTANT: You are a generation worker. Use ONLY image generation MCP tools.
Do NOT spawn other workers. Do NOT research or interact with user.
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
- Always use `subagent_type="general-purpose"` for research workers
- Always use `model="sonnet"` for consistency
- Embed all necessary context directly in the prompt string
- Include clear instructions about what the worker should NOT do

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

2. **Format for user presentation**
   - Use the format shown in Process Steps (Step 4 for Phase 1a, Step 10 for Phase 1b)
   - Keep it concise but complete
   - Maintain the user-friendly tone

3. **Validate completeness**
   - Did the worker provide all 3 options (directions or palettes)?
   - Does each option have all required elements?
   - For Phase 1b: Are hex codes in valid format (#RRGGBB)?
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
| Phase 1a selection confirmed | Use Bash tool to create `.claude/local/` (if needed), use Write tool to save full state |
| Phase 1b selection confirmed | Use Read tool to load current state, update `current_phase` to "1b_complete" and add `decisions.color_palette`, use Write tool to save |
| Phase 1c selection confirmed (future) | Use Read tool to load current state, update `current_phase` and `decisions`, use Write tool to save |
| Project completes | Use Bash tool to delete state file |
| User starts fresh | Use Bash tool to delete state file |

### State File Format

**After Phase 1a:**
```json
{
  "brand_description": "artisan coffee shop",
  "started": "2026-01-23T10:30:00Z",
  "current_phase": "1a_complete",
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

### How to Read State (Resume Flow)

In Step 1b of Process Steps (Phase 1a), **use the Read tool** to read `.claude/local/agent-state.json`:

- **If Read succeeds:** Parse the JSON content and extract the fields below
- **If Read returns an error:** The file doesn't exist; inform user no previous session found

Parse the JSON to extract:
- `brand_description` - Show to user for context
- `current_phase` - Determine where to resume
  - `"1a_complete"`: Resume from Phase 1b (palette generation)
  - `"1b_complete"`: Resume from Phase 1c (logo concepts - not yet implemented)
- `decisions.style_direction` - Show what's already been selected
- `decisions.color_palette` - Show if Phase 1b was completed
- `started` - Show how long ago the session started

**Resume Logic:**
- If `current_phase === "1a_complete"`: Proceed directly to Step 7 (Phase 1b)
- If `current_phase === "1b_complete"`: Inform user Phase 1c not yet implemented
- If phase is incomplete: Resume at the last incomplete phase

## Checkpoints

Checkpoints allow users to return to previous decisions:

| Checkpoint | Data Saved | Back Action |
|------------|------------|-------------|
| After style selection (Phase 1a) | Style direction + characteristics | Return to style options, allow re-selection |
| After palette selection (Phase 1b) | Palette name + colors with hex codes | Return to palette options, allow re-selection |
| After logo selection (Phase 1c - future) | Logo concept + image path | Return to logo options |

**Back Command (Future):**
```
User: /agent back

Agent: Returning to color palette selection.

       Previously selected: Earthy Contrast

       Here are all 3 palettes again:
       [Redisplays palette options]

       Select again or keep "Earthy Contrast"?
```

**Back to Earlier Phase (Future):**
```
User: /agent back to style

Agent: Returning to style direction selection.

       Previously selected: Modern Minimal

       Warning: Going back will clear your palette selection (Earthy Contrast).

       Here are all 3 style directions again:
       [Redisplays options]

       Select again or keep "Modern Minimal"?
```

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

## Extension Points

When implementing Phase 1c:

1. **Add logo concept worker prompt** (template already outlined above)
2. **Add logo generation worker prompt** (template already outlined above)
3. **Implement logo checkpoint save/load** (state file structure needs logo_concept field)
4. **Add navigation commands** (`/agent show`, `/agent back`, etc.)
5. **Parse logo outputs** from concept and generation workers
6. **Spawn image generation workers** for logo visuals
7. **Update error handling** for logo-specific worker types

The architecture is designed to extend naturally:
- Each phase follows the same pattern (research → present → select → checkpoint)
- Worker prompts are templates with clear boundaries
- State management is centralized
- Phase 1a and 1b demonstrate the full pattern

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
- Workers should not generate images (orchestrator spawns generation workers separately)
- Workers should not spawn sub-workers (flat hierarchy)
- Workers return findings to orchestrator, not to user directly

## Future Enhancements

Beyond Phase 1c:

- **Phase 2: Supporting Materials** - Business card, letterhead concepts
- **Phase 3: Digital Assets** - Social media templates, website hero
- **Export Package** - ZIP with all finals, style guide, asset log
- **Variation Generator** - Spawn workers to create 3 variations of any concept
- **Feedback Loop** - "Why did you choose X?" reflection prompts
