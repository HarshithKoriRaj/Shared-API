"""Shared Chat vertical API — abstract contract for all chat implementations."""

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class Message:
    """Represents a chat message."""

    message_id: str   # opaque — each implementation encodes as needed
    channel: str      # channel_id the message belongs to
    text: str
    sender: str
    timestamp: str


@dataclass
class Channel:
    """Represents a chat channel or conversation."""

    channel_id: str
    name: str
    is_private: bool | None = None   # None if platform does not distinguish
    channel_type: str | None = None  # e.g. "group", "supergroup", "dm"


class ChatClient(ABC):
    """Abstract base class for all chat client implementations."""

    @abstractmethod
    def send_message(self, channel_id: str, text: str) -> Message:
        """Send a message to a channel.

        Args:
            channel_id: The target channel or conversation ID.
            text: The message content to send.

        Returns:
            The sent Message object.

        """

    @abstractmethod
    def get_channels(self) -> list[Channel]:
        """List all available channels or conversations.

        Returns:
            List of Channel objects.

        """

    @abstractmethod
    def get_channel(self, channel_id: str) -> Channel:
        """Get a single channel by ID.

        Args:
            channel_id: The channel ID to retrieve.

        Returns:
            Channel object.

        Raises:
            ValueError: If the channel is not found.

        """

    @abstractmethod
    def get_messages(
        self,
        channel_id: str,
        limit: int = 10,
        cursor: str | None = None,
    ) -> list[Message]:
        """Get recent messages from a channel.

        Args:
            channel_id: The channel or conversation to fetch messages from.
            limit: Maximum number of messages to return.
            cursor: Optional pagination cursor. Implementations that do not
                support cursor-based pagination may ignore this parameter.

        Returns:
            List of Message objects.

        """

    @abstractmethod
    def get_message(self, message_id: str) -> Message:
        """Get a single message by its opaque ID.

        Args:
            message_id: Opaque message identifier. Format is
                implementation-defined (e.g. ``"channel_id:timestamp"``
                for Slack, ``"chat_id:message_id"`` for Telegram).

        Returns:
            Message object.

        Raises:
            ValueError: If the message is not found.

        """

    @abstractmethod
    def delete_message(self, message_id: str) -> None:
        """Delete a message by its opaque ID.

        Args:
            message_id: Opaque message identifier. Format is
                implementation-defined (e.g. ``"channel_id:timestamp"``
                for Slack, ``"chat_id:message_id"`` for Telegram).

        Raises:
            ValueError: If the message cannot be deleted or is not found.

        """


class _ClientRegistry:
    """Holds the registered client factory."""

    _factory: Callable[[], ChatClient] | None = None

    @classmethod
    def set(cls, factory: Callable[[], ChatClient]) -> None:
        """Register a factory.

        Args:
            factory: Callable that returns a ChatClient instance.

        """
        cls._factory = factory

    @classmethod
    def get(cls) -> Callable[[], ChatClient] | None:
        """Get the registered factory.

        Returns:
            The registered factory or None.

        """
        return cls._factory


def get_client() -> ChatClient:
    """Return an instance of the registered ChatClient implementation.

    Returns:
        Instance of the registered ChatClient.

    Raises:
        RuntimeError: If no implementation has been registered.

    """
    factory = _ClientRegistry.get()
    if factory is None:
        msg = (
            "No chat client implementation registered. "
            "Import an implementation package to register it."
        )
        raise RuntimeError(msg)
    return factory()


def register_client(factory: Callable[[], ChatClient]) -> None:
    """Register a chat client implementation factory.

    Call this once at application start-up (e.g. from an implementation's
    ``__init__.py``) to wire in a concrete ChatClient without monkey-patching.

    Args:
        factory: Callable that returns a ChatClient instance.

    """
    _ClientRegistry.set(factory)
