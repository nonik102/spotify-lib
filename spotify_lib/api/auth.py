from spotify_lib.api._base import BaseAPI
from spotify_lib.common import JsonBlob, Token

class SpotifyAuthAPI(BaseAPI):
    def __init__(self) -> None:
        super().__init__()
        self._base_url = "https://accounts.spotify.com/api"

    def get_auth_token(self, payload: JsonBlob) -> Token:
        url = f"{self._base_url}/token"
        resp = self._post(url, payload)
        token_json = resp.json()
        return Token(
            value=token_json['access_token'],
            type=token_json['token_type'],
            alive_seconds=token_json['expires_in']
        )

    def start_user_auth(self, params: JsonBlob) -> Token:
        url = f"{self._base_url}/authorize"
        self._get(url, params=params)

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
