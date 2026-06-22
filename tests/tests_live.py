import unittest
import os
import asyncio
import client as WebClient

# To run these live tests, set the MATTERMOST_WEBHOOK_URL environment variable
# to your Mattermost incoming webhook URL.
channel = "channel-activity"
username = "username"
recipient = "targetuser"
MATTERMOST_WEBHOOK_URL = os.environ.get("MATTERMOST_WEBHOOK_URL", None)
MATTERMOST_BOT_TOKEN = os.environ.get("MATTERMOST_BOT_TOKEN", None)
MATTERMOST_SERVER_URL = os.environ.get("MATTERMOST_SERVER_URL", None)

@unittest.skipIf(not MATTERMOST_WEBHOOK_URL, "MATTERMOST_WEBHOOK_URL environment variable not set")
class TestSyncMattermostClientLive(unittest.TestCase):

    def setUp(self):
        self.client = WebClient.SyncMattermostClient(MATTERMOST_WEBHOOK_URL, channel=channel, username=username)

    def test_send_message(self):
        """
        Tests sending a simple message using the synchronous client.
        """
        response = self.client.send_message(text="Hello from the sync live test!")
        self.assertEqual(response, "ok")

    def test_send_message_with_attachment(self):
        """
        Tests sending a message with an attachment using the synchronous client.
        """
        attachments = [
            {
                "fallback": "This is a test attachment.",
                "color": "#36a64f",
                "pretext": "This is the attachment pretext.",
                "author_name": "Test Bot",
                "author_link": "https://github.com/anshulthakur/mm-py-webhooks",
                "author_icon": "https://www.mattermost.org/wp-content/uploads/2016/04/icon.png",
                "title": "Test Attachment",
                "title_link": "https://www.mattermost.org/",
                "text": "This is the attachment text.",
                "fields": [
                    {
                        "short": False,
                        "title": "Field 1",
                        "value": "This is the first field."
                    },
                    {
                        "short": True,
                        "title": "Field 2",
                        "value": "This is the second field."
                    }
                ]
            }
        ]
        response = self.client.send_message(text="A message with an attachment from the sync live test.", attachments=attachments)
        self.assertEqual(response, "ok")

    @unittest.skipIf(not (MATTERMOST_SERVER_URL and MATTERMOST_BOT_TOKEN), "MATTERMOST_SERVER_URL or MATTERMOST_BOT_TOKEN not set")
    def test_send_direct_message(self):
        """
        Tests sending a personal direct message to a user using the synchronous client.
        """
        client = WebClient.SyncMattermostClient(
            server_url=MATTERMOST_SERVER_URL,
            bot_token=MATTERMOST_BOT_TOKEN
        )
        response = client.send_direct_message(recipient=recipient, text=f"Hello {recipient}! This is a live sync direct message from the bot.")
        self.assertIn("id", response)
        self.assertEqual(response["message"], f"Hello {recipient}! This is a live sync direct message from the bot.")

@unittest.skipIf(not MATTERMOST_WEBHOOK_URL, "MATTERMOST_WEBHOOK_URL environment variable not set")
class TestAsyncMattermostClientLive(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.client = WebClient.AsyncMattermostClient(MATTERMOST_WEBHOOK_URL, channel=channel, username=username)

    async def test_send_message(self):
        """
        Tests sending a simple message using the asynchronous client.
        """
        response = await self.client.send_message(text="Hello from the async live test!")
        self.assertEqual(response, "ok")

    async def test_send_message_with_attachment(self):
        """
        Tests sending a message with an attachment using the asynchronous client.
        """
        attachments = [
            {
                "fallback": "This is a test attachment.",
                "color": "#36a64f",
                "pretext": "This is the attachment pretext.",
                "author_name": "Test Bot",
                "author_link": "https://github.com/anshulthakur/mm-py-webhooks",
                "author_icon": "https://www.mattermost.org/wp-content/uploads/2016/04/icon.png",
                "title": "Test Attachment",
                "title_link": "https://www.mattermost.org/",
                "text": "This is the attachment text.",
                "fields": [
                    {
                        "short": False,
                        "title": "Field 1",
                        "value": "This is the first field."
                    },
                    {
                        "short": True,
                        "title": "Field 2",
                        "value": "This is the second field."
                    }
                ]
            }
        ]
        response = await self.client.send_message(text="A message with an attachment from the async live test.", attachments=attachments)
        self.assertEqual(response, "ok")

    @unittest.skipIf(not (MATTERMOST_SERVER_URL and MATTERMOST_BOT_TOKEN), "MATTERMOST_SERVER_URL or MATTERMOST_BOT_TOKEN not set")
    async def test_send_direct_message(self):
        """
        Tests sending a personal direct message to a user using the asynchronous client.
        """
        client = WebClient.AsyncMattermostClient(
            server_url=MATTERMOST_SERVER_URL,
            bot_token=MATTERMOST_BOT_TOKEN
        )
        response = await client.send_direct_message(recipient=recipient, text=f"Hello {recipient}! This is a live async direct message from the bot.")
        self.assertIn("id", response)
        self.assertEqual(response["message"], f"Hello {recipient}! This is a live async direct message from the bot.")

if __name__ == '__main__':
    unittest.main()
