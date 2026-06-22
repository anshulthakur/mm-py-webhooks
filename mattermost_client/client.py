import requests
import aiohttp

class SyncMattermostClient:
    """
    Synchronous client for Mattermost incoming webhooks and bot token messaging.
    """
    def __init__(self, webhook_url=None, channel=None, username=None, icon_url=None, server_url=None, bot_token=None):
        self.webhook_url = webhook_url
        self.channel = channel
        self.username = username
        self.icon_url = icon_url
        self.server_url = server_url
        self.bot_token = bot_token
        self._bot_user_id = None

    def send_message(self, text=None, channel=None, username=None, icon_url=None, icon_emoji=None, attachments=None, type=None, props=None, priority=None):
        """
        Sends a message to the Mattermost webhook.
        """
        if not self.webhook_url:
            raise ValueError("webhook_url must be configured to send webhook messages.")

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

    def _get_bot_user_id(self):
        if self._bot_user_id:
            return self._bot_user_id
        
        url = f"{self.server_url.rstrip('/')}/api/v4/users/me"
        headers = {"Authorization": f"Bearer {self.bot_token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        self._bot_user_id = response.json().get("id")
        return self._bot_user_id

    def _get_recipient_user_id(self, recipient):
        clean_name = recipient
        if clean_name.startswith('@'):
            clean_name = clean_name[1:]
        
        try:
            url = f"{self.server_url.rstrip('/')}/api/v4/users/username/{clean_name}"
            headers = {"Authorization": f"Bearer {self.bot_token}"}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json().get("id")
        except Exception:
            pass
            
        return recipient

    def send_direct_message(self, recipient, text=None, attachments=None, props=None):
        """
        Sends a direct message (personal message) to a user using the bot-account token.
        `recipient` can be a username (with or without '@') or a user ID.
        """
        if not self.server_url or not self.bot_token:
            raise ValueError("server_url and bot_token must be configured to send direct messages.")

        headers = {
            "Authorization": f"Bearer {self.bot_token}",
            "Content-Type": "application/json"
        }
        
        bot_user_id = self._get_bot_user_id()
        recipient_user_id = self._get_recipient_user_id(recipient)
        
        channel_url = f"{self.server_url.rstrip('/')}/api/v4/channels/direct"
        channel_response = requests.post(
            channel_url,
            headers=headers,
            json=[bot_user_id, recipient_user_id]
        )
        channel_response.raise_for_status()
        channel_id = channel_response.json().get("id")
        
        posts_url = f"{self.server_url.rstrip('/')}/api/v4/posts"
        if props is None:
            props = {}
        if attachments is not None:
            props["attachments"] = attachments

        payload = {
            "channel_id": channel_id,
            "message": text,
            "props": props if props else None
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        
        post_response = requests.post(posts_url, headers=headers, json=payload)
        post_response.raise_for_status()
        return post_response.json()

class AsyncMattermostClient:
    """
    Asynchronous client for Mattermost incoming webhooks and bot token messaging.
    """
    def __init__(self, webhook_url=None, channel=None, username=None, icon_url=None, server_url=None, bot_token=None):
        self.webhook_url = webhook_url
        self.channel = channel
        self.username = username
        self.icon_url = icon_url
        self.server_url = server_url
        self.bot_token = bot_token
        self._bot_user_id = None

    async def send_message(self, text=None, channel=None, username=None, icon_url=None, icon_emoji=None, attachments=None, type=None, props=None, priority=None):
        """
        Sends a message to the Mattermost webhook asynchronously.
        """
        if not self.webhook_url:
            raise ValueError("webhook_url must be configured to send webhook messages.")

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

    async def _get_bot_user_id(self, session):
        if self._bot_user_id:
            return self._bot_user_id
        
        url = f"{self.server_url.rstrip('/')}/api/v4/users/me"
        headers = {"Authorization": f"Bearer {self.bot_token}"}
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            data = await response.json()
            self._bot_user_id = data.get("id")
            return self._bot_user_id

    async def _get_recipient_user_id(self, session, recipient):
        clean_name = recipient
        if clean_name.startswith('@'):
            clean_name = clean_name[1:]
        
        try:
            url = f"{self.server_url.rstrip('/')}/api/v4/users/username/{clean_name}"
            headers = {"Authorization": f"Bearer {self.bot_token}"}
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("id")
        except Exception:
            pass
            
        return recipient

    async def send_direct_message(self, recipient, text=None, attachments=None, props=None):
        """
        Sends a direct message (personal message) to a user using the bot-account token asynchronously.
        `recipient` can be a username (with or without '@') or a user ID.
        """
        if not self.server_url or not self.bot_token:
            raise ValueError("server_url and bot_token must be configured to send direct messages.")

        headers = {
            "Authorization": f"Bearer {self.bot_token}",
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            bot_user_id = await self._get_bot_user_id(session)
            recipient_user_id = await self._get_recipient_user_id(session, recipient)
            
            channel_url = f"{self.server_url.rstrip('/')}/api/v4/channels/direct"
            async with session.post(
                channel_url,
                headers=headers,
                json=[bot_user_id, recipient_user_id]
            ) as channel_response:
                channel_response.raise_for_status()
                channel_data = await channel_response.json()
                channel_id = channel_data.get("id")
            
            posts_url = f"{self.server_url.rstrip('/')}/api/v4/posts"
            if props is None:
                props = {}
            if attachments is not None:
                props["attachments"] = attachments

            payload = {
                "channel_id": channel_id,
                "message": text,
                "props": props if props else None
            }
            payload = {k: v for k, v in payload.items() if v is not None}
            
            async with session.post(posts_url, headers=headers, json=payload) as post_response:
                post_response.raise_for_status()
                return await post_response.json()