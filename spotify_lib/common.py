from dataclasses import dataclass
from typing import NewType

SPOTIFY_SECRET_FILE_NAME="spotify_api"

JsonBlob = NewType("JsonBlob", dict)
SpotifyID = NewType("SpotifyID", str)

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

    def __str__(self) -> str:
        return self.value
