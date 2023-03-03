from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from dataclasses import Field

    from .models.abc import BaseModel


__all__ = (
    "SomeRandomApiException",
    "BadRequest",
    "NotFound",
    "InternalServerError",
    "Forbidden",
    "HTTPException",
    "RateLimited",
    "ImageError",
    "TypingError",
)


class SomeRandomApiException(Exception):
    """Base exception for all errors raised by this library.

    Attributes
    ----------
    data: Any
        The data returned by the API.
    enum: ``BaseEndpoint``
        The enum category that the endpoint is a part of.
    endpoint: ``Endpoint``
        The endpoint that was called.
    """

    def __init__(self, enum, data: Any, /):
        self.data: Any = data
        self.endpoint = enum.value

        self.message = f"{str(data)}"
        if isinstance(data, dict):
            try:
                self.message = data["error"]
            except KeyError:
                pass

            try:
                self.code = data["code"]
            except KeyError:
                self.code = getattr(self.__class__, "code", 0)

            self.message += f" (Code: {self.code})"

        super().__init__(f"While requesting /{self.endpoint.path or enum.base()}: {self.message}")


class BadRequest(SomeRandomApiException):
    """``Bad Request`` error."""

    code = 400


class NotFound(SomeRandomApiException):
    """``Not Found`` error."""

    code = 404


class InternalServerError(SomeRandomApiException):
    """``Internal Server Error`` error."""

    def __init__(self, enum, data: Any, /):
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

    def __init__(self, enum, response, data: Any, /):
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
    """Exception raised when an image could not be retrieved.

    Attributes
    ----------
    url: str
        The URL of the image.
    status: int
        The status code of the response.
    """

    def __init__(self, url: str, status: int, /):
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
    field: :class:`dataclasses.Field`
        The field that the error occurred in. Use ``field.name`` to get the name of the field (argument).
    """

    def __init__(
        self, cls: BaseModel, field: Field, value: Any, *, message: Optional[str] = None, **format_kwarg: Any
    ) -> None:
        self.cls: BaseModel = cls
        self.field: Field = field
        message = message or "{field_name} must be of type {field_type}, not {current_type}."
        message = message.format(
            field_name=f"'{field.name}'",
            class_name=f"{cls.__class__.__name__}()",
            field_type=field.type.__class__.__name__,
            current_type=type(value).__name__,
            field_value=value,
            field_value_type=type(value).__name__,
            **format_kwarg,
        )
        super().__init__(f"Error in class: {cls.__class__.__name__}() and argument: '{field.name}': {message}")
