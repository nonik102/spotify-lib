from dataclasses import dataclass
from typing import NewType

SPOTIFY_SECRET_FILE_NAME="spotify_api"
TOKEN_PATH="/home/nonik/.tokens"

JsonBlob = NewType("JsonBlob", dict)

@dataclass
class Token:
    value: str
    type: str
    alive_seconds: int
