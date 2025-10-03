import requests
import aiohttp

class SyncMattermostClient:
    """
    Synchronous client for Mattermost incoming webhooks.
    """
    def __init__(self, webhook_url, channel=None, username=None, icon_url=None):
        self.webhook_url = webhook_url
        self.channel = channel
        self.username = username
        self.icon_url = icon_url

    def send_message(self, text=None, channel=None, username=None, icon_url=None, icon_emoji=None, attachments=None, type=None, props=None, priority=None):
        """
        Sends a message to the Mattermost webhook.
        """
        payload = {
            "text": text,
            "channel": channel or self.channel,
            "username": username or self.username,
            "icon_url": icon_url or self.icon_url,
            "icon_emoji": icon_emoji,
            "attachments": attachments,
            "type": type,
            "props": props,
            "priority": priority
        }
        # Filter out None values
        payload = {k: v for k, v in payload.items() if v is not None}

        response = requests.post(self.webhook_url, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.text

class AsyncMattermostClient:
    """
    Asynchronous client for Mattermost incoming webhooks.
    """
    def __init__(self, webhook_url, channel=None, username=None, icon_url=None):
        self.webhook_url = webhook_url
        self.channel = channel
        self.username = username
        self.icon_url = icon_url

    async def send_message(self, text=None, channel=None, username=None, icon_url=None, icon_emoji=None, attachments=None, type=None, props=None, priority=None):
        """
        Sends a message to the Mattermost webhook asynchronously.
        """
        payload = {
            "text": text,
            "channel": channel or self.channel,
            "username": username or self.username,
            "icon_url": icon_url or self.icon_url,
            "icon_emoji": icon_emoji,
            "attachments": attachments,
            "type": type,
            "props": props,
            "priority": priority
        }
        # Filter out None values
        payload = {k: v for k, v in payload.items() if v is not None}

        async with aiohttp.ClientSession() as session:
            async with session.post(self.webhook_url, json=payload) as response:
                response.raise_for_status() # Raise an exception for bad status codes
                return await response.text()