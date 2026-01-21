import base64
import pytest
from pathlib import Path

from nanobananapro_mcp.utils import (
    encode_image_to_base64,
    decode_base64_to_bytes,
    validate_aspect_ratio,
    validate_resolution,
    validate_model,
    MODEL_ALIASES,
    VALID_MODELS,
)


class TestEncodeImageToBase64:
    def test_encodes_bytes_to_base64_string(self):
        image_bytes = b"\x89PNG\r\n\x1a\n"  # PNG magic bytes
        result = encode_image_to_base64(image_bytes)
        assert isinstance(result, str)
        assert base64.b64decode(result) == image_bytes

    def test_encodes_from_file_path(self, tmp_path):
        test_file = tmp_path / "test.png"
        test_file.write_bytes(b"\x89PNG\r\n\x1a\ntest_data")
        result = encode_image_to_base64(test_file)
        assert isinstance(result, str)
        decoded = base64.b64decode(result)
        assert decoded == b"\x89PNG\r\n\x1a\ntest_data"


class TestDecodeBase64ToBytes:
    def test_decodes_base64_string_to_bytes(self):
        original = b"test_image_data"
        encoded = base64.b64encode(original).decode("utf-8")
        result = decode_base64_to_bytes(encoded)
        assert result == original


class TestValidateAspectRatio:
    @pytest.mark.parametrize("ratio", [
        "1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"
    ])
    def test_valid_aspect_ratios(self, ratio):
        assert validate_aspect_ratio(ratio) == ratio

    def test_invalid_aspect_ratio_raises(self):
        with pytest.raises(ValueError, match="Invalid aspect ratio"):
            validate_aspect_ratio("7:3")

    def test_none_returns_default(self):
        assert validate_aspect_ratio(None) == "1:1"


class TestValidateResolution:
    @pytest.mark.parametrize("res", ["1K", "2K", "4K"])
    def test_valid_resolutions(self, res):
        assert validate_resolution(res, model="gemini-3-pro-image-preview") == res

    def test_invalid_resolution_raises(self):
        with pytest.raises(ValueError, match="Invalid resolution"):
            validate_resolution("8K", model="gemini-3-pro-image-preview")

    def test_none_returns_default(self):
        assert validate_resolution(None, model="gemini-3-pro-image-preview") == "1K"

    def test_validate_resolution_allows_all_for_pro(self):
        model = "gemini-3-pro-image-preview"
        assert validate_resolution("1K", model) == "1K"
        assert validate_resolution("2K", model) == "2K"
        assert validate_resolution("4K", model) == "4K"
        assert validate_resolution(None, model) == "1K"  # default


class TestValidateModel:
    def test_valid_models_only_contains_pro(self):
        assert VALID_MODELS == ["gemini-3-pro-image-preview"]

    def test_model_aliases_only_pro(self):
        assert "flash" not in MODEL_ALIASES
        assert "nano-banana" not in MODEL_ALIASES
        assert MODEL_ALIASES["pro"] == "gemini-3-pro-image-preview"
        assert MODEL_ALIASES["nano-banana-pro"] == "gemini-3-pro-image-preview"

    def test_validate_model_rejects_flash(self):
        with pytest.raises(ValueError, match="Invalid model"):
            validate_model("flash")
        with pytest.raises(ValueError, match="Invalid model"):
            validate_model("gemini-2.5-flash-image")

    def test_validate_model_accepts_pro(self):
        assert validate_model("pro") == "gemini-3-pro-image-preview"
        assert validate_model("nano-banana-pro") == "gemini-3-pro-image-preview"
        assert validate_model("gemini-3-pro-image-preview") == "gemini-3-pro-image-preview"

    def test_invalid_model_raises(self):
        with pytest.raises(ValueError, match="Invalid model"):
            validate_model("gpt-4")
