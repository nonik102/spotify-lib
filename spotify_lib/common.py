from dataclasses import dataclass
from typing import NewType

SPOTIFY_CLIENT_ID="2cb8cf45c61b4adba65390250e7b62dd"
SPOTIFY_SECRET="e7ed2693ef2044fda0c01cbd8464bcce"

JsonBlob = NewType("JsonBlob", dict)

@dataclass
class Token:
    value: str
    type: str
    alive_seconds: int
