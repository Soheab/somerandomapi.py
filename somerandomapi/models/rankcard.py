from typing import Literal

from .. import utils as _utils
from ..internals.endpoints import Premium
from .abc import BaseImageModel, attribute

__all__ = ("Rankcard",)


class Rankcard(BaseImageModel):
    """Represents a rank card."""

    __endpoint__ = Premium.RANK_CARD

    template: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9]
    """The template to use. Must be a number between 1 and 9.
    
    .. versionadded:: 0.1.0
    """
    username: str = attribute(max_length=32)
    """The username of the user. Max 32 characters."""
    avatar_url: str = attribute(data_name="avatar")
    """The avatar URL of the user. Must be .png or .jpg."""
    level: int
    """The current level of the user."""
    current_xp: int = attribute(data_name="cxp")
    """The current XP of the user."""
    needed_xp: int = attribute(data_name="nxp")
    """The needed XP to level up."""
    discriminator: int | None = attribute(default=None, min_length=1, max_length=4, forced_type=str)
    """The discriminator of the user.
    
    Will be stripped if equal to 0
    """
    background_url: str | None = attribute(default=None, data_name="bg")
    """The custom background of the rank card as url. Tier 2+ key required.
    
    This cannot be used with background_color.
    """
    background_color: str | None = attribute(default=None, data_name="cbg")
    """The custom background color of the rank card. Tier 1+ key required.

    Can put "random" to get a random color.
    
    This cannot be used with background.
    """
    text_color: str | None = attribute(default=None, data_name="ctext")
    """The custom text color of the rank card as hex.
    
    Can put "random" to get a random color.
    """
    current_xp_color: str | None = attribute(default=None, data_name="ccxp")
    """The color of the current XP as hex.

    Can put "random" to get a random color.
    """
    xp_bar_color: str | None = attribute(default=None, data_name="cbar")
    """The color of the XP bar as hex.

    Can put "random" to get a random color.
    """
    username_color: str | None = attribute(default=None, data_name="ctag")
    """The color of the username as hex.

    Can put "random" to get a random color.

    .. versionadded:: 0.1.0
    
    """

    def __post_init__(self) -> None:
        COLOR_ERROR = "Invalid {0} color. Must be a valid hex color or 'random'. Valid formats: '#000000', 0x000000, 000000"
        if self.background_color is not None:
            if not (color := _utils._check_colour_value(self.background_color)):
                raise ValueError(COLOR_ERROR.format("background"))
            self.background_color = color
        if self.text_color is not None:
            if not (color := _utils._check_colour_value(self.text_color)):
                raise ValueError(COLOR_ERROR.format("text"))
            self.text_color = color
        if self.current_xp_color is not None:
            if not (color := _utils._check_colour_value(self.current_xp_color)):
                raise ValueError(COLOR_ERROR.format("current xp"))
            self.current_xp_color = color
        if self.xp_bar_color is not None:
            if not (color := _utils._check_colour_value(self.xp_bar_color)):
                raise ValueError(COLOR_ERROR.format("xp bar"))
            self.xp_bar_color = color
        if self.username_color is not None:
            if not (color := _utils._check_colour_value(self.username_color)):
                raise ValueError(COLOR_ERROR.format("username"))
            self.username_color = color

        super().__post_init__()
