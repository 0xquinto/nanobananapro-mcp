---
name: agent-brand
description: Guided brand identity agent that orchestrates multi-step visual branding projects through research, exploration, and generation. Uses Task tool workers to research style directions, craft prompts, and generate images. Employs guided collaboration where the agent proposes options and users make decisions.
argument-hint: "brand description" [--resume]
---

# Agent: Brand Identity

Orchestrates complex brand identity projects through guided collaboration. This agent researches style directions, proposes visual options, and coordinates image generation workers - but never generates images directly. All generation is delegated to specialized Task tool workers.

## How to Use

**Starting a new project:**
```
/agent brand "description of your brand"
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

## Workflow Overview

```
User invokes: /agent brand "artisan coffee shop"
    ↓
Phase 1a: Brief Collection
    ↓
Spawn Research Worker (Task tool)
    ↓
Present 3 Style Directions
    ↓
User Selects Direction
    ↓
[Phase 1b: Color Palette - Not implemented yet]
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
| `/agent show` | 📋 Planned | Redisplay current options at this phase |
| `/agent back` | 📋 Planned | Return to previous checkpoint |
| `/agent tweak "X"` | 📋 Planned | Refine current options with feedback |
| `/agent status` | 📋 Planned | Show current phase and all decisions made |
| `/agent help` | 📋 Planned | List available commands and current context |
| `/agent resume` | 📋 Planned | Continue from saved state file |

**Legend:**
- ✓ Active - Fully implemented
- 📋 Planned - Documented but not implemented

## Phase 1a: Style Direction (ACTIVE)

This is the only phase currently active. Later phases (1b: Palette, 1c: Logo) are placeholders.

### Process

1. **Brief Collection**
   - User provides brand description: `/agent brand "artisan coffee shop"`
   - Agent acknowledges and prepares to research

2. **Style Research Worker**
   - Spawn Task tool with research prompt
   - Worker researches 3 distinct style directions
   - Each direction includes:
     - Name
     - Visual characteristics (colors, typography, elements)
     - Mood/emotion
     - Why it fits the brand
   - Worker returns natural language description

3. **Present Options**
   - Parse worker output
   - Display 3 directions clearly formatted
   - Offer choice or custom direction

4. **User Selection**
   - User picks a direction (1, 2, 3, or describes custom)
   - Agent confirms selection
   - Checkpoint saved (for future resume functionality)

### Research Worker Prompt Template

```
You are a style research specialist. Research 3 distinct visual style directions for this brand:

Brand: [user's brand description]

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

Return your findings as natural language that the orchestrator will parse and present.
```

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

       [Phase 1b: Color Palette - coming soon]
```

## Phase 1b: Color Palette (PLACEHOLDER)

Not implemented yet. Future functionality:

- Generate 3 palette variations within selected style
- Each palette: 5-6 colors with hex codes and usage guidance
- User selects preferred palette
- Checkpoint saved

### Palette Worker Prompt Template (Future)

```
You are a color palette specialist. Create 3 color palette variations
for this brand, within the [selected style] direction:

Brand: [brand description]
Style: [selected direction name and characteristics]

For each palette provide:
1. Palette name
2. 5-6 colors with hex codes
3. Usage notes (primary, accent, neutral, etc.)
4. Why this palette works for the brand

Make the 3 palettes distinct but all aligned with the style direction.

IMPORTANT: You are a research worker. Do NOT generate images or spawn other workers.
Return findings as natural language.
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

### Spawning a Worker

```python
# Orchestrator spawns a worker via Task tool
Task(
  prompt=worker_prompt_template.format(
    brand=user_brand_description,
    context=additional_context
  ),
  restrictions="advisory: do not generate images, do not spawn workers"
)
```

### Parsing Worker Output

Workers return natural language. Orchestrator must parse:
- Extract structured information (direction names, characteristics)
- Format for user presentation
- Validate completeness (did worker provide all requested elements?)

### Error Handling

| Worker Issue | Orchestrator Response |
|--------------|----------------------|
| Worker returns incomplete data | Re-spawn with clarified prompt |
| Worker violates restrictions (tries to generate) | Ignore invalid actions, parse valid output |
| Worker fails entirely | Report to user, offer to retry or manual input |

## State Management (Future)

Not fully implemented yet. When implemented:

**State File:** `.claude/local/agent-state.json`

```json
{
  "brand_description": "artisan coffee shop",
  "started": "2026-01-23T10:30:00Z",
  "current_phase": "1b",
  "decisions": {
    "style_direction": {
      "name": "Modern Minimal",
      "characteristics": "...",
      "selected_at": "2026-01-23T10:32:00Z"
    },
    "color_palette": null,
    "logo_concept": null
  },
  "worker_outputs": {
    "style_research": "...",
    "palette_research": null
  }
}
```

**Usage:**
- Created when Phase 1a begins
- Updated after each checkpoint
- Read on `--resume` to continue
- Deleted when project completes

## Checkpoints

Checkpoints allow users to return to previous decisions:

| Checkpoint | Data Saved | Back Action |
|------------|------------|-------------|
| After style selection | Style direction + characteristics | Return to style options, allow re-selection |
| After palette selection | Palette + hex codes | Return to palette options |
| After logo selection | Logo concept + image path | Return to logo options |

**Back Command (Future):**
```
User: /agent back

Agent: Returning to style direction selection.

       Previously selected: Modern Minimal

       Here are all 3 directions again:
       [Redisplays options]

       Select again or keep "Modern Minimal"?
```

## Error Handling

| Situation | Agent Response |
|-----------|----------------|
| Empty brand description | "Please describe your brand. What does [business name] do? Who is it for?" |
| Worker returns invalid output | Re-spawn with clarified prompt, limit 2 retries |
| User provides unclear selection | "Did you mean option [N]? Or would you like something different?" |
| State file corrupted (future) | Start fresh, offer to import previous decisions manually |
| All phases complete | "Brand identity complete! Summary: [recap all decisions]" |

## Examples

### Complete Phase 1a Flow

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

```
User: /agent status

Agent: ## Brand Identity Progress

       **Brand:** Boutique yoga studio focused on mindfulness
       **Started:** 2026-01-23 at 10:30 AM
       **Current Phase:** 1a complete, 1b pending

       **Decisions Made:**
       ✓ Style Direction: Serene Minimalist (Warm)
         - Warm whites, soft beige, pale peach accents
         - Generous space, simple line art
         - Rounded sans-serif fonts

       **Next Steps:**
       Phase 1b will generate color palette options (not implemented yet)

       Use `/agent show` to review current options
       Use `/agent back` to change previous decisions
```

### Resuming (Future)

```
User: /agent resume

Agent: Found previous brand identity session from 2 hours ago.

       **Brand:** Artisan coffee shop
       **Last Phase:** 1a complete (Style: Modern Minimal selected)

       Continue from Phase 1b: Color Palette? (yes / start fresh)

User: yes

Agent: Resuming from Phase 1b.

       Selected style: Modern Minimal (clean lines, muted earth tones,
       geometric shapes, sans-serif fonts)

       [Would spawn palette worker - not implemented yet]

       Phase 1b coming soon. For now, session restored but can't proceed further.
```

## Extension Points

When implementing Phase 1b and 1c:

1. **Add worker prompt templates** (already outlined above)
2. **Implement checkpoint save/load** (state file structure defined)
3. **Add navigation commands** (`/agent show`, `/agent back`, etc.)
4. **Parse palette and logo outputs** from workers
5. **Spawn image generation workers** for logo concepts
6. **Update error handling** for new worker types

The architecture is designed to extend naturally:
- Each phase follows the same pattern (research → present → select → checkpoint)
- Worker prompts are templates with clear boundaries
- State management is centralized

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
