# Mattermost Client for Incoming Webhooks

A simple Python client for sending messages to Mattermost using incoming webhooks.

## Installation

```bash
pip install mattermost-client-py
```

## Usage

First, you need to create an incoming webhook in your Mattermost instance. You can find instructions on how to do that [here](https://developers.mattermost.com/integrate/webhooks/incoming/).

### Synchronous Client

The synchronous client is useful for simple applications that don't require asynchronous operations.

```python
from mattermost_client import SyncMattermostClient

# Initialize the client with your Mattermost webhook URL
client = SyncMattermostClient("https://your-mattermost-instance.com/hooks/your_webhook_token")

# Send a simple message
response = client.send_message(text='Hello, Mattermost!')
print(response)

# Send a more complex message with attachments
attachments = [
    {
        "fallback": "Upgrade your client to see this attachment.",
        "color": "#FF8000",
        "pretext": "This is optional pretext that shows above the attachment.",
        "author_name": "Mattermost",
        "author_link": "https://mattermost.com/",
        "author_icon": "http://www.mattermost.org/wp-content/uploads/2016/04/icon.png",
        "title": "Example Attachment",
        "title_link": "https://docs.mattermost.com/developer/message-attachments.html",
        "text": "This is the text of the attachment. It can be formatted with Markdown.",
        "fields": [
            {
                "short": False,
                "title": "Long Field",
                "value": "This is a long field, so it is not short."
            },
            {
                "short": True,
                "title": "Short Field",
                "value": "This is a short field."
            }
        ],
        "image_url": "http://www.mattermost.org/wp-content/uploads/2016/04/icon.png"
    }
]


response = client.send_message(
    text='A message with an attachment.',
    attachments=attachments,
    channel='town-square',
    username='My Bot',
    icon_url='https://www.mattermost.org/wp-content/uploads/2016/04/icon.png'
)
print(response)
```

## Asynchronous Usage (with aiohttp)

The asynchronous client is ideal for applications using `asyncio`.

```python
import asyncio
from mattermost_client import AsyncMattermostClient

async def main():
    # Initialize the client with your Mattermost webhook URL
    mm = AsyncMattermostClient("https://your-mattermost-instance.com/hooks/your_webhook_token")

    # Send a message asynchronously
    response = await mm.send_message("Hello, Mattermost! (async)")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License.