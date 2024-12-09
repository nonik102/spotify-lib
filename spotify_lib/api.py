from typing import Any

import requests
from requests import Request, Response, Session

from spotify_lib.common import SPOTIFY_SECRET_FILE_NAME, TOKEN_PATH, JsonBlob, Token
from spotify_lib.utils import SpotifySecret, SpotifySecretProvider

class CredentialsManager:

    def __init__(self, secret_provider: SpotifySecretProvider) -> None:
        self._secret_provider = secret_provider
        self._secret: SpotifySecret = self._load_credentials()

    def _load_credentials(self):
        return self._secret_provider.get_secret(SPOTIFY_SECRET_FILE_NAME)

    @property
    def client_id(self) -> str:
        return self._secret.client_id

    @property
    def secret(self) -> str:
        return self._secret.secret

class BaseAPI:
    def __init__(self) -> None:
        self._session = Session()

    @property
    def headers(self) -> JsonBlob:
        return JsonBlob({})

    @property
    def session(self) -> Session:
        # can add checking for if the session is still alive
        return self._session

    def _send(self, request: Request) -> Response:
        prepared = request.prepare()
        resp = self.session.send(prepared)
        return resp

    def _get(self, url: str, headers: dict | None = None, **kwargs: Any) -> Response:
        params = dict(kwargs)
        req = Request(
            method="GET", url=url, params=params, headers=self.headers | (headers or {})
        )
        resp = self._send(req)
        return resp

    def _post(
        self, url: str, data: JsonBlob, headers: dict | None = None, **kwargs: Any
    ) -> Response:
        params = dict(kwargs)
        req = Request(
            method="POST",
            url=url,
            params=params,
            headers=self.headers | (headers or {}),
            data=data,
        )
        resp = self._send(req)
        return resp


class SpotifyAPI(BaseAPI):
    def __init__(self, base_url: str, credentials: CredentialsManager) -> None:
        super().__init__()
        self._base_url = base_url
        self._creds = credentials

    def get_auth_token(self) -> Token:
        url = f"{self._base_url}/token"
        data = JsonBlob(
            {
                "grant_type": "client_credentials",
                "client_id": self._creds.client_id,
                "client_secret": self._creds.secret,
            }
        )
        resp = self._post(url, data)
        token_json = resp.json()
        return Token(
            value=token_json['access_token'],
            type=token_json['token_type'],
            alive_seconds=token_json['expires_in']
        )

def main():
    secret_provider = SpotifySecretProvider(TOKEN_PATH)
    creds = CredentialsManager(secret_provider)
    spotify_api = SpotifyAPI("https://accounts.spotify.com/api", creds)
    token = spotify_api.get_auth_token()
    print(token)


if __name__ == "__main__":
    main()
