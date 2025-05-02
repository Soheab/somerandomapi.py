from typing import Literal, Self

from ..enums import ResultType
from .abc import BaseModel

__all__ = ("EncodeResult",)


class EncodeResult(BaseModel, frozen=True, validate_types=False):
    """Represents the result of an encoding."""

    _type: Literal["ENCODE", "DECODE"]

    name: Literal["BASE64", "BINARY"]
    """The name of the encoding."""
    input: str
    """The input text."""
    text: str
    """The encoded/decoded text."""

    def __str__(self) -> str:
        return self.text

    @property
    def type(self) -> ResultType:
        """The type of the result."""
        return ResultType(self._type)

    def to_dict(self) -> dict[Literal["encode", "decode"], str]:
        """Converts this model to a dictionary."""
        return {self._type.lower(): self.input}  # pyright: ignore[reportReturnType]

    @classmethod
    def from_dict(
        cls, _input: str, _type: Literal["ENCODE", "DECODE"], name: Literal["BASE64", "BINARY"], text: str
    ) -> Self:
        """Converts a dictionary to this model."""
        return cls(
            _type=_type,
            name=name,
            input=_input,
            text=text,
        )
