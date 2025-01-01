from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import NewType

SPOTIFY_SECRET_FILE_NAME="spotify_api"
SPOTIFY_CALLBACK_URI = "http://localhost:8000/callback"
SPOTIFY_LOGIN_URL = "http://localhost:8000/login"
LOCAL_API_URL = "http://localhost:8000"

JsonBlob = NewType("JsonBlob", dict)
SpotifyID = NewType("SpotifyID", str)
SpotifyURI = NewType("SpotifyURI", str)
Scope = NewType("Scope", str)

class SpotifyItemType(Enum):
    ALBUM = "album"
    ARTIST = "artist"
    PLAYLIST = "playlist"
    TRACK = "track"
    SHOW = "show"
    EPISODE = "episode"
    AUDIOBOOK = "audiobook"

    def __str__(self) -> str:
        return self.value

@dataclass
class Token:
    value: str
    type: str
    alive_seconds: int
    scopes: list[Scope]
    refresh_token: str | None

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_json(cls, token_json: JsonBlob) -> Token:
        return Token(
            value=token_json['access_token'],
            type=token_json['token_type'],
            alive_seconds=token_json['expires_in'],
            scopes=[
                Scope(scope_str) for scope_str
                in token_json.get('scope', "").strip().split(" ")
                if token_json.get('scope')
            ],
            refresh_token=token_json.get('refresh_token')
        )
