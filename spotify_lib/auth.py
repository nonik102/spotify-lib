from __future__ import annotations

import base64
from dataclasses import dataclass

from datetime import datetime, timedelta
from typing import override
from uuid import uuid4

from spotify_lib.api.auth import SpotifyAuthAPI
from spotify_lib.common import SPOTIFY_LOGIN_URL, SPOTIFY_CALLBACK_URI, JsonBlob, Scope, Token


SPOTIFY_SECRET_FILE_PATH = "/home/nonik/.tokens/spotify_api.tok"

class AuthorizationError(Exception):
    pass

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

    def get_basic_auth(self) -> str:
        client_id = self._secret.client_id
        secret = self._secret.secret
        secret_string = f"{client_id}:{secret}".encode("ascii")
        encoded = base64.b64encode(secret_string)
        return f"Basic {encoded.decode()}"

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
        token_json = self._api.get_token(data)
        self._token = Token.from_json(token_json)
        print(token_json)
        # reset death time
        self._token_death_time = datetime.now() + timedelta(seconds=self._token.alive_seconds)

class ScopedSpotifyTokenProvider(_SpotifyTokenProvider):
    def __init__(self, api: SpotifyAuthAPI, scopes: list[Scope]) -> None:
        super().__init__(api)
        self._scopes = scopes

    def request_scoped_token(self) -> str:
        state = str(uuid4())
        params = JsonBlob({
            "response_type": "code",
            "client_id": self._secret.client_id,
            "scope": " ".join(self._scopes),
            "redirect_uri": SPOTIFY_CALLBACK_URI,
            "state": state
        })
        redirect_url = self._api.authorize(params)
        return redirect_url

    def store_scoped_token(self, code: str) -> None:
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": SPOTIFY_CALLBACK_URI
        }
        headers = {
            "Authorization": self.get_basic_auth(),
            "content-type": "application/x-www-form-urlencoded"
        }
        token_json = self._api.get_token(
            payload=JsonBlob(payload), headers=JsonBlob(headers)
        )
        self._token = Token.from_json(token_json)
        # reset death time
        self._token_death_time = datetime.now() + timedelta(seconds=self._token.alive_seconds)

    @override
    def _refresh_token(self) -> None:
        if self._token is None:
            raise AuthorizationError(
                f"please log in to spotify by going to the url {SPOTIFY_LOGIN_URL}"
            )
        params = JsonBlob({
            "grant_type": "refresh_token",
            "refresh_token": self._token.refresh_token
        })
        token_json = self._api.get_token(params)
        self._token = Token.from_json(token_json)
        # reset death time
        self._token_death_time = datetime.now() + timedelta(seconds=self._token.alive_seconds)


@dataclass
class SpotifySecret:
    client_id: str
    secret: str

