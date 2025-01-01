from requests.sessions import Session, Request
from requests import Response
from requests import HTTPError

from spotify_lib.common import JsonBlob

class APIError(Exception):
    pass

class BaseAPI:
    def __init__(self) -> None:
        self._session = Session()

    @property
    def headers(self) -> JsonBlob:
        return JsonBlob({})

    @property
    def session(self) -> Session:
        return self._session

    def _send(self, request: Request) -> Response:
        prepared = request.prepare()
        resp = self.session.send(prepared)
        try:
            resp.raise_for_status()
        except HTTPError as e:
            raise APIError(e) from e
        return resp

    def _get(
        self, url: str,
        headers: dict | None = None, params: dict[str, str] | None = None
    ) -> Response:
        req = Request(
            method="GET", url=url, params=params, headers=self.headers | (headers or {})
        )
        resp = self._send(req)
        return resp

    def _post(
        self, url: str, data: JsonBlob | None = None,
        headers: dict | None = None, params: dict[str, str] | None = None
    ) -> Response:
        if data == None:
            data = JsonBlob({})
        req = Request(
            method="POST",
            url=url,
            params=params,
            headers=self.headers | (headers or {}),
            data=data,
        )
        resp = self._send(req)
        return resp

    def _put(
        self, url: str, data: JsonBlob,
        headers: dict | None = None, params: dict[str, str] | None = None
    ) -> Response:
        req = Request(
            method="PUT",
            url=url,
            params=params,
            headers=self.headers | (headers or {}),
            json=data,
        )
        resp = self._send(req)
        return resp
