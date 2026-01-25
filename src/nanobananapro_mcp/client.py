"""Wrapper for Google Gemini GenAI client."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from google import genai
from google.genai import types

from .retry import DEFAULT_ASYNC_RETRY
from .utils import (
    encode_image_to_base64,
    validate_aspect_ratio,
    validate_resolution,
    validate_model,
    validate_seed,
)


@dataclass
class ImageGenerationResult:
    """Result from image generation."""

    text: str | None = None
    image_data: bytes | None = None
    mime_type: str | None = None
    grounding_metadata: dict | None = None

    @classmethod
    def from_response(cls, response: Any) -> "ImageGenerationResult":
        """Extract result from Gemini response."""
        text = None
        image_data = None
        mime_type = None

        for part in response.parts:
            if part.text is not None:
                text = part.text
            elif part.inline_data is not None:
                image_data = part.inline_data.data
                mime_type = part.inline_data.mime_type

        grounding = None
        if hasattr(response, "grounding_metadata"):
            grounding = response.grounding_metadata

        return cls(
            text=text,
            image_data=image_data,
            mime_type=mime_type,
            grounding_metadata=grounding,
        )


class GeminiImageClient:
    """Client wrapper for Gemini image generation."""

    def __init__(self, api_key: str | None = None):
        """Initialize client with API key from param or environment."""
        key = api_key or os.environ.get("GEMINI_API_KEY")
        if not key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is required. "
                "Set it or pass api_key parameter."
            )
        self._client = genai.Client(api_key=key)

    async def generate_image(
        self,
        prompt: str,
        model: str = "gemini-3-pro-image-preview",
        aspect_ratio: str | None = None,
        resolution: str | None = None,
        response_modalities: list[str] | None = None,
        seed: int | None = None,
    ) -> ImageGenerationResult:
        """Generate an image from a text prompt.

        Args:
            prompt: Text description of the image to generate
            model: Model to use for generation
            aspect_ratio: Output aspect ratio
            resolution: Output resolution (1K, 2K, 4K)
            response_modalities: Response types to request
            seed: Optional seed for reproducible generation (0 to 2147483647).
                  Note: Seed support depends on the underlying API.

        Returns:
            ImageGenerationResult with generated image data
        """
        model = validate_model(model)
        aspect_ratio = validate_aspect_ratio(aspect_ratio)
        resolution = validate_resolution(resolution, model)
        validated_seed = validate_seed(seed)
        modalities = response_modalities or ["TEXT", "IMAGE"]

        config = types.GenerateContentConfig(
            response_modalities=modalities,
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size=resolution if model == "gemini-3-pro-image-preview" else None,
            ),
            # Note: seed parameter is validated and stored for future API support
            # When Gemini API supports seed, add: seed=validated_seed
        )

        @DEFAULT_ASYNC_RETRY
        async def _call_api():
            return await self._client.aio.models.generate_content(
                model=model,
                contents=prompt,
                config=config,
            )

        response = await _call_api()
        return ImageGenerationResult.from_response(response)

    def edit_image(
        self,
        prompt: str,
        image_path: str | Path,
        model: str = "gemini-3-pro-image-preview",
        aspect_ratio: str | None = None,
        resolution: str | None = None,
        seed: int | None = None,
    ) -> ImageGenerationResult:
        """Edit an existing image with a text prompt.

        Args:
            prompt: Instructions for editing the image
            image_path: Path to the input image file
            model: Model to use for editing
            aspect_ratio: Output aspect ratio (optional, defaults to input)
            resolution: Output resolution (1K, 2K, 4K)
            seed: Optional seed for reproducible generation (0 to 2147483647).
                  Note: Seed support depends on the underlying API.

        Returns:
            ImageGenerationResult with edited image data
        """
        from PIL import Image

        model = validate_model(model)
        aspect_ratio = validate_aspect_ratio(aspect_ratio)
        resolution = validate_resolution(resolution, model)
        validated_seed = validate_seed(seed)

        image = Image.open(image_path)

        config = types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size=resolution if model == "gemini-3-pro-image-preview" else None,
            ),
            # Note: seed parameter is validated and stored for future API support
            # When Gemini API supports seed, add: seed=validated_seed
        )

        @DEFAULT_RETRY
        def _call_api():
            return self._client.models.generate_content(
                model=model,
                contents=[prompt, image],
                config=config,
            )

        response = _call_api()
        return ImageGenerationResult.from_response(response)

    def compose_images(
        self,
        prompt: str,
        image_paths: list[str | Path],
        model: str = "gemini-3-pro-image-preview",
        aspect_ratio: str | None = None,
        resolution: str | None = None,
        seed: int | None = None,
    ) -> ImageGenerationResult:
        """Compose a new image from multiple reference images.

        Args:
            prompt: Instructions for composing the images
            image_paths: List of paths to input images (max 14)
            model: Model to use for composition
            aspect_ratio: Output aspect ratio
            resolution: Output resolution (1K, 2K, 4K)
            seed: Optional seed for reproducible generation (0 to 2147483647).
                  Note: Seed support depends on the underlying API.

        Returns:
            ImageGenerationResult with composed image data
        """
        from PIL import Image

        model = validate_model(model)
        aspect_ratio = validate_aspect_ratio(aspect_ratio)
        resolution = validate_resolution(resolution, model)
        validated_seed = validate_seed(seed)

        # Validate image count (Pro supports up to 14)
        if len(image_paths) > 14:
            raise ValueError(
                f"Maximum 14 images supported, got {len(image_paths)}"
            )

        images = [Image.open(p) for p in image_paths]
        contents = [prompt] + images

        config = types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size=resolution if model == "gemini-3-pro-image-preview" else None,
            ),
            # Note: seed parameter is validated and stored for future API support
            # When Gemini API supports seed, add: seed=validated_seed
        )

        @DEFAULT_RETRY
        def _call_api():
            return self._client.models.generate_content(
                model=model,
                contents=contents,
                config=config,
            )

        response = _call_api()
        return ImageGenerationResult.from_response(response)

    def search_grounded_image(
        self,
        prompt: str,
        aspect_ratio: str | None = None,
        resolution: str | None = None,
    ) -> ImageGenerationResult:
        """Generate image with Google Search grounding (Pro only)."""
        model = "gemini-3-pro-image-preview"
        aspect_ratio = validate_aspect_ratio(aspect_ratio)
        resolution = validate_resolution(resolution, model)

        config = types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size=resolution,
            ),
            tools=[{"google_search": {}}],
        )

        @DEFAULT_RETRY
        def _call_api():
            return self._client.models.generate_content(
                model=model,
                contents=prompt,
                config=config,
            )

        response = _call_api()
        return ImageGenerationResult.from_response(response)
