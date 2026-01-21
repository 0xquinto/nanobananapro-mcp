"""Tests for output_path parameter behavior."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from nanobananapro_mcp.server import _result_to_dict
from nanobananapro_mcp.client import ImageGenerationResult


def test_result_to_dict_with_output_path_excludes_base64():
    """When output_path is provided, base64 should NOT be in response."""
    result = ImageGenerationResult(
        text="Test image",
        image_data=b"fake image bytes",
        mime_type="image/png",
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test.png"
        response = _result_to_dict(result, str(output_path))

        assert response["image_base64"] is None
        assert response["saved_path"] == str(output_path.absolute())
        assert output_path.read_bytes() == b"fake image bytes"


def test_result_to_dict_without_output_path_includes_base64():
    """When no output_path, base64 should be in response."""
    result = ImageGenerationResult(
        text="Test image",
        image_data=b"fake image bytes",
        mime_type="image/png",
    )

    response = _result_to_dict(result, output_path=None)

    assert response["image_base64"] is not None
    assert response["saved_path"] is None
