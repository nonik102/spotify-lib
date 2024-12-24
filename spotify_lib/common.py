from dataclasses import dataclass
from enum import Enum
from typing import NewType

SPOTIFY_SECRET_FILE_NAME="spotify_api"
SPOTIFY_REDIRECT_URI = "http://localhost:8000/callback"

JsonBlob = NewType("JsonBlob", dict)
SpotifyID = NewType("SpotifyID", str)
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

    def __str__(self) -> str:
        return self.value
