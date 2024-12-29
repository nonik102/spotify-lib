import logging

from requests import Response
from fastapi import APIRouter, FastAPI

from spotify_lib.state import StateManager
from starlette.responses import RedirectResponse

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
        self._state_manager = state_manager

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



state_manager = StateManager()
app = FastAPI()
backend_api = App(state_manager)
app.include_router(backend_api.router)
