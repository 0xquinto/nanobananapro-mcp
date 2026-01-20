"""Utility functions for image encoding and validation."""

import base64
from pathlib import Path

VALID_ASPECT_RATIOS = [
    "1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"
]

VALID_RESOLUTIONS = ["1K", "2K", "4K"]

MODEL_ALIASES = {
    "flash": "gemini-2.5-flash-image",
    "pro": "gemini-3-pro-image-preview",
    "nano-banana": "gemini-2.5-flash-image",
    "nano-banana-pro": "gemini-3-pro-image-preview",
}

VALID_MODELS = [
    "gemini-2.5-flash-image",
    "gemini-3-pro-image-preview",
]


def encode_image_to_base64(image: bytes | str | Path) -> str:
    """Encode image bytes or file path to base64 string."""
    if isinstance(image, (str, Path)):
        image_bytes = Path(image).read_bytes()
    else:
        image_bytes = image
    return base64.b64encode(image_bytes).decode("utf-8")


def decode_base64_to_bytes(data: str) -> bytes:
    """Decode base64 string to bytes."""
    return base64.b64decode(data)


def validate_aspect_ratio(ratio: str | None) -> str:
    """Validate aspect ratio, returning default if None."""
    if ratio is None:
        return "1:1"
    if ratio not in VALID_ASPECT_RATIOS:
        raise ValueError(
            f"Invalid aspect ratio: {ratio}. "
            f"Must be one of: {', '.join(VALID_ASPECT_RATIOS)}"
        )
    return ratio


def validate_resolution(resolution: str | None, model: str) -> str:
    """Validate resolution for the given model."""
    if resolution is None:
        return "1K"
    if resolution not in VALID_RESOLUTIONS:
        raise ValueError(
            f"Invalid resolution: {resolution}. "
            f"Must be one of: {', '.join(VALID_RESOLUTIONS)}"
        )
    # Flash model only supports 1K
    if model == "gemini-2.5-flash-image" and resolution != "1K":
        return "1K"
    return resolution


def validate_model(model: str) -> str:
    """Validate and resolve model name/alias."""
    # Check aliases first
    if model.lower() in MODEL_ALIASES:
        return MODEL_ALIASES[model.lower()]
    # Check full model names
    if model in VALID_MODELS:
        return model
    raise ValueError(
        f"Invalid model: {model}. "
        f"Must be one of: {', '.join(VALID_MODELS)} "
        f"or aliases: {', '.join(MODEL_ALIASES.keys())}"
    )
