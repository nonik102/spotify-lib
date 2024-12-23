from typing import Any

import requests
from requests import Request, Response, Session
from requests.models import HTTPError

from spotify_lib.common import JsonBlob, SpotifyID, SpotifyItemType, Token
from spotify_lib.auth import SpotifyTokenProvider

class APIError(Exception):
    pass

class BaseAPI:
    def __init__(self) -> None:
        self._session = Session()

    @property
    def headers(self) -> JsonBlob:
        return JsonBlob({})

    @property
    def session(self) -> Session:
        return self._session

    def _send(self, request: Request) -> Response:
        prepared = request.prepare()
        resp = self.session.send(prepared)
        try:
            resp.raise_for_status()
        except HTTPError as e:
            raise APIError(e) from e
        return resp

    def _get(
        self, url: str,
        headers: dict | None = None, params: dict[str, str] | None = None
    ) -> Response:
        req = Request(
            method="GET", url=url, params=params, headers=self.headers | (headers or {})
        )
        resp = self._send(req)
        return resp

    def _post(
        self, url: str, data: JsonBlob,
        headers: dict | None = None, params: dict[str, str] | None = None
    ) -> Response:
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
    def __init__(self, base_url: str) -> None:
        super().__init__()
        self._base_url = base_url
        self._token_provider = SpotifyTokenProvider(self._get_auth_token)

    # auth stuff ########################################################
    def _get_auth_token(self, payload: JsonBlob) -> Token:
        url = "https://accounts.spotify.com/api/token"
        resp = self._post(url, payload)
        token_json = resp.json()
        return Token(
            value=token_json['access_token'],
            type=token_json['token_type'],
            alive_seconds=token_json['expires_in']
        )

    @property
    def token(self) -> Token:
        return self._token_provider.token

    @property
    def auth_headers(self) -> JsonBlob:
        base_headers = super().headers
        return JsonBlob(base_headers | {
            "Authorization": f"Bearer {self.token}"
        })

    # api stuff #########################################################
    def get_artist(self, artist_id: SpotifyID) -> JsonBlob:
        url = f"{self._base_url}/artists/{artist_id}"
        resp = self._get(url, headers=self.auth_headers)
        body = resp.json()
        return JsonBlob(body)

    def get_album(self, album_id: SpotifyID) -> JsonBlob:
        url = f"{self._base_url}/albums/{album_id}"
        resp = self._get(url, headers=self.auth_headers)
        body = resp.json()
        return JsonBlob(body)

    def get_track(self, track_id: SpotifyID) -> JsonBlob:
        url = f"{self._base_url}/tracks/{track_id}"
        resp = self._get(url, headers=self.auth_headers)
        body = resp.json()
        return JsonBlob(body)

    def search(self, query: str, desired_types: list[SpotifyItemType]) -> JsonBlob:
        url = f"{self._base_url}/search"
        params = {
            "q": query,
            "type": desired_types
        }
        resp = self._get(url, headers=self.auth_headers, params=params)
        body = resp.json()
        return JsonBlob(body)

