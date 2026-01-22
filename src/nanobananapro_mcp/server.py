"""MCP Server for Nano Banana Pro image generation."""

from __future__ import annotations

import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .client import GeminiImageClient, ImageGenerationResult
from .sessions import ChatSessionManager
from .utils import encode_image_to_base64

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


def _result_to_dict(result: ImageGenerationResult, output_path: str | None = None) -> dict:
    """Convert ImageGenerationResult to dict for tool response.

    When output_path is provided, the image is saved to disk and base64 is NOT
    included in the response (to avoid exceeding token limits).
    """
    response = {
        "text": result.text,
        "image_base64": None,
        "mime_type": result.mime_type,
        "saved_path": None,
    }

    if result.image_data:
        if output_path:
            # Save to file, skip base64 to keep response small
            path = Path(output_path)
            path.write_bytes(result.image_data)
            response["saved_path"] = str(path.absolute())
        else:
            # No output path, include base64 in response
            response["image_base64"] = encode_image_to_base64(result.image_data)

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
) -> dict:
    """
    Generate an image from a text prompt.

    Args:
        prompt: Text description of the image to generate
        model: Model to use - "pro", "nano-banana-pro", or full model name
        aspect_ratio: Output aspect ratio (1:1, 16:9, 9:16, etc.)
        resolution: Output resolution (1K, 2K, 4K)
        output_path: Optional path to save the generated image

    Returns:
        Dict with text response, base64 image data, and saved path if applicable
    """
    client = get_client()
    result = client.generate_image(
        prompt=prompt,
        model=model,
        aspect_ratio=aspect_ratio,
        resolution=resolution,
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
) -> dict:
    """
    Edit an existing image using a text prompt.

    Args:
        prompt: Instructions for editing the image
        image_path: Path to the input image file
        model: Model to use - "pro", "nano-banana-pro", or full model name
        aspect_ratio: Output aspect ratio (optional, defaults to input)
        resolution: Output resolution (1K, 2K, 4K)
        output_path: Optional path to save the edited image

    Returns:
        Dict with text response, base64 image data, and saved path if applicable
    """
    client = get_client()
    result = client.edit_image(
        prompt=prompt,
        image_path=image_path,
        model=model,
        aspect_ratio=aspect_ratio,
        resolution=resolution,
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
) -> dict:
    """
    Compose a new image from multiple reference images.

    Args:
        prompt: Instructions for composing the images
        image_paths: List of paths to input images (max 14)
        model: Model to use - "pro", "nano-banana-pro", or full model name
        aspect_ratio: Output aspect ratio
        resolution: Output resolution
        output_path: Optional path to save the composed image

    Returns:
        Dict with text response, base64 image data, and saved path if applicable
    """
    client = get_client()
    result = client.compose_images(
        prompt=prompt,
        image_paths=image_paths,
        model=model,
        aspect_ratio=aspect_ratio,
        resolution=resolution,
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
        output_path: Optional path to save the image

    Returns:
        Dict with text, image, grounding metadata, and saved path
    """
    client = get_client()
    result = client.search_grounded_image(
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
) -> dict:
    """
    Start a new multi-turn image editing session.

    Args:
        initial_prompt: First prompt to generate the initial image
        model: Model to use for the session
        output_path: Optional path to save the generated image

    Returns:
        Dict with session_id and initial generation result
    """
    session_id = session_manager.create_session(model=model)
    session = session_manager.get_session(session_id)
    result = session.send_message(initial_prompt)

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
        output_path: Optional path to save the generated image

    Returns:
        Dict with updated image and text response
    """
    session = session_manager.get_session(session_id)
    result = session.send_message(
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
