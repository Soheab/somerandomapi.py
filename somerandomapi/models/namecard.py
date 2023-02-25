from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

from ..internals.endpoints import CanvasMisc
from .abc import BaseImageModel


__all__ = ("GenshinNamecard",)


@dataclass
class GenshinNamecard(BaseImageModel):
    """Represents a genshin namecard."""

    _endpoint = CanvasMisc.GENSHIN_NAMECARD

    avatar: str
    """The avatar URL of the user. Must be .png or .jpg."""
    birthday: str
    """The birthday, dd/mm/yyyy"""
    username: str
    """The username"""
    description: Optional[str]
    """The description"""

    if TYPE_CHECKING:

        @classmethod
        def from_dict(
            cls,
            *,
            avatar: str,
            birthday: str,
            username: str,
            description: Optional[str],
        ):
            ...

    def __post_init__(self):
        self.__class__._validate_types(self, globals(), locals())
