---
name: quickstart
description: Guided introduction to image generation skills. Use when user is new,
  asks "how do I start?", "what can you do with images?", or invokes /quickstart.
  Routes to appropriate skill based on user goals.
argument-hint: ""
---

# Quickstart

Interactive onboarding for new users. Explains capabilities and routes to the right skill.

## When This Skill Activates

- User invokes `/quickstart`
- User asks: "how do I start?", "what can you do?", "help with images"
- First-time detection (no `style-library.md` or projects found)

## Flow

### Step 1: Welcome Message

Display:

```
## Welcome to Image Generation

I can help you create images using AI. Here's what's possible:

**Quick Generation** — Describe an idea, I'll enhance it and generate
**Visual Projects** — Set up brand/campaign/character projects with consistency
**Style Capture** — Extract styles from references and reuse them
**Prompt Improvement** — Analyze and fix underperforming prompts

What would you like to do?
```

### Step 2: Route Based on Response

| User Intent | Route To | Suggested Command |
|-------------|----------|-------------------|
| "generate an image" / "make something" | image-prompt | `/image-prompt [their idea]` |
| "start a project" / "brand work" | project-setup | `/project-setup` |
| "improve my prompt" / "why isn't this working" | prompt-anatomy | `/prompt-anatomy [their prompt]` |
| "extract style from reference" | capture-trends | `/capture-trends [path]` |
| "what styles do I have" | style-library | `/style-library list` |

### Step 3: Guided First Generation

If user chooses "generate an image":

1. Ask: "What do you want to create? (Describe in a few words)"
2. Take their response and invoke `/image-prompt` with it
3. After generation, show: "Nice! Here are some next steps:"
   - "Refine this image — just describe changes"
   - "Start a project for multiple related images → `/project-setup`"
   - "Save this style for reuse → `/capture-trends [output-path]`"

### Step 4: Success Confirmation

After first successful action:

```
## You're Set Up!

**Quick reference:**
- `/image-prompt [idea]` — Generate images
- `/enhance-prompt [text]` — Improve a prompt
- `/style-library list` — See saved styles
- `/project-setup` — Start a new project

**Pro tip:** Use `--chat` for iterative refinement:
`/image-prompt fantasy landscape --chat`
```

## First-Run Detection

Suggest quickstart if:
- No `style-library.md` in current directory or root
- No project directories detected
- User's first image-related request in session

Detection message:
> "Looks like you're just getting started! Want a quick walkthrough? (`/quickstart`)"

## Error Handling

| Situation | Response |
|-----------|----------|
| User unclear | Offer multiple choice: "Are you trying to: generate an image / set up a project / improve a prompt?" |
| User asks about capabilities | Show full skill list with one-line descriptions |
| User wants to skip | "No problem! Just use `/image-prompt [your idea]` anytime." |

## Integration

This skill is an entry point that routes to other skills. It does not call MCP tools directly.
