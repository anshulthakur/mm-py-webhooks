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

    @patch('requests.post')
    @patch('requests.get')
    def test_send_direct_message(self, mock_get, mock_post):
        # Arrange
        # Mock GET requests: /users/me and /users/username/target-user
        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json.side_effect = [
            {"id": "bot-user-id"},       # for /users/me
            {"id": "recipient-user-id"}  # for /users/username/target-user
        ]
        mock_get.return_value = mock_get_response

        # Mock POST requests: /channels/direct and /posts
        mock_post_response = MagicMock()
        mock_post_response.status_code = 200
        mock_post_response.json.side_effect = [
            {"id": "direct-channel-id"},  # for /channels/direct
            {"id": "post-id", "message": "Hello to user!"}  # for /posts
        ]
        mock_post.return_value = mock_post_response

        client = WebClient.SyncMattermostClient(
            server_url="https://mattermost.example.com",
            bot_token="my-bot-token"
        )

        # Act
        result = client.send_direct_message(recipient="target-user", text="Hello to user!")

        # Assert
        self.assertEqual(result, {"id": "post-id", "message": "Hello to user!"})
        
        # Verify GET calls
        mock_get.assert_any_call("https://mattermost.example.com/api/v4/users/me", headers={"Authorization": "Bearer my-bot-token"})
        mock_get.assert_any_call("https://mattermost.example.com/api/v4/users/username/target-user", headers={"Authorization": "Bearer my-bot-token"})

        # Verify POST calls
        mock_post.assert_any_call(
            "https://mattermost.example.com/api/v4/channels/direct",
            headers={"Authorization": "Bearer my-bot-token", "Content-Type": "application/json"},
            json=["bot-user-id", "recipient-user-id"]
        )
        mock_post.assert_any_call(
            "https://mattermost.example.com/api/v4/posts",
            headers={"Authorization": "Bearer my-bot-token", "Content-Type": "application/json"},
            json={"channel_id": "direct-channel-id", "message": "Hello to user!"}
        )

    def test_send_direct_message_missing_config(self):
        client = WebClient.SyncMattermostClient()
        with self.assertRaises(ValueError):
            client.send_direct_message(recipient="target-user", text="Hello")

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

    @patch("client.aiohttp.ClientSession")
    async def test_send_direct_message(self, MockClientSession):
        # Create mock responses for session.get and session.post
        # GET /users/me
        mock_get_me_resp = AsyncMock()
        mock_get_me_resp.status = 200
        mock_get_me_resp.json = AsyncMock(return_value={"id": "bot-user-id"})

        # GET /users/username/target-user
        mock_get_user_resp = AsyncMock()
        mock_get_user_resp.status = 200
        mock_get_user_resp.json = AsyncMock(return_value={"id": "recipient-user-id"})

        # POST /channels/direct
        mock_post_channel_resp = AsyncMock()
        mock_post_channel_resp.status = 200
        mock_post_channel_resp.json = AsyncMock(return_value={"id": "direct-channel-id"})

        # POST /posts
        mock_post_msg_resp = AsyncMock()
        mock_post_msg_resp.status = 200
        mock_post_msg_resp.json = AsyncMock(return_value={"id": "post-id", "message": "Hello to user!"})

        # Mocks for GET/POST context managers
        mock_get_me_cm = MagicMock()
        mock_get_me_cm.__aenter__.return_value = mock_get_me_resp
        mock_get_me_cm.__aexit__.return_value = AsyncMock()

        mock_get_user_cm = MagicMock()
        mock_get_user_cm.__aenter__.return_value = mock_get_user_resp
        mock_get_user_cm.__aexit__.return_value = AsyncMock()

        mock_post_channel_cm = MagicMock()
        mock_post_channel_cm.__aenter__.return_value = mock_post_channel_resp
        mock_post_channel_cm.__aexit__.return_value = AsyncMock()

        mock_post_msg_cm = MagicMock()
        mock_post_msg_cm.__aenter__.return_value = mock_post_msg_resp
        mock_post_msg_cm.__aexit__.return_value = AsyncMock()

        # Create mock session
        mock_session = MagicMock()
        mock_session.get.side_effect = [mock_get_me_cm, mock_get_user_cm]
        mock_session.post.side_effect = [mock_post_channel_cm, mock_post_msg_cm]

        # Make aiohttp.ClientSession() return our mock session as context manager
        mock_client_cm = MagicMock()
        mock_client_cm.__aenter__.return_value = mock_session
        mock_client_cm.__aexit__.return_value = AsyncMock()
        MockClientSession.return_value = mock_client_cm

        # Instantiate client and send direct message
        client = WebClient.AsyncMattermostClient(
            server_url="https://mattermost.example.com",
            bot_token="my-bot-token"
        )
        result = await client.send_direct_message(recipient="target-user", text="Hello to user!")

        self.assertEqual(result, {"id": "post-id", "message": "Hello to user!"})

        # Assert calls
        mock_session.get.assert_any_call(
            "https://mattermost.example.com/api/v4/users/me",
            headers={"Authorization": "Bearer my-bot-token"}
        )
        mock_session.get.assert_any_call(
            "https://mattermost.example.com/api/v4/users/username/target-user",
            headers={"Authorization": "Bearer my-bot-token"}
        )
        mock_session.post.assert_any_call(
            "https://mattermost.example.com/api/v4/channels/direct",
            headers={"Authorization": "Bearer my-bot-token", "Content-Type": "application/json"},
            json=["bot-user-id", "recipient-user-id"]
        )
        mock_session.post.assert_any_call(
            "https://mattermost.example.com/api/v4/posts",
            headers={"Authorization": "Bearer my-bot-token", "Content-Type": "application/json"},
            json={"channel_id": "direct-channel-id", "message": "Hello to user!"}
        )

    async def test_send_direct_message_missing_config(self):
        client = WebClient.AsyncMattermostClient()
        with self.assertRaises(ValueError):
            await client.send_direct_message(recipient="target-user", text="Hello")

if __name__ == '__main__':
    unittest.main()
