from __future__ import annotations
from typing import TYPE_CHECKING, Literal, Tuple, Dict

from dataclasses import dataclass

from ..enums import ResultType

if TYPE_CHECKING:
    from typing_extensions import Self


__all__: Tuple[str, ...] = ("EncodeResult",)


@dataclass
class EncodeResult:
    """Represents the result of an encoding."""

    _type: Literal["ENCODE", "DECODE"]

    name: Literal["BASE64", "BINARY"]
    """The name of the encoding."""
    input: str
    """The input text."""
    text: str
    """The encoded/decoded text."""

    @property
    def type(self) -> ResultType:
        """The type of the result."""
        return ResultType(self._type)

    def to_dict(self) -> Dict[Literal["encode", "decode"], str]:
        """Converts this model to a dictionary."""
        return {self._type.lower(): self.input}  # type: ignore

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
