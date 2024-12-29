import unittest
from unittest import mock
from time import sleep
from typing import Any

from spotify_lib.auth import SpotifyTokenProvider

class TestTokenProvider(unittest.TestCase):
    def _get_mock_token(self, alive_seconds: int) -> Any:
        mock_token = {
            "access_token": "token_value",
            "expires_in": alive_seconds,
            "token_type": "test",
        }
        return mock_token

    def test_get_token(self):
        mock_token = self._get_mock_token(alive_seconds=10)
        mock_api = mock.MagicMock()
        mock_api.get_token = mock.MagicMock(return_value=mock_token)

        token_provider = SpotifyTokenProvider(mock_api)
        tok = token_provider.token

        self.assertIsNotNone(tok)
        mock_api.get_token.assert_called_once()

    def test_token_reuse(self):
        mock_token = self._get_mock_token(
            alive_seconds=1
        )
        mock_api = mock.MagicMock()
        mock_api.get_token = mock.MagicMock(return_value=mock_token)

        token_provider = SpotifyTokenProvider(mock_api)
        # test that we can re-use the same token
        token1 = token_provider.token
        token2 = token_provider.token
        self.assertEqual(token1, token2)
        mock_api.get_token.assert_called_once()


    def test_token_refresh(self):
        mock_token1 = self._get_mock_token(alive_seconds=1)
        mock_token2 = self._get_mock_token(alive_seconds=2)
        mock_api = mock.MagicMock()
        mock_api.get_token = mock.MagicMock(side_effect=[mock_token1, mock_token2])

        token_provider = SpotifyTokenProvider(mock_api)
        # test that we can will get new tokens correctly
        token1 = token_provider.token
        sleep(2)
        token2 = token_provider.token
        self.assertNotEqual(token1, token2)
        self.assertEqual(
            mock_api.get_token.call_count, 2
        )

