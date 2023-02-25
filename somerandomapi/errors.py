from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from aiohttp import ClientResponse

    from .internals.endpoints import BaseEndpoint, Endpoint


__all__ = (
    "SomeRandomApiException",
    "BadRequest",
    "NotFound",
    "InternalServerError",
    "Forbidden",
    "HTTPException",
    "RateLimited",
    "ImageError",
)


class SomeRandomApiException(Exception):
    def __init__(self, enum: BaseEndpoint, data: Any, message: Optional[str] = None, /):
        self.data: Any = data
        self.endpoint: Endpoint = enum.value

        self.message = f"{str(data)}"
        if isinstance(data, dict):
            try:
                self.message = data["error"]
            except KeyError:
                pass

            try:
                self.code = data["code"]
            except KeyError:
                self.code = 0

            self.message += f" (Code: {self.code})"

        print("error cALLING", self.message, enum, self.endpoint, self.endpoint.path, enum.base())
        super().__init__(f"While requesting /{self.endpoint.path or enum.base()}: {self.message}")


class BadRequest(SomeRandomApiException):
    pass


class NotFound(SomeRandomApiException):
    def __init__(self, enum: BaseEndpoint, data: Any, /):
        Exception.__init__(self, f"Could not find {enum.base()}{enum.value.endpoint.path}.")


class InternalServerError(SomeRandomApiException):
    def __init__(self, enum: BaseEndpoint, data: Any, /):
        Exception.__init__(self, f"Internal Server Error while requesting {enum.base()}{enum.value.path}.")


class Forbidden(SomeRandomApiException):
    pass


class RateLimited(SomeRandomApiException):
    code = 429


class HTTPException(SomeRandomApiException):
    response: ClientResponse
    data: Any
    message: str
    code: int

    def __init__(self, enum: BaseEndpoint, response: ClientResponse, data: Any, /):
        self.response = response
        self.data = data
        if isinstance(data, dict):
            try:
                self.message = data["error"]
            except KeyError:
                pass
            try:
                self.code = data["code"]
            except KeyError:
                self.code = response.status
        else:
            self.message = str(data)
            self.code = response.status

        super().__init__(enum, data)


class ImageError(SomeRandomApiException):
    def __init__(self, url: str, status: int, /):
        self.url: str = url
        self.status: int = status
        Exception.__init__(self, f"Could not get image from {url} (code: {status})")
