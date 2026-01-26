"""MCP Server for Nano Banana Pro image generation."""

from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .client import GeminiImageClient, ImageGenerationResult
from .sessions import ChatSessionManager
from .utils import encode_image_to_base64, validate_seed

# Default output directory for generated images
DEFAULT_OUTPUT_DIR = "outputs"

# Initialize FastMCP server
mcp = FastMCP("nanobananapro")

# Global client and session manager (lazy initialized)
_client: GeminiImageClient | None = None
session_manager = ChatSessionManager()


def get_client() -> GeminiImageClient:
    """Get or create the Gemini client."""
    global _client
    if _client is None:
        _client = GeminiImageClient()
    return _client


def _generate_output_path(prefix: str = "image") -> Path:
    """Generate a unique output path in the default outputs directory.

    Creates the outputs directory if it doesn't exist.
    Returns a path like: outputs/image_20260126_143052.png
    """
    output_dir = Path(DEFAULT_OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.png"
    return output_dir / filename


def _result_to_dict(result: ImageGenerationResult, output_path: str | None = None) -> dict:
    """Convert ImageGenerationResult to dict for tool response.

    Images are always saved to disk. If no output_path is provided,
    a unique path is auto-generated in the 'outputs/' directory.
    Base64 is NOT included in the response to avoid exceeding token limits.
    """
    response = {
        "text": result.text,
        "mime_type": result.mime_type,
        "saved_path": None,
    }

    if result.image_data:
        # Determine output path (use provided or auto-generate)
        if output_path:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)
        else:
            path = _generate_output_path()

        # Save to file
        path.write_bytes(result.image_data)
        response["saved_path"] = str(path.absolute())

    if result.grounding_metadata:
        response["grounding_metadata"] = result.grounding_metadata

    return response


@mcp.tool()
async def generate_image(
    prompt: str,
    model: str = "gemini-3-pro-image-preview",
    aspect_ratio: str = "1:1",
    resolution: str = "1K",
    output_path: str | None = None,
    seed: int | None = None,
) -> dict:
    """
    Generate an image from a text prompt.

    Args:
        prompt: Text description of the image to generate
        model: Model to use - "pro", "nano-banana-pro", or full model name
        aspect_ratio: Output aspect ratio (1:1, 16:9, 9:16, etc.)
        resolution: Output resolution (1K, 2K, 4K)
        output_path: Path to save the image (default: outputs/image_TIMESTAMP.png)
        seed: Optional seed for reproducible generation (0 to 2147483647)

    Returns:
        Dict with text response and saved_path where image was written
    """
    validated_seed = validate_seed(seed)
    client = get_client()
    result = await client.generate_image(
        prompt=prompt,
        model=model,
        aspect_ratio=aspect_ratio,
        resolution=resolution,
        seed=validated_seed,
    )
    return _result_to_dict(result, output_path)


@mcp.tool()
async def edit_image(
    prompt: str,
    image_path: str,
    model: str = "gemini-3-pro-image-preview",
    aspect_ratio: str | None = None,
    resolution: str = "1K",
    output_path: str | None = None,
    seed: int | None = None,
) -> dict:
    """
    Edit an existing image using a text prompt.

    Args:
        prompt: Instructions for editing the image
        image_path: Path to the input image file
        model: Model to use - "pro", "nano-banana-pro", or full model name
        aspect_ratio: Output aspect ratio (optional, defaults to input)
        resolution: Output resolution (1K, 2K, 4K)
        output_path: Path to save the image (default: outputs/image_TIMESTAMP.png)
        seed: Optional seed for reproducible generation (0 to 2147483647)

    Returns:
        Dict with text response and saved_path where image was written
    """
    validated_seed = validate_seed(seed)
    client = get_client()
    result = await client.edit_image(
        prompt=prompt,
        image_path=image_path,
        model=model,
        aspect_ratio=aspect_ratio,
        resolution=resolution,
        seed=validated_seed,
    )
    return _result_to_dict(result, output_path)


@mcp.tool()
async def compose_images(
    prompt: str,
    image_paths: list[str],
    model: str = "gemini-3-pro-image-preview",
    aspect_ratio: str = "1:1",
    resolution: str = "2K",
    output_path: str | None = None,
    seed: int | None = None,
) -> dict:
    """
    Compose a new image from multiple reference images.

    Args:
        prompt: Instructions for composing the images
        image_paths: List of paths to input images (max 14)
        model: Model to use - "pro", "nano-banana-pro", or full model name
        aspect_ratio: Output aspect ratio
        resolution: Output resolution
        output_path: Path to save the image (default: outputs/image_TIMESTAMP.png)
        seed: Optional seed for reproducible generation (0 to 2147483647)

    Returns:
        Dict with text response and saved_path where image was written
    """
    validated_seed = validate_seed(seed)
    client = get_client()
    result = await client.compose_images(
        prompt=prompt,
        image_paths=image_paths,
        model=model,
        aspect_ratio=aspect_ratio,
        resolution=resolution,
        seed=validated_seed,
    )
    return _result_to_dict(result, output_path)


@mcp.tool()
async def search_grounded_image(
    prompt: str,
    aspect_ratio: str = "16:9",
    resolution: str = "2K",
    output_path: str | None = None,
) -> dict:
    """
    Generate an image grounded with Google Search data (Pro only).

    Useful for visualizing current data like weather forecasts,
    stock charts, or recent events.

    Args:
        prompt: Description incorporating real-time data needs
        aspect_ratio: Output aspect ratio
        resolution: Output resolution (1K, 2K, 4K)
        output_path: Path to save the image (default: outputs/image_TIMESTAMP.png)

    Returns:
        Dict with text, grounding metadata, and saved_path where image was written
    """
    client = get_client()
    result = await client.search_grounded_image(
        prompt=prompt,
        aspect_ratio=aspect_ratio,
        resolution=resolution,
    )
    return _result_to_dict(result, output_path)


@mcp.tool()
async def start_image_chat(
    initial_prompt: str,
    model: str = "gemini-3-pro-image-preview",
    output_path: str | None = None,
    seed: int | None = None,
) -> dict:
    """
    Start a new multi-turn image editing session.

    Args:
        initial_prompt: First prompt to generate the initial image
        model: Model to use for the session
        output_path: Path to save the image (default: outputs/image_TIMESTAMP.png)
        seed: Optional seed for reproducible generation (0 to 2147483647).
              Note: Seed support in chat sessions depends on the underlying API.

    Returns:
        Dict with session_id, text response, and saved_path where image was written
    """
    # Validate seed (reserved for future API support in chat sessions)
    validated_seed = validate_seed(seed)
    session_id = session_manager.create_session(model=model)
    session = session_manager.get_session(session_id)
    result = await session.send_message(initial_prompt)

    result_dict = _result_to_dict(result, output_path)
    result_dict["session_id"] = session_id
    return result_dict


@mcp.tool()
async def continue_image_chat(
    session_id: str,
    prompt: str,
    aspect_ratio: str | None = None,
    resolution: str | None = None,
    output_path: str | None = None,
) -> dict:
    """
    Continue an existing image chat session.

    Args:
        session_id: ID of the session to continue
        prompt: Next instruction for image modification
        aspect_ratio: Optional new aspect ratio
        resolution: Optional new resolution
        output_path: Path to save the image (default: outputs/image_TIMESTAMP.png)

    Returns:
        Dict with session_id, turn_count, text response, and saved_path where image was written
    """
    session = session_manager.get_session(session_id)
    result = await session.send_message(
        prompt=prompt,
        aspect_ratio=aspect_ratio,
        resolution=resolution,
    )

    result_dict = _result_to_dict(result, output_path)
    result_dict["session_id"] = session_id
    result_dict["turn_count"] = len(session.history) // 2
    return result_dict


@mcp.tool()
async def end_image_chat(session_id: str) -> dict:
    """
    End and clean up an image chat session.

    Args:
        session_id: ID of the session to end

    Returns:
        Dict confirming session was ended
    """
    session = session_manager.get_session(session_id)
    turn_count = len(session.history) // 2
    session_manager.delete_session(session_id)

    return {
        "status": "ended",
        "session_id": session_id,
        "total_turns": turn_count,
    }


@mcp.tool()
async def list_chat_sessions() -> dict:
    """
    List all active chat sessions.

    Returns:
        Dict with list of session IDs
    """
    return {
        "sessions": session_manager.list_sessions(),
        "count": len(session_manager.list_sessions()),
    }


def main():
    """Entry point for running the server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
