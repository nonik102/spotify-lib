import unittest
from unittest import mock
from io import StringIO
from time import sleep

from spotify_lib.auth import SpotifyTokenProvider

class TestTokenProvider(unittest.TestCase):
    def test_get_token(self):
        mock_token = mock.MagicMock(
            value="token_value",
            alive_seconds=10
        )
        mock_callback= mock.MagicMock(return_value=mock_token)

        token_provider = SpotifyTokenProvider(mock_callback)
        tok = token_provider.token

        self.assertEqual(tok, mock_token)
        mock_callback.assert_called_once()

    def test_token_reuse(self):
        mock_token = mock.MagicMock(
            alive_seconds=1
        )
        mock_callback = mock.MagicMock(return_value=mock_token)

        token_provider = SpotifyTokenProvider(mock_callback)
        # test that we can re-use the same token
        token1 = token_provider.token
        token2 = token_provider.token
        self.assertEqual(token1, token2)
        mock_callback.assert_called_once()


    def test_token_refresh(self):
        mock_token1 = mock.MagicMock(alive_seconds=1)
        mock_token2 = mock.MagicMock(alive_seconds=2)
        mock_callback = mock.MagicMock(side_effect=[mock_token1, mock_token2])

        token_provider = SpotifyTokenProvider(mock_callback)
        # test that we can will get new tokens correctly
        token1 = token_provider.token
        sleep(2)
        token2 = token_provider.token
        self.assertNotEqual(token1, token2)
        self.assertEqual(
            mock_callback.call_count, 2
        )

