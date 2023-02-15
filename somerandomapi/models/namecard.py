from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, Optional, Optional

from dataclasses import dataclass, field

from ..internals.endpoints import CanvasMisc
from .abc import BaseModel

if TYPE_CHECKING:
    from ..models.image import Image

__all__: Tuple[str, ...] = ("GenshinNamecard",)


@dataclass
class GenshinNamecard(BaseModel):
    """Represents a tweet."""

    _endpoint = CanvasMisc.GENSHIN_NAMECARD
    _image: Image = field(init=False)

    avatar: str
    """The avatar URL of the user. Must be .png or .jpg."""
    birthday: str
    """The birthday, dd/mm/yyyy"""
    username: str
    """The username"""
    description: Optional[str]
    """The description"""

    @property
    def image(self) -> Image:
        """The image of the namecard.

        Returns
        -------
        :class:`Image`
            The image of the namecard.
        """
        return self._image
