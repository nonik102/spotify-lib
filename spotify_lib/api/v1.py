from typing import Any
from spotify_lib.api._base import BaseAPI
from spotify_lib.common import Token, JsonBlob, SpotifyID, SpotifyItemType
from spotify_lib.auth import SpotifyTokenProvider

class SpotifyAPI(BaseAPI):
    def __init__(self, token_provider: SpotifyTokenProvider) -> None:
        super().__init__()
        self._base_url = "https://api.spotify.com/v1"
        self._token_provider = token_provider

    @property
    def _std_auth_headers(self) -> JsonBlob:
        base_headers = super().headers
        token = self._token_provider.token
        return JsonBlob(base_headers | {
            "Authorization": f"Bearer {token}"
        })

    def get_artist(self, artist_id: SpotifyID) -> JsonBlob:
        url = f"{self._base_url}/artists/{artist_id}"
        resp = self._get(url, headers=self._std_auth_headers)
        body = resp.json()
        return JsonBlob(body)

    def get_album(self, album_id: SpotifyID) -> JsonBlob:
        url = f"{self._base_url}/albums/{album_id}"
        resp = self._get(url, headers=self._std_auth_headers)
        body = resp.json()
        return JsonBlob(body)

    def get_track(self, track_id: SpotifyID) -> JsonBlob:
        url = f"{self._base_url}/tracks/{track_id}"
        resp = self._get(url, headers=self._std_auth_headers)
        body = resp.json()
        return JsonBlob(body)

    def search(self, query: str, desired_types: list[SpotifyItemType]) -> JsonBlob:
        url = f"{self._base_url}/search"
        params = {
            "q": query,
            "type": desired_types
        }
        resp = self._get(url, headers=self._std_auth_headers, params=params)
        body = resp.json()
        return JsonBlob(body)

    def _play(
        self,
        context_uri: SpotifyID | None = None,
        uris: list[SpotifyID] | None = None,
        offset: Any | None = None,
        position_ms: int  = 0,
        device_id: str | None = None
    ) -> None:
        url = f"{self._base_url}/me/player/play"
        params = {}
        if device_id is not None:
            params['device_id'] = device_id
        body: dict[str, Any] = {
            "position_ms": position_ms
        }
        if context_uri is not None:
            body['context_uri'] = context_uri
        if uris is not None:
            body['uris'] = uris
        if offset is not None:
            body['offset'] = offset
        headers = self._std_auth_headers | {"Content-Type": "application/json"}
        self._put(
            url, headers=headers, params=params, data=body
        )
