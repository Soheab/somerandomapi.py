import asyncio
import json

import pytest

from somerandomapi import utils as _utils
from somerandomapi.errors import BadRequest, Forbidden, HTTPException, ImageError, NotFound, RateLimited
from somerandomapi.internals.endpoints import Base
from somerandomapi.internals.http import HTTPClient, json_or_text
from somerandomapi.models.image import Image


class FakeResponse:
    def __init__(self, status=200, content_type="application/json", payload=None, body=b"img") -> None:
        self.status = status
        self.content_type = content_type
        self._payload = payload if payload is not None else {}
        self._body = body

    async def text(self, encoding="utf-8"):
        if self.content_type == "application/json":
            return json.dumps(self._payload)
        return str(self._payload)

    async def read(self):
        return self._body


class _CM:
    def __init__(self, response):
        self.response = response

    async def __aenter__(self):
        return self.response

    async def __aexit__(self, *_):
        return None


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.headers = {}
        self.closed = False
        self.last_url = None

    def get(self, url):
        self.last_url = url
        return _CM(self.responses.pop(0))

    async def close(self):
        self.closed = True


def _run(coro):
    return asyncio.run(coro)


def test_json_or_text() -> None:
    j = _run(json_or_text(FakeResponse(payload={"a": 1})))
    assert j == {"a": 1}
    t = _run(json_or_text(FakeResponse(content_type="text/plain", payload="hello")))
    assert t == "hello"


def _client_with_session(session: FakeSession) -> HTTPClient:
    return HTTPClient(token="abc", session=session)


def test_request_success_json_and_image() -> None:
    json_session = FakeSession([FakeResponse(payload={"ok": True})])
    http = _client_with_session(json_session)
    data = _run(http.request(Base.JOKE))
    assert data == {"ok": True}

    img_session = FakeSession([FakeResponse(content_type="image/png")])
    http2 = _client_with_session(img_session)
    data2 = _run(http2.request(Base.JOKE))
    assert isinstance(data2, Image)


def test_request_error_mapping() -> None:
    mapping = [
        (400, BadRequest),
        (403, Forbidden),
        (404, NotFound),
        (429, RateLimited),
        (500, AttributeError),
        (418, HTTPException),
    ]
    for status, exc_type in mapping:
        session = FakeSession([FakeResponse(status=status, payload={"message": "x"})])
        http = _client_with_session(session)
        with pytest.raises(exc_type):
            _run(http.request(Base.JOKE))


def test_request_200_with_error_field_raises_bad_request() -> None:
    session = FakeSession([FakeResponse(status=200, payload={"error": "bad"})])
    http = _client_with_session(session)
    with pytest.raises(BadRequest):
        _run(http.request(Base.JOKE))


def test_get_image_url_and_close() -> None:
    session = FakeSession([FakeResponse(status=200, content_type="image/png", body=b"abc")])
    http = _client_with_session(session)
    assert _run(http._get_image_url("https://x")) == b"abc"

    session2 = FakeSession([FakeResponse(status=404, content_type="image/png")])
    http2 = _client_with_session(session2)
    with pytest.raises(ImageError):
        _run(http2._get_image_url("https://x"))

    # close only closes non-user-provided sessions
    real = HTTPClient(token=None, session=_utils.NOVALUE)
    fake = FakeSession([])
    real._session = fake
    _run(real.close())
    assert fake.closed
