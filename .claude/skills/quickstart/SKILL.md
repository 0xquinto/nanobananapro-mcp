---
name: quickstart
description: Guided introduction to image generation skills. Use when user is new,
  asks "how do I start?", "what can you do with images?", or invokes /quickstart.
  Routes to appropriate skill based on user goals.
argument-hint: ""
---

# Quickstart

Interactive onboarding that routes users to the right skill.

## Welcome Message

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

## Routing Table

| User Intent | Skill | Command |
|-------------|-------|---------|
| "generate an image", "make something" | image-prompt | `/image-prompt [idea]` |
| "start a project", "brand work" | project-setup | `/project-setup` |
| "improve my prompt", "why isn't this working" | prompt-anatomy | `/prompt-anatomy [prompt]` |
| "extract style from reference" | capture-trends | `/capture-trends [path]` |
| "what styles do I have" | style-library | `/style-library list` |

## First Generation Flow

When user wants to generate an image:
1. Ask what they want to create
2. Invoke `/image-prompt` with their response
3. After success, offer next steps: refine the image, start a project (`/project-setup`), or save the style (`/capture-trends`)

## Success Confirmation

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

Suggest `/quickstart` when no `style-library.md` or project directories exist, or on the user's first image request in a session.

Detection message: "Looks like you're just getting started! Want a quick walkthrough? (`/quickstart`)"

## Error Handling

| Situation | Response |
|-----------|----------|
| User unclear | Offer choices: generate / project / improve prompt |
| Asks about capabilities | Show skill list with descriptions |
| Wants to skip | "No problem! Use `/image-prompt [idea]` anytime." |

## Note

This skill routes to other skills. It does not call MCP tools directly.
