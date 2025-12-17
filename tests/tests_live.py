import unittest
import os
import asyncio
import client as WebClient

# To run these live tests, set the MATTERMOST_WEBHOOK_URL environment variable
# to your Mattermost incoming webhook URL.
channel = "channel-activity"
username = "username"
MATTERMOST_WEBHOOK_URL = os.environ.get("MATTERMOST_WEBHOOK_URL", "<url>")

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

if __name__ == '__main__':
    unittest.main()
