from __future__ import annotations

from typing import TYPE_CHECKING, Any
import contextlib

from . import utils as _utils

if TYPE_CHECKING:
    from .internals.endpoints import Endpoint
    from .models.abc import BaseModel


__all__ = (
    "BadRequest",
    "Forbidden",
    "HTTPException",
    "ImageError",
    "InternalServerError",
    "NotFound",
    "RateLimited",
    "SomeRandomApiException",
    "TypingError",
)


class SomeRandomApiException(Exception):
    """Base exception for all errors raised by this library.

    Attributes
    ----------
    data: Any
        The data returned by the API.
    endpoint: ``Endpoint``
        The endpoint that was called.
        Use ``endpoint.path`` to get the full path of the endpoint.
    """

    def __init__(self, endpoint: Endpoint, data: Any, /) -> None:
        self.data: Any = data
        self.endpoint: Endpoint = endpoint

        self.message = f"{data!s}"
        if isinstance(data, dict):
            with contextlib.suppress(KeyError):
                self.message = data["error"]

            try:
                self.code = data["code"]
            except KeyError:
                self.code = getattr(self.__class__, "code", 0)

            self.message += f" (Code: {self.code})"

        super().__init__(f"While requesting /{endpoint.path}: {self.message}")


class BadRequest(SomeRandomApiException):
    """``Bad Request`` error."""

    code = 400


class NotFound(SomeRandomApiException):
    """``Not Found`` error."""

    code = 404


class InternalServerError(SomeRandomApiException):
    """``Internal Server Error`` error."""

    def __init__(self, enum, data: Any, /) -> None:
        Exception.__init__(self, f"Internal Server Error while requesting {enum.base()}{enum.value.path}.")


class Forbidden(SomeRandomApiException):
    """``Forbidden`` error."""

    code = 403


class RateLimited(SomeRandomApiException):
    """``Too Many Requests`` error."""

    code = 429


class HTTPException(SomeRandomApiException):
    """Exception raised when an HTTP request fails."""

    response: Any
    data: Any
    message: str
    code: int

    def __init__(self, enum, response, data: Any, /) -> None:
        self.response = response
        self.data = data
        if isinstance(data, dict):
            with contextlib.suppress(KeyError):
                self.message = data["error"]
            try:
                self.code = data["code"]
            except KeyError:
                self.code = response.status
        else:
            self.message = str(data)
            self.code = response.status

        super().__init__(enum, data)


class ImageError(SomeRandomApiException):
    """Exception raised when an image could not be retrieved.

    Attributes
    ----------
    url: str
        The URL of the image.
    status: int
        The status code of the response.
    """

    def __init__(self, url: str, status: int, /) -> None:
        self.url: str = url
        self.status: int = status
        Exception.__init__(self, f"Could not get image from {url} (code: {status})")


class TypingError(TypeError):
    """Exception raised when a typing error occurs.

    This is usually raised in a dataclass when a type is not what it is supposed to be.

    Attributes
    ----------
    cls: ``BaseModel``
        The class that the error occurred in.
    attribute: :class:`Attribute`
        The attribute that the error occurred in. Use ``attribute.name`` to get the name of the attribute (argument).
    """

    def __init__(
        self,
        cls: BaseModel,
        attribute: Any,
        value: Any,
        *,
        message: str | None = None,
        cast_type: bool = True,
        **format_kwarg: Any,
    ) -> None:
        self.cls: BaseModel = cls
        self.attribute: Any = attribute
        message = message or "{field_name} must be of type {field_type} not {current_type}."

        field_value_type = type(value) if cast_type else value
        message = message.format(
            field_name=f"'{attribute.name}'",
            class_name=f"{cls.__class__.__name__}()",
            field_type=_utils._get_type(attribute.type, {}, {})[0],
            current_type=type(value).__name__,
            field_value=value,
            field_value_type=repr(field_value_type),
            **format_kwarg,
        )
        self.error_message: str = message
        super().__init__(f"Error in class: {cls.__class__.__name__}() and argument: '{attribute.name}': {message}")
