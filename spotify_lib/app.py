import logging
from fastapi import APIRouter, FastAPI
from uuid import uuid4
import base64

from spotify_lib.api.auth import SpotifyAuthAPI
from spotify_lib.auth import ScopedSpotifyTokenProvider
from spotify_lib.common import JsonBlob, Token, Scope, SPOTIFY_REDIRECT_URI
from starlette.responses import RedirectResponse

logger = logging.getLogger(__name__)


class CallbackError(Exception):
    pass

# TODO: add XSRF-Token checking

class App:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.router.add_api_route(
            "/login", self.login, methods=["GET"]
        )
        self.router.add_api_route(
            "/callback", self.callback, methods=["GET"]
        )
        # state
        self._auth_api = SpotifyAuthAPI()
        scopes = [Scope('user-read-email')]
        self._token_manager = ScopedSpotifyTokenProvider(self._auth_api, scopes)

    def login(self):
        state = str(uuid4())
        params = JsonBlob({
            "response_type": "code",
            "client_id": self._token_manager._secret.client_id,
            "scope": " ".join(self._token_manager._scopes),
            "redirect_uri": SPOTIFY_REDIRECT_URI,
            "state": state
        })
        redirect_url = self._auth_api.start_user_auth(params)
        response = RedirectResponse(url=redirect_url)
        return response

    def _get_basic_auth(self) -> str:
        client_id = self._token_manager._secret.client_id
        secret = self._token_manager._secret.secret
        secret_string = f"{client_id}:{secret}".encode("ascii")
        encoded = base64.b64encode(secret_string)
        return f"Basic: {encoded.decode()}"

    def callback(self, code: str | None = None, state: str | None = None, error: str | None = None) -> None:
        if error:
            raise CallbackError(error)
        if not code:
            raise CallbackError("No code received")
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": SPOTIFY_REDIRECT_URI
        }
        headers = {
            "Authorization": self._get_basic_auth(),
            "content-type": "application/x-www-form-urlencoded"
        }
        token = self._auth_api.get_auth_token(
            payload=JsonBlob(payload), headers=JsonBlob(headers)
        )
        print(token)


app = FastAPI()
backend_api = App()
app.include_router(backend_api.router)
