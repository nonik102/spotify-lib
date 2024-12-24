from __future__ import annotations

from dataclasses import dataclass

from datetime import datetime, timedelta
from typing import override
from uuid import uuid4

from spotify_lib.api.auth import SpotifyAuthAPI
from spotify_lib.common import SPOTIFY_REDIRECT_URI, JsonBlob, Scope, Token


SPOTIFY_SECRET_FILE_PATH = "/home/nonik/.tokens/spotify_api.tok"

class _SpotifyTokenProvider:
    def __init__(self, api: SpotifyAuthAPI) -> None:
        self._api = api
        self._token_death_time = datetime.min
        self._secret = self.get_secret()
        self._token: Token | None = None

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
        raise NotImplementedError()

    @staticmethod
    def get_secret() -> SpotifySecret:
        with open(SPOTIFY_SECRET_FILE_PATH, 'r', encoding="utf-8") as fp:
            client_id = fp.readline().strip('\n')
            secret = fp.readline().strip('\n')
        return SpotifySecret(client_id, secret)


class SpotifyTokenProvider(_SpotifyTokenProvider):
    def _refresh_token(self) -> None:
        data = JsonBlob({
            "grant_type": "client_credentials",
            "client_id": self._secret.client_id,
            "client_secret": self._secret.secret,
        })
        self._token = self._api.get_auth_token(data)
        # reset death time
        self._token_death_time = datetime.now() + timedelta(seconds=self._token.alive_seconds)

class ScopedSpotifyTokenProvider(_SpotifyTokenProvider):
    def __init__(self, api: SpotifyAuthAPI, scopes: list[Scope]) -> None:
        super().__init__(api)
        self._scopes = scopes
        self._reauth_token: Token | None = None

    @override
    def _refresh_token(self) -> None:
        state = str(uuid4())
        params = JsonBlob({
            "response_type": "code",
            "client_id": self._secret.client_id,
            "scope": " ".join(self._scopes),
            "redirect_uri": SPOTIFY_REDIRECT_URI,
            "state": state
        })
        resp = self._api.start_user_auth(params)


@dataclass
class SpotifySecret:
    client_id: str
    secret: str

if __name__ == "__main__":
    api = SpotifyAuthAPI()
    token_provider = ScopedSpotifyTokenProvider(api, scopes=[Scope("user-read-private")])
    tok = token_provider.token

