from dataclasses import dataclass
from typing import NewType

SPOTIFY_SECRET_FILE_NAME="spotify_api"

JsonBlob = NewType("JsonBlob", dict)
SpotifyID = NewType("SpotifyID", int)

@dataclass
class Token:
    value: str
    type: str
    alive_seconds: int
