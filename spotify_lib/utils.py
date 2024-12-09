from dataclasses import dataclass
import os

from datetime import datetime, timedelta
from typing import IO
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


@dataclass
class SpotifySecret:
    client_id: str
    secret: str


class SpotifySecretProvider:
    """manage retrieval of spotify api secrets from disk"""

    def __init__(self, secret_dir: str) -> None:
        self._secret_dir = secret_dir

    def _secret_file(self, name: str) -> IO:
        # get the specified secret handle for read only
        secret_path = f"{self._secret_dir}{os.sep}{name}.tok"
        return open(secret_path, 'r', encoding='utf-8')

    def get_secret(self, name: str) -> SpotifySecret:
        with self._secret_file(name) as fp:
            client_id = fp.readline().strip('\n')
            secret = fp.readline().strip('\n')
        return SpotifySecret(client_id, secret)



def main():
    path="/home/nonik/.tokens"
    secret_provider = SpotifySecretProvider(path)
    secret = secret_provider.get_secret("spotify_api")
    print(secret)

if __name__ == "__main__":
    main()
