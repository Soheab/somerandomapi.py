from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, Dict, Literal

from dataclasses import dataclass

if TYPE_CHECKING:
    from typing_extensions import Self

__all__: Tuple[str, ...] = ("RGB",)


@dataclass
class RGB:
    """Represents an RGB color."""

    r: int
    """The red value of the color."""
    g: int
    """The green value of the color."""
    b: int
    """The blue value of the color."""

    @classmethod
    def from_dict(cls, data: Dict[Literal["r", "g", "b"], int]) -> Self:
        """Converts a dictionary to a RGB color.

        Parameters
        ----------
        data: :class:`dict`
            The dictionary to convert.

        Returns
        -------
        :class:`RGB`
            The RGB color.
        """
        return cls(**data)

    @property
    def to_tuple(self) -> tuple[int, int, int]:
        """Returns the RGB values as a tuple."""
        return self.r, self.g, self.b
