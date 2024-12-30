import logging

from fastapi import APIRouter, FastAPI

from spotify_lib.api.v1 import SpotifyAPI
from spotify_lib.state import StateManager
from starlette.responses import RedirectResponse
from spotify_lib.common import SpotifyID, SpotifyItemType

logger = logging.getLogger(__name__)


class CallbackError(Exception):
    pass

# TODO: add XSRF-Token checking

class App:
    def __init__(self, state_manager: StateManager) -> None:
        self.router = APIRouter()
        self.router.add_api_route(
            "/login", self.login, methods=["GET"]
        )
        self.router.add_api_route(
            "/callback", self.callback, methods=["GET"]
        )
        self.router.add_api_route(
            "/token", self.token, methods=["GET"]
        )
        self.router.add_api_route(
            "/play", self.play, methods=["GET"]
        )
        self.router.add_api_route(
            "/play_album", self.play_album, methods=["GET"]
        )
        self._state_manager = state_manager
        self._std_api = SpotifyAPI(state_manager._token_manager)

    def login(self):
        redirect_url = self._state_manager.get_login_redirect_url()
        response = RedirectResponse(url=redirect_url)
        return response

    def callback(self, code: str | None = None, state: str | None = None, error: str | None = None) -> None:
        if error:
            raise CallbackError(error)
        if not code:
            raise CallbackError("No code received")
        self._state_manager.handle_spotify_callback(code)

    def token(self):
        return self._state_manager.get_token()

    def play(self, uri: SpotifyID) -> None:
        self._std_api._play(
            context_uri=uri
        )

    def play_album(self, name: str) -> None:
        search_result = self._std_api.search(
            query=name,
            desired_types=[SpotifyItemType.ALBUM]
        )
        albums = search_result['albums']['items']
        album_uri = albums[0]['uri']
        self._std_api._play(
            context_uri=album_uri,
            offset={"position": 0}
        )



state_manager = StateManager()
app = FastAPI()
backend_api = App(state_manager)
app.include_router(backend_api.router)
