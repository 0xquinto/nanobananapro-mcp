# MCP Output Handling Notes

Investigation notes from enhance-prompt skill testing session.

---

## Issue: Large Output Handling (RESOLVED)

When `generate_image` returns, the base64 image data causes the result to exceed Claude Code's token limit.

### What Happened

1. **Tool call**: `mcp__nanobananapro__generate_image` with prompt, model, aspect_ratio, resolution
2. **Result**: Error - "result (3,890,238 characters) exceeds maximum allowed tokens"
3. **Root cause**: Base64 encoding was always included, even when `output_path` was provided

### Solution Implemented

Modified `_result_to_dict` in `server.py` to conditionally include base64:

- **With `output_path`**: Saves file, returns `saved_path` only (response ~100 bytes)
- **Without `output_path`**: Returns `image_base64` (original behavior)

### Usage

Always provide `output_path` when calling image generation tools:

```python
generate_image(
    prompt="...",
    output_path="/path/to/output/image.jpg"
)
```

Response will be:
```json
{
  "text": "optional model commentary",
  "image_base64": null,
  "mime_type": "image/jpeg",
  "saved_path": "/absolute/path/to/output/image.jpg"
}
```

---

## Session Details

- Date: 2026-01-21
- Issue discovered during: enhance-prompt skill testing
- Fix commit: [see git log]
