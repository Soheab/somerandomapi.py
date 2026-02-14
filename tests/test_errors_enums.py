import pytest

from somerandomapi import enums
from somerandomapi.errors import (
    BadRequest,
    HTTPException,
    ImageError,
    InternalServerError,
    SomeRandomApiException,
)
from somerandomapi.internals.endpoints import Base
from somerandomapi.models.rankcard import Rankcard


class _Resp:
    def __init__(self, status: int) -> None:
        self.status = status


def test_base_enum_str() -> None:
    assert str(enums.TweetTheme.LIGHT) == "light"
    assert str(enums.ResultType.ENCODE) == "ENCODE"


def test_base_exception_formats() -> None:
    exc = SomeRandomApiException(Base.JOKE, {"error": "bad", "code": 400})
    assert "While requesting /joke" in str(exc)
    assert "bad" in str(exc)

    bad = BadRequest(Base.JOKE, {"error": "oops"})
    assert "Code:" in str(bad)


def test_http_exception_and_image_error() -> None:
    exc = HTTPException(Base.JOKE, _Resp(418), "teapot")
    assert exc.code == 418
    assert "teapot" in str(exc)

    img = ImageError("https://img", 404)
    assert img.url == "https://img"
    assert img.status == 404


def test_internal_server_error_message() -> None:
    with pytest.raises(AttributeError):
        InternalServerError(Base.JOKE, {})


def test_rankcard_color_validation() -> None:
    rc = Rankcard(
        template=1,
        username="user",
        avatar_url="https://img",
        level=1,
        current_xp=1,
        needed_xp=2,
        background_color="#00ff00",
    )
    assert rc.background_color == "00ff00"

    with pytest.raises(ValueError):
        Rankcard(
            template=1,
            username="user",
            avatar_url="https://img",
            level=1,
            current_xp=1,
            needed_xp=2,
            background_color="zzzzzz",
        )
