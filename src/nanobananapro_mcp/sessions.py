"""Multi-turn chat session management for image generation."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from google.genai import types

from .client import GeminiImageClient, ImageGenerationResult
from .utils import validate_model, validate_aspect_ratio, validate_resolution


@dataclass
class ChatSession:
    """A multi-turn image chat session."""

    model: str
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    history: list[dict] = field(default_factory=list)
    _client: GeminiImageClient | None = field(default=None, repr=False)
    _chat: Any = field(default=None, repr=False)

    def __post_init__(self):
        self.model = validate_model(self.model)
        self._client = GeminiImageClient()
        self._chat = self._client._client.aio.chats.create(
            model=self.model,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                tools=[{"google_search": {}}] if "pro" in self.model else None,
            ),
        )

    async def send_message(
        self,
        prompt: str,
        aspect_ratio: str | None = None,
        resolution: str | None = None,
    ) -> ImageGenerationResult:
        """Send a message and get a response."""
        aspect_ratio = validate_aspect_ratio(aspect_ratio)
        resolution = validate_resolution(resolution, self.model)

        config = types.GenerateContentConfig(
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size=resolution if "pro" in self.model else None,
            ),
        )

        self.history.append({"role": "user", "content": prompt})

        response = await self._chat.send_message(prompt, config=config)
        result = ImageGenerationResult.from_response(response)

        self.history.append({
            "role": "assistant",
            "content": result.text,
            "has_image": result.image_data is not None,
        })

        return result


class ChatSessionManager:
    """Manages multiple chat sessions."""

    def __init__(self):
        self._sessions: dict[str, ChatSession] = {}

    def create_session(self, model: str = "gemini-3-pro-image-preview") -> str:
        """Create a new chat session and return its ID."""
        session = ChatSession(model=model)
        self._sessions[session.session_id] = session
        return session.session_id

    def get_session(self, session_id: str) -> ChatSession:
        """Get a session by ID."""
        if session_id not in self._sessions:
            raise KeyError(f"Session not found: {session_id}")
        return self._sessions[session_id]

    def delete_session(self, session_id: str) -> None:
        """Delete a session."""
        if session_id not in self._sessions:
            raise KeyError(f"Session not found: {session_id}")
        del self._sessions[session_id]

    def list_sessions(self) -> list[str]:
        """List all session IDs."""
        return list(self._sessions.keys())
