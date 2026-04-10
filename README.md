# ospsd-chat-api

Shared abstract Chat vertical API for OSPSD Spring '26 — Teams 4 (Telegram), 8 (Discord), 9 (Slack).

This repo contains only the ABC definitions — no implementation code.

## Install

```bash
uv add git+https://github.com/HarshithKoriRaj/Shared-API.git
```

## Contract

### Data Classes

- `Message` — `message_id`, `channel`, `text`, `sender`, `timestamp`
- `Channel` — `channel_id`, `name`, `is_private`, `channel_type`

### Methods

| Method | Signature | Returns |
|--------|-----------|---------|
| `send_message` | `(channel_id, text)` | `Message` |
| `get_channels` | `()` | `list[Channel]` |
| `get_channel` | `(channel_id)` | `Channel` |
| `get_messages` | `(channel_id, limit=10, cursor=None)` | `list[Message]` |
| `get_message` | `(message_id)` | `Message` |
| `delete_message` | `(message_id)` | `None` |

## Notes

- `message_id` is **opaque** — each implementation encodes it as needed
  (Slack: `"channel_id:timestamp"`, Telegram: `"chat_id:message_id"`)
- `cursor` in `get_messages` is optional — implementations that do not
  support pagination may ignore it
- `is_private` in `Channel` is optional — `None` if platform does not distinguish
- `channel_type` in `Channel` is optional — used by Telegram to distinguish
  `"group"`, `"supergroup"`, `"channel"`, `"dm"` chat types

## Usage

```python
from chat_client_api import ChatClient, Channel, Message, get_client, register_client
```
