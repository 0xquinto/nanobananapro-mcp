import pytest
from unittest.mock import AsyncMock, Mock, patch

from nanobananapro_mcp.sessions import ChatSessionManager, ChatSession


class TestChatSessionManager:
    def test_create_session_returns_id(self):
        manager = ChatSessionManager()
        with patch("nanobananapro_mcp.sessions.GeminiImageClient"):
            session_id = manager.create_session(model="gemini-3-pro-image-preview")
            assert isinstance(session_id, str)
            assert len(session_id) > 0

    def test_get_session_returns_session(self):
        manager = ChatSessionManager()
        with patch("nanobananapro_mcp.sessions.GeminiImageClient"):
            session_id = manager.create_session(model="gemini-3-pro-image-preview")
            session = manager.get_session(session_id)
            assert session is not None
            assert isinstance(session, ChatSession)

    def test_get_nonexistent_session_raises(self):
        manager = ChatSessionManager()
        with pytest.raises(KeyError, match="Session not found"):
            manager.get_session("nonexistent-id")

    def test_delete_session_removes_session(self):
        manager = ChatSessionManager()
        with patch("nanobananapro_mcp.sessions.GeminiImageClient"):
            session_id = manager.create_session(model="gemini-3-pro-image-preview")
            manager.delete_session(session_id)
            with pytest.raises(KeyError):
                manager.get_session(session_id)

    def test_list_sessions_returns_all_ids(self):
        manager = ChatSessionManager()
        with patch("nanobananapro_mcp.sessions.GeminiImageClient"):
            id1 = manager.create_session(model="gemini-3-pro-image-preview")
            id2 = manager.create_session(model="pro")
            sessions = manager.list_sessions()
            assert id1 in sessions
            assert id2 in sessions


class TestChatSession:
    @pytest.mark.asyncio
    async def test_send_message_stores_history(self):
        with patch("nanobananapro_mcp.sessions.GeminiImageClient") as mock_client_class:
            mock_client = Mock()
            mock_client_class.return_value = mock_client
            mock_chat = Mock()
            mock_client._client.aio.chats.create.return_value = mock_chat
            mock_response = Mock()
            mock_response.parts = [Mock(text="response", inline_data=None)]
            mock_chat.send_message = AsyncMock(return_value=mock_response)

            session = ChatSession(model="gemini-3-pro-image-preview")
            await session.send_message("test prompt")

            assert len(session.history) == 2
            assert session.history[0]["role"] == "user"
            assert session.history[0]["content"] == "test prompt"
            assert session.history[1]["role"] == "assistant"
            assert session.history[1]["content"] == "response"


class TestAsyncChatSession:
    @pytest.mark.asyncio
    async def test_send_message_is_async(self):
        with patch("nanobananapro_mcp.sessions.GeminiImageClient") as mock_client_class:
            mock_client = Mock()
            mock_client_class.return_value = mock_client
            mock_chat = Mock()
            mock_client._client.aio.chats.create.return_value = mock_chat
            mock_response = Mock()
            mock_response.parts = [Mock(text="async response", inline_data=None)]
            mock_chat.send_message = AsyncMock(return_value=mock_response)

            session = ChatSession(model="gemini-3-pro-image-preview")
            result = await session.send_message("test prompt")

            assert result.text == "async response"
            mock_chat.send_message.assert_called_once()
