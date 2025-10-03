# Mattermost Python Webhooks

A Python client for sending messages to Mattermost using incoming webhooks. This library provides both synchronous and asynchronous clients.

## Installation

Use pip to install the package:

```bash
pip install git+https://github.com/anshulthakur/mm-py-webhooks.git
```

## Usage

First, you need to create an incoming webhook in your Mattermost instance. You can find instructions on how to do that [here](https://developers.mattermost.com/integrate/webhooks/incoming/).

### Synchronous Client

The synchronous client is useful for simple applications that don't require asynchronous operations.

```python
from mattermost_py import SyncMattermostClient

# Initialize the client with your webhook URL
client = SyncMattermostClient('https://your-mattermost-instance.com/hooks/your-webhook-token')

# Send a simple message
response = client.send_message(text='Hello, Mattermost!')
print(response)

# Send a message with more options
attachments = [{
    'fallback': 'This is the fallback text for the attachment.',
    'color': '#36a64f',
    'pretext': 'This is optional pretext that appears above the attachment.',
    'author_name': 'Mattermost Py',
    'author_link': 'https://github.com/your-username/mm-py-webhooks',
    'author_icon': 'https://www.mattermost.org/wp-content/uploads/2016/04/icon.png',
    'title': 'Attachment Title',
    'title_link': 'https://docs.mattermost.com/developer/message-attachments.html',
    'text': 'This is the text of the attachment.',
    'fields': [{
        'short': False,
        'title': 'Field 1',
        'value': 'Value 1'
    }, {
        'short': True,
        'title': 'Field 2',
        'value': 'Value 2'
    }],
    'image_url': 'http://www.mattermost.org/wp-content/uploads/2016/03/logoHorizontal_WS.png'
}]

response = client.send_message(
    text='A message with an attachment.',
    attachments=attachments,
    channel='town-square',
    username='My Bot',
    icon_url='https://www.mattermost.org/wp-content/uploads/2016/04/icon.png'
)
print(response)
```

### Asynchronous Client

The asynchronous client is ideal for applications using `asyncio`.

```python
import asyncio
from mattermost_py import AsyncMattermostClient

async def main():
    # Initialize the client with your webhook URL
    client = AsyncMattermostClient('https://your-mattermost-instance.com/hooks/your-webhook-token')

    # Send a simple message
    response = await client.send_message(text='Hello, Mattermost!')
    print(response)

if __name__ == '__main__':
    asyncio.run(main())
```
