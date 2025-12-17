import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import client as WebClient

webhook_url = "https://example.com/webhook"
channel = "test-channel"
username = "test-user"

class TestSyncMattermostClient(unittest.TestCase):

    @patch('requests.post')
    def test_send_message(self, mock_post):
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = 'ok'
        mock_post.return_value = mock_response

        client = WebClient.SyncMattermostClient(webhook_url, channel=channel, username=username)

        # Act
        client.send_message(text='Hello, world!', channel=channel)

        # Assert
        expected_payload = {
            'text': 'Hello, world!',
            'channel': channel,
            'username': username,
        }
        mock_post.assert_called_once_with(webhook_url, json=expected_payload)

    @patch('requests.post')
    def test_send_message_with_defaults(self, mock_post):
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = 'ok'
        mock_post.return_value = mock_response

        client = WebClient.SyncMattermostClient(webhook_url, channel=channel, username=username)

        # Act
        client.send_message(text='Hello, world!')

        # Assert
        expected_payload = {
            'text': 'Hello, world!',
            'channel': channel,
            'username': username,
        }
        mock_post.assert_called_once_with(webhook_url, json=expected_payload)

class TestAsyncMattermostClient(unittest.IsolatedAsyncioTestCase):

    @patch("client.aiohttp.ClientSession")
    async def test_send_message(self, MockClientSession):
        # Create mock response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value="ok")

        # Create mock post context manager
        mock_post_cm = MagicMock()
        mock_post_cm.__aenter__.return_value = mock_response
        mock_post_cm.__aexit__.return_value = AsyncMock()

        # Create mock session
        mock_session = MagicMock()
        mock_session.post.return_value = mock_post_cm

        # Make aiohttp.ClientSession() return our mock session as context manager
        mock_client_cm = MagicMock()
        mock_client_cm.__aenter__.return_value = mock_session
        mock_client_cm.__aexit__.return_value = AsyncMock()
        MockClientSession.return_value = mock_client_cm

        # Instantiate client and send message
        client = WebClient.AsyncMattermostClient(webhook_url, channel=channel, username=username)
        result = await client.send_message(text="Hello, world!")

        # Assert payload and result
        expected_payload = {
            "text": "Hello, world!",
            "channel": channel,
            "username": username,
        }
        mock_session.post.assert_called_once_with(webhook_url, json=expected_payload)
        self.assertEqual(result, "ok")

    @patch("client.aiohttp.ClientSession")
    async def test_send_message_with_defaults(self, MockClientSession):
        # Create mock response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value="ok")

        # Create mock post context manager
        mock_post_cm = MagicMock()
        mock_post_cm.__aenter__.return_value = mock_response
        mock_post_cm.__aexit__.return_value = AsyncMock()

        # Create mock session and attach post context manager
        mock_session = MagicMock()
        mock_session.post.return_value = mock_post_cm

        # Make aiohttp.ClientSession() return our mock session as context manager
        mock_client_cm = MagicMock()
        mock_client_cm.__aenter__.return_value = mock_session
        mock_client_cm.__aexit__.return_value = AsyncMock()
        MockClientSession.return_value = mock_client_cm

        # Instantiate client and send message
        client = WebClient.AsyncMattermostClient(webhook_url, channel=channel, username=username)
        result = await client.send_message(text="Hello, world!")

        # Assert payload and result
        expected_payload = {
            "text": "Hello, world!",
            "channel": channel,
            "username": username,
        }
        mock_session.post.assert_called_once_with(webhook_url, json=expected_payload)
        self.assertEqual(result, "ok")

if __name__ == '__main__':
    unittest.main()
