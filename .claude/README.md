# .claude Directory

Claude Code configuration for the nanobananapro-mcp project.

## Structure

```
.claude/
├── skills/                  # Image generation workflow skills
│   ├── README.md            # Full skill documentation
│   ├── image-prompt/        # Primary generation skill
│   ├── enhance-prompt/      # Prompt improvement
│   ├── moodboard/           # Learn design through moodboards
│   ├── taste-check/         # Cliché and quality analysis
│   ├── prompt-anatomy/      # Structural analysis
│   ├── style-library/       # Preset management
│   ├── capture-trends/      # Extract styles from references
│   ├── project-setup/       # Scaffold projects
│   └── quickstart/          # New user onboarding
├── hooks/                   # Pre/post tool hooks
│   ├── check-style-guide-lock.sh
│   ├── protect-finals.sh
│   └── log-generated-image.sh
├── gemini-patterns.md       # Model-specific prompt patterns
├── settings.json            # Hook configuration (checked in)
└── settings.local.json      # Local overrides (git-ignored)
```

## Skills

See [skills/README.md](skills/README.md) for full documentation.

| Skill | Command | Purpose |
|-------|---------|---------|
| image-prompt | `/image-prompt` | Generate images from concepts |
| enhance-prompt | `/enhance-prompt` | Improve naive prompts |
| moodboard | `/moodboard` | Learn design through moodboard creation |
| taste-check | `/taste-check` | Detect clichés and quality issues |
| prompt-anatomy | `/prompt-anatomy` | Analyze prompt structure |
| style-library | `/style-library` | Manage style presets |
| capture-trends | `/capture-trends` | Extract styles from references |
| project-setup | `/project-setup` | Scaffold visual projects |
| quickstart | `/quickstart` | New user onboarding |

## Hooks

Hooks enforce project conventions automatically.

| Hook | Event | Purpose |
|------|-------|---------|
| `check-style-guide-lock.sh` | PreToolUse (Edit/Write) | Block edits to locked style-guide.md |
| `protect-finals.sh` | PreToolUse (Edit/Write) | Prevent modification of outputs/finals/ |
| `log-generated-image.sh` | PostToolUse (image MCP tools) | Auto-log generated images to asset-log.md |

## Configuration

- **settings.json** - Shared hook configuration (checked into git)
- **settings.local.json** - Personal overrides (git-ignored)

To disable hooks locally, create `settings.local.json`:

```json
{
  "hooks": {
    "PreToolUse": [],
    "PostToolUse": []
  }
}
```
