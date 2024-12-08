
from datetime import datetime, timedelta
from spotify_lib.api import SpotifyAPI
from spotify_lib.common import Token

class SpotifyTokenProvider:
    def __init__(self, spotify_api: SpotifyAPI) -> None:
        self._api = spotify_api
        self._token: Token | None = None
        self._token_death_time: datetime | None = None

    def _is_expired(self) -> bool:
        if not self._token_death_time:
            return True
        if datetime.now() > self._token_death_time:
            return True
        return False

    def refresh_token(self) -> None:
        token = self._api.get_auth_token()
        self._token = token
        self._token_death_time = datetime.now() + timedelta(seconds=token.alive_seconds)

    def get_token(self) -> Token:
        if self._token is None or self._is_expired():
            self.refresh_token()
        assert self._token is not None
        return self._token

