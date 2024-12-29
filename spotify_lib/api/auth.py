from spotify_lib.api._base import BaseAPI
from spotify_lib.common import JsonBlob

class SpotifyAuthAPI(BaseAPI):
    def __init__(self) -> None:
        super().__init__()
        self._base_url = "https://accounts.spotify.com"

    def get_token(self, payload: JsonBlob, headers: JsonBlob | None = None) -> JsonBlob:
        url = f"{self._base_url}/api/token"
        resp = self._post(
            url,
            data=payload,
            headers=self.headers | (headers or {})
        )
        token_json = resp.json()
        return token_json

    def authorize(self, params: JsonBlob) -> str:
        url = f"{self._base_url}/authorize"
        resp = self._get(url, params=params)
        return resp.url

