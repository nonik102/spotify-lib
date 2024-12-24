from spotify_lib.api._base import BaseAPI
from spotify_lib.common import JsonBlob, Token

class SpotifyAuthAPI(BaseAPI):
    def __init__(self) -> None:
        super().__init__()
        self._base_url = "https://accounts.spotify.com"

    def get_auth_token(self, payload: JsonBlob, headers: JsonBlob | None = None) -> Token:
        url = f"{self._base_url}/api/token"
        resp = self._post(
            url,
            data=payload,
            headers=self.headers | (headers or {})
        )
        token_json = resp.json()
        return Token(
            value=token_json['access_token'],
            type=token_json['token_type'],
            alive_seconds=token_json['expires_in'],
            scopes=[]
        )

    def start_user_auth(self, params: JsonBlob) -> str:
        url = f"{self._base_url}/authorize"
        resp = self._get(url, params=params)
        return resp.url

def main():
    params = {
        "response_type": "code",
        "client_id": "2cb8cf45c61b4adba65390250e7b62dd",
        "scope": "user-read-private user-read-email",
        "redirect_uri": "https://localhost:8000",
        "state": "123"
    }
    api = SpotifyAuthAPI()
    api.start_user_auth(JsonBlob(params))

if __name__ == "__main__":
    main()
