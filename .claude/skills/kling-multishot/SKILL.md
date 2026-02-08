---
name: kling-multishot
description: Use when the user wants to create a multi-shot video using Kling 3.0 and NBP image generation. Orchestrates a two-phase pipeline — intake (interactive interview + planning) then execution (asset generation + Kling guidance).
---

# Kling 3.0 Multi-Shot Pipeline

## Overview

You are the lead agent orchestrating a Kling 3.0 multi-shot filmmaking pipeline. You run two phases sequentially — intake (collect creative variables with deep user engagement) then execution (generate assets + Kling prompts). You run character design directly (no spawned agents for that step). You spawn teammates only for stages that don't require interactive user loops.

## Architecture

```
You (lead — this session)
  ├── TeamCreate("kling-intake")
  │     ├── Task: source-digester      (Stage 0 — source analysis + extraction)
  │     ├── You: ambiguity resolution  (between Stage 0 and Stage 1)
  │     ├── Task: story-architect       (Stage 1 — receives synthetic Q1)
  │     ├── You: character design       (Stage 2 — lead-driven, sequential, visual)
  │     ├── Task: shot-planner          (Stage 3 — collaborative with user)
  │     └── Task: intake-reviewer       (Stage 4 — assembly + validation)
  ├── TeamDelete("kling-intake")
  │
  ├── TeamCreate("kling-execution")
  │     ├── Task: ref-generator-X       (Phase 1, one per character, uses concept images)
  │     ├── Task: env-generator         (Phase 2, parallel with Phase 1)
  │     ├── Task: hero-composer         (Phase 3, if multi-character)
  │     ├── Task: frame-generator       (Phase 4, parallel with Phases 1+2)
  │     ├── Task: shot-prompter         (Phase 5)
  │     └── You guide Kling Phase 6 directly
  └── TeamDelete("kling-execution")
```

Key differences from previous version:
- **No visual-director agent** — visual language is part of Stage 1
- **No spawned character-designer agents** — lead runs character design directly with concept image generation
- **Multi-sequence support** — videos > 8s are planned as multiple Kling sequences
- **More user interaction** — shot planning is collaborative, not autonomous

All teammates are leaf workers — they do NOT create teams or spawn agents.

## Full Lifecycle

### Phase A: Intake

**Step 1** — Create intake team:
```
TeamCreate({ team_name: "kling-intake", description: "Collect variables for Kling 3.0 multi-shot workflow" })
```

**Step 2** — Spawn Stage 0 (source-digester):
```
Task({
  team_name: "kling-intake",
  name: "source-digester",
  subagent_type: "general-purpose",
  prompt: "[Read skill: .claude/skills/kling-source-digester/SKILL.md] + [user's opening message]"
})
```
The source-digester analyzes the input, extracts variables, self-validates via `validate_intake_digest`, and writes `scratchpad/intake/stage0-source-digest.md`.

**Step 3** — Read Stage 0 output. If ambiguities exist, present them to the user grouped by priority:
  1. Characters (who appears)
  2. Scope (duration, format)
  3. Creative choices (tone, pacing, sonic)
Use AskUserQuestion with the ambiguity options as multiple-choice.

**Step 4** — Construct synthetic Q1 message from digest extracted fields + user's ambiguity resolutions. Format as a natural user brief:

  "I want to make a [output_format] based on [source_reference].
   Genre: [genre]. Tone: [tone].
   The audience should feel [emotional_core]...
   Characters: [list]...
   Locations: [list]...
   [For needs_interview items:] I haven't decided on [field] yet — please ask me about it."

**Step 5** — Spawn Stage 1 (story-architect) with synthetic Q1 as the user's opening message:
```
Task({
  team_name: "kling-intake",
  name: "story-architect",
  subagent_type: "general-purpose",
  prompt: "[Read skill: .claude/skills/kling-story-architect/SKILL.md] + [synthetic Q1 message]"
})
```
The story-architect's existing confirm-if-stated logic handles pre-filled values. It interviews only for `needs_interview` gaps. Writes `scratchpad/intake/stage1-story-foundation.md`.

**Step 6** — Read Stage 1 output. Extract `character_count`, `character_names`, `production` parameters, `visual_language`, flags.

**Step 7** — Run Stage 2: Character Design (LEAD-DRIVEN, SEQUENTIAL)

Read the character designer protocol: `.claude/skills/kling-character-designer/SKILL.md`

You run this directly — do NOT spawn character-designer agents. For each character in `character_names`, follow the protocol:

```
For each character (one at a time, sequentially):
  1. Propose text design (appearance, costume, distinguishing elements)
     - Reference locked concept images from prior characters for cohesion
  2. User reviews and approves/tweaks text
  3. Generate concept image with NBP:
     mcp__nanobananapro__generate_image({
       prompt: "[character description prompt]",
       aspect_ratio: "1:1",
       resolution: "1K",
       model: "pro"
     })
  4. User reviews concept image
  5. If not right → adjust description, regenerate (max 3 iterations per character)
  6. If approved → write stage2-character-{name}.md, move to next character
```

Each character file includes `concept_image_path` pointing to the approved concept image.

**Step 8** — Spawn Stage 3 (shot-planner). Blocked by: Stage 1 + all Stage 2 characters locked.
```
Task({
  team_name: "kling-intake",
  name: "shot-planner",
  subagent_type: "general-purpose",
  prompt: "[Read skill: .claude/skills/kling-shot-planner/SKILL.md] + [Stage 1 data] + [all Stage 2 data]"
})
```
The shot-planner MUST interview the user about structure and pacing before generating. For multi-sequence videos, it plans one sequence at a time with user approval.

**Step 9** — Wait for Stage 3 to complete. Spawn Stage 4 (intake-reviewer).
```
Task({
  team_name: "kling-intake",
  name: "intake-reviewer",
  subagent_type: "general-purpose",
  prompt: "[Read skill: .claude/skills/kling-intake-reviewer/SKILL.md] + [all stage output files]"
})
```

**Step 10** — Intake-reviewer presents brief, gets user approval. Read approved `final-intake-document.md`.

**Step 11** — Shut down intake agents (reverse dependency order):
```
SendMessage({ type: "shutdown_request", recipient: "intake-reviewer" })
SendMessage({ type: "shutdown_request", recipient: "shot-planner" })
SendMessage({ type: "shutdown_request", recipient: "story-architect" })
SendMessage({ type: "shutdown_request", recipient: "source-digester" })
```
Note: No character-designer or visual-director agents to shut down (lead ran those directly).

**Step 12** — Delete intake team:
```
TeamDelete()
```

### Intake Dependency Graph

```
Stage 0 (source-digester)             — spawned agent
  └──→ Lead: ambiguity resolution     — lead-driven, interactive
        └──→ Stage 1 (story-architect) — spawned agent, receives synthetic Q1
              └──→ Stage 2 (character design)     — lead-driven, sequential
                    └──→ Stage 3 (shot-planner)   — spawned agent, collaborative
                          └──→ Stage 4 (intake-reviewer)  — spawned agent
```

All stages are sequential. No parallel intake agents.

### Phase B: Execution

**Step 13** — Create execution team:
```
TeamCreate({ team_name: "kling-execution", description: "Generate NBP assets and Kling prompts" })
```

**Step 14** — Spawn Phase 1 + Phase 2 + Phase 4 in PARALLEL:

For each character (concept images from intake serve as visual anchors):
```
Task({
  team_name: "kling-execution",
  name: "ref-generator-{name}",
  subagent_type: "general-purpose",
  prompt: "[Read skill: .claude/skills/kling-ref-generator/SKILL.md] + [character data from intake including concept_image_path] + [visual_language]"
})
```

```
Task({
  team_name: "kling-execution",
  name: "env-generator",
  subagent_type: "general-purpose",
  prompt: "[Read skill: .claude/skills/kling-env-generator/SKILL.md] + [scene data from intake]"
})
```

```
Task({
  team_name: "kling-execution",
  name: "frame-generator",
  subagent_type: "general-purpose",
  prompt: "[Read skill: .claude/skills/kling-frame-generator/SKILL.md] + [shot_plan + characters + visual_language from intake]"
})
```

**Step 15** — Wait for Phase 1 + Phase 2. IF multi-character, spawn Phase 3:
```
Task({
  team_name: "kling-execution",
  name: "hero-composer",
  subagent_type: "general-purpose",
  prompt: "[Read skill: .claude/skills/kling-hero-composer/SKILL.md] + [all Phase 1+2 image refs] + [multi_character positions]"
})
```
IF single character, skip Phase 3 — use the character reference as hero image.

**Step 16** — Wait for Phase 3 (or skip) + Phase 4. Spawn Phase 5:
```
Task({
  team_name: "kling-execution",
  name: "shot-prompter",
  subagent_type: "general-purpose",
  prompt: "[Read skill: .claude/skills/kling-shot-prompter/SKILL.md] + [entire intake doc] + [all asset refs from Phases 1-4]"
})
```

**Step 17** — Assemble deliverables. Present Review Gate (see below).

**Step 18** — Iteration loop if user requests changes.

**Step 19** — User approves. Guide Kling Phase 6 directly (see below).

**Step 20** — Shut down execution agents (reverse order).

**Step 21** — Delete execution team.

**Step 22** — Session complete.

## Review Gate

After Phase 5 completes, run the validation checklist, then present:

### Validation Checklist

Before presenting assets, verify:

- [ ] Image format is PNG
- [ ] Resolution >= 1080p (2K or 4K preferred)
- [ ] Aspect ratio matches the intended Kling generation setting
- [ ] Characters are visually consistent across all references (if multi-character)
- [ ] Characters match their approved concept images from intake
- [ ] Lighting direction is consistent across all references
- [ ] Start/end frames match the scene environment of the main reference image
- [ ] Character descriptions used in prompts are identical across all related generations
- [ ] Camera/lens language in NBP prompts is compatible with Kling shot prompts
- [ ] Multi-sequence continuity: end frames connect to next sequence start frames

Write validated results to `scratchpad/execution/deliverables-summary.md`.

### Presentation

For single-sequence videos:

```
## Your Assets Are Ready

### Character References
- **[NAME]**: [image path] -- [framing], [view_angle], [lighting]
  Concept match: [yes/no]

### Scene Environment
- [image path] -- [environment description]

### Hero Reference (for Kling upload)
- [image path] -- composite of characters in scene
  (or single character ref if only one character)

### Start Frame
- [image path] -- [start_frame.action_state]

### End Frame
- [image path] -- [end_frame.action_state]

### Kling Shot Prompts
[formatted prompts ready to copy-paste]

---
**Review these assets. Tell me:**
- "Looks good" to proceed to Kling
- "Change [X]" for specific adjustments
- "Redo [character/scene]" to regenerate from scratch
```

For multi-sequence videos, present assets per sequence with clear labeling.

### Routing Feedback

| Feedback | Action |
|----------|--------|
| "Looks good" | Proceed to Kling Phase 6 |
| "Change lighting on [character]" | `edit_image` directly (no agent needed) |
| "[Character]'s costume isn't right" | Re-spawn `ref-generator-{name}` with updated description |
| "The whole vibe is wrong" | Update visual_language, re-spawn ALL ref-generators + env-generator + hero-composer + frame-generator |
| "Add another shot" | Update shot_plan, re-spawn shot-prompter |
| "Start frame pose is wrong" | Re-spawn frame-generator |
| "Doesn't match the concept image" | Re-spawn ref-generator with stronger concept image anchoring |

## Kling Phase 6 — Direct Guidance

You handle this directly (no teammate).

### Single-Sequence Videos

1. "Upload this hero reference image: {path}"
2. "Click **Multi-cam** to enable multi-shot mode"
3. "Paste these shot prompts:" (present each with duration)
4. "Enable **Bind elements to enhance consistency**"
5. "Upload start frame: {path} and end frame: {path}"
6. "Set resolution to 1080p, enable Native Audio"
7. "Generate and review 4 variations"

### Multi-Sequence Videos

For each sequence:
1. "**Sequence [N] of [TOTAL]** — [NARRATIVE_BEAT]"
2. "Upload hero reference: {path}"
3. "Paste these shot prompts for sequence [N]:" (present each with duration)
4. "Upload start frame: {path} and end frame: {path}"
5. "Generate and review"
6. "Save the best variation, then we'll set up the next sequence"

After all sequences:
7. "Use Kling's video extension or your editor to stitch sequences together"

### Post-Production

- If dialogue -> apply Lip Sync
- If stills needed -> Extract Frame
- If further editing -> Create in Omni
- If multi-sequence -> stitch in editor, match transitions

## Dynamic Scaling

| Condition | Intake | Execution |
|-----------|--------|-----------|
| 1 character | Lead designs 1 character with concept image | 1 ref-generator (with concept anchor). Skip hero-composer. |
| N characters | Lead designs N characters sequentially with concept images | N ref-generators (parallel, each with concept anchor) + hero-composer |
| dialogue_scene | Force view_angle constraints during character design | Ensure face visibility in refs |
| complex_design | Flag during character design | ref-generator uses start_image_chat |
| multi_scene | Lead asks about outfit variants during character design | Extra ref-generator tasks per variant |
| 8s video | 1 sequence planned | 1 Kling Multi-Cam generation |
| 15-30s video | 2-4 sequences planned | 2-4 Kling Multi-Cam generations, stitched |
| 60s+ video | 6+ sequences planned | 6+ Kling Multi-Cam generations, stitched |
| New character mid-intake | Lead designs additional character (sequential) | Spawn additional ref-generator, re-run hero-composer |

## Failure Handling

| Failure | Response |
|---------|----------|
| Agent times out | Check task status. Re-spawn with same name and prompt. |
| Agent produces invalid output | Read partial output, identify gaps. Send message or re-spawn. |
| Agent marks complete but output missing | Re-spawn agent. |
| Multiple agents conflict | Read both outputs, merge or re-run one. |
| Concept image generation fails | Retry with adjusted prompt. If persistent, skip concept image and note for ref-generator. |
| User rejects concept image 3+ times | Suggest a completely different direction or let user describe more specifically. |

## Scratchpad File Layout

```
scratchpad/
  intake/
    stage0-source-digest.md          # source analysis + extraction
    stage1-story-foundation.md       # project, production, scene, visual_language, flags
    stage2-character-{name}.md       # per character (includes concept_image_path)
    stage3-shot-plan.md              # sequences with shots
    final-intake-document.md         # assembled by intake-reviewer
  execution/
    ref-character-{name}.md          # production references (anchored to concept images)
    ref-environment.md
    ref-hero-composite.md
    ref-start-frame.md
    ref-end-frame.md
    kling-shot-prompts.md
    deliverables-summary.md
```
