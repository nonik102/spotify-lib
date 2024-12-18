import unittest
from unittest import mock
from io import StringIO
from time import sleep

from spotify_lib.utils import SpotifySecretProvider, SpotifyTokenProvider

class TestSecretProvider(unittest.TestCase):

    def test_secret_provider(self):
        # setup
        test_file = StringIO(
            "desired_client_id\ndesired_secret\n"
        )
        secret_provider = SpotifySecretProvider("path/to/test/file/directory")
        # mock
        secret_provider._secret_file = lambda x: test_file

        #perform test
        spotify_secret = secret_provider.get_secret("test_file_name")
        self.assertEqual(spotify_secret.client_id, "desired_client_id")
        self.assertEqual(spotify_secret.secret, "desired_secret")

class TestTokenProvider(unittest.TestCase):

    def test_get_token(self):
        mock_token = mock.MagicMock(
            value="token_value",
            alive_seconds=10
        )
        mock_api = mock.MagicMock()
        mock_api.get_auth_token = mock.MagicMock(return_value=mock_token)

        token_provider = SpotifyTokenProvider(mock_api)
        tok = token_provider.get_token()

        self.assertEqual(tok, mock_token)
        mock_api.get_auth_token.assert_called_once()

    def test_token_reuse(self):
        mock_token = mock.MagicMock(
            alive_seconds=1
        )
        mock_api = mock.MagicMock()
        mock_api.get_auth_token = mock.MagicMock(return_value=mock_token)

        token_provider = SpotifyTokenProvider(mock_api)
        # test that we can re-use the same token
        token1 = token_provider.get_token()
        token2 = token_provider.get_token()
        self.assertEqual(token1, token2)
        mock_api.get_auth_token.assert_called_once()


    def test_token_refresh(self):
        mock_token1 = mock.MagicMock(alive_seconds=1)
        mock_token2 = mock.MagicMock(alive_seconds=2)
        mock_api = mock.MagicMock()
        mock_api.get_auth_token = mock.MagicMock(side_effect=[mock_token1, mock_token2])

        token_provider = SpotifyTokenProvider(mock_api)
        # test that we can will get new tokens correctly
        token1 = token_provider.get_token()
        sleep(2)
        token2 = token_provider.get_token()
        self.assertNotEqual(token1, token2)
        self.assertEqual(
            mock_api.get_auth_token.call_count, 2
        )

