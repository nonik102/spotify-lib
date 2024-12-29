
from spotify_lib.api.auth import SpotifyAuthAPI
from spotify_lib.common import Token
from spotify_lib.auth import ScopedSpotifyTokenProvider


class StateManager:
    def __init__(self) -> None:
        scopes = []
        auth_api = SpotifyAuthAPI()
        self._token_manager = ScopedSpotifyTokenProvider(auth_api, scopes)

    def get_token(self) -> Token:
        return self._token_manager.token

    def get_login_redirect_url(self) -> str:
        return self._token_manager.request_scoped_token()

    def handle_spotify_callback(self, code: str) -> None:
        self._token_manager.store_scoped_token(code)
