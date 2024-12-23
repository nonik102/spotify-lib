from __future__ import annotations

from dataclasses import dataclass

from datetime import datetime, timedelta
from typing import Callable

from spotify_lib.common import JsonBlob, Token


SPOTIFY_SECRET_FILE_PATH = "/home/nonik/.tokens/spotify_api.tok"

class SpotifyTokenProvider:
    # TODO: Fix this to lazy-load
    def __init__(self, callback: Callable[[JsonBlob], Token]) -> None:
        self._callback = callback
        self._token_death_time = datetime.min
        self._secret = self.get_secret()
        self._token: Token | None = None
        self._token = self.token

    @property
    def token(self) -> Token:
        if self._token is None or self._is_expired():
            self._refresh_token()
        assert self._token is not None
        return self._token

    def _is_expired(self) -> bool:
        if not self._token_death_time:
            return True
        if datetime.now() > self._token_death_time:
            return True
        return False

    def _refresh_token(self) -> None:
        data = JsonBlob({
            "grant_type": "client_credentials",
            "client_id": self._secret.client_id,
            "client_secret": self._secret.secret,
        })
        self._token = self._callback(data)
        # reset death time
        self._token_death_time = datetime.now() + timedelta(seconds=self._token.alive_seconds)

    def get_secret(self) -> SpotifySecret:
        with open(SPOTIFY_SECRET_FILE_PATH, 'r', encoding="utf-8") as fp:
            client_id = fp.readline().strip('\n')
            secret = fp.readline().strip('\n')
        return SpotifySecret(client_id, secret)

@dataclass
class SpotifySecret:
    client_id: str
    secret: str

