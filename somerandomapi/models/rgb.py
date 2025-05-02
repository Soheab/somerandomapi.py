from typing import Literal
from collections.abc import Iterator

from .abc import BaseModel

__all__ = ("RGB",)


class RGB(BaseModel, frozen=True, validate_types=False):
    """Represents an RGB color."""

    r: int
    """The red value of the color."""
    g: int
    """The green value of the color."""
    b: int
    """The blue value of the color."""

    @property
    def as_tuple(self) -> tuple[int, int, int]:
        """Returns the RGB values as a tuple."""
        return self.r, self.g, self.b

    def __repr__(self) -> str:
        return f"rgb{self.as_tuple}"

    def __iter__(self) -> Iterator[int]:
        return iter(self.as_tuple)

    def to_dict(self) -> dict[Literal["r", "g", "b"], int]:
        """Converts the RGB color to a dictionary."""
        return {"r": self.r, "g": self.g, "b": self.b}
