"""Shared Chat vertical API — Teams 4 (Telegram), 8 (Discord), 9 (Slack)."""
from .client import (
    Channel,
    ChannelNotFoundError,
    ChatClient,
    ChatError,
    Message,
    MessageDeleteError,
    MessageNotFoundError,
    get_client,
    register_client,
)

__all__ = [
    "Channel",
    "ChannelNotFoundError",
    "ChatClient",
    "ChatError",
    "Message",
    "MessageDeleteError",
    "MessageNotFoundError",
    "get_client",
    "register_client",
]
