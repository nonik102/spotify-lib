from fastapi import FastAPI

from spotify_lib.common import JsonBlob, Token

app = FastAPI()

class CallbackError(Exception):
    pass

# TODO: add XSRF-Token checking

user_token: Token | None = None

@app.get("/")
def read_root() -> JsonBlob:
    return {"Hello": "World"}

@app.get("/callback")
def callback(code: str | None, state: str | None, error: str | None) -> None:
    if error:
        raise CallbackError(error)
    if code:
        # we succeeded

    breakpoint()
    print(code)
