# Gemini Image Generation Patterns

Reference for patterns specific to Gemini 3 Pro vs. universal image generation best practices.

## Gemini-Specific Patterns

These patterns are optimized for or unique to Gemini 3 Pro:

### Aspect Ratio Handling

| Pattern | Gemini Behavior | Universal Equivalent |
|---------|-----------------|---------------------|
| Exact ratios only | Gemini requires exact values: 1:1, 16:9, etc. | Some models accept approximate |
| 21:9 ultrawide | Supported natively | Often requires workarounds |

### Prompt Structure

| Pattern | Gemini Preference | Notes |
|---------|-------------------|-------|
| Natural prose | Preferred over keyword lists | Gemini responds better to flowing sentences |
| Negative prompts | Not supported | Use positive framing instead |
| Quality keywords | Generally ignored | "8K, masterpiece" has no effect |
| Concrete details | Highly effective | Specific > generic always |

### Multi-Turn Sessions

| Pattern | Gemini Behavior |
|---------|-----------------|
| Context retention | Full history maintained within session |
| Image reference | Previous images available for editing |
| Style drift | Minimal across turns |

### Search-Grounded Generation

Gemini-exclusive feature. No universal equivalent.

| Use Case | Effectiveness |
|----------|---------------|
| Current weather | High |
| Recent events | Medium (depends on indexing) |
| Stock data | Medium |
| Historical facts | High |

## Universal Patterns

These patterns work across all major image models (Gemini, DALL-E, Midjourney, Stable Diffusion):

### The 6-Element Formula

| Element | Universal Effectiveness |
|---------|------------------------|
| Subject | High across all models |
| Composition | High (shot types, angles) |
| Action | High |
| Location | High |
| Style | Medium (model-dependent interpretation) |
| Constraints | Low (each model handles differently) |

### Effective Techniques

| Technique | Universality |
|-----------|--------------|
| Specific subjects | Universal |
| Named art styles | Universal (varies by training data) |
| Lighting descriptions | Universal |
| Camera terminology | Universal |
| Era/period references | Universal |

### Ineffective Techniques

| Technique | Why It Fails |
|-----------|--------------|
| "4K, 8K, HD" | Ignored by most models |
| "trending on ArtStation" | Overfit, unpredictable |
| "masterpiece, best quality" | Generic, no effect |
| Excessive adjectives | Dilutes focus |

## Model-Specific Notes

### vs. DALL-E 3

| Aspect | Gemini | DALL-E 3 |
|--------|--------|----------|
| Negative prompts | Not supported | Not supported (use positive framing) |
| Text in images | Limited | Better |
| Photorealism | Strong | Strong |

### vs. Midjourney

| Aspect | Gemini | Midjourney |
|--------|--------|------------|
| Parameter syntax | Natural language | `--ar`, `--v`, etc. |
| Style control | Via prose | Via `--style` |
| Variations | Via chat session | Built-in variation UI |

### vs. Stable Diffusion

| Aspect | Gemini | SD |
|--------|--------|-----|
| Negative prompts | Not supported | Critical |
| CFG scale | Not exposed | User-controlled |
| Steps | Not exposed | User-controlled |
