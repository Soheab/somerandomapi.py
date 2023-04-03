from __future__ import annotations

import random
from typing import Literal, Optional, TYPE_CHECKING

from .. import utils as _utils
from ..enums import CanvasBorder, CanvasCrop, CanvasFilter, CanvasOverlay
from ..internals.endpoints import (
    CanvasFilter as CanvasFilterEndpoint,
    CanvasMisc as CanvasMiscEndpoint,
    CanvasOverlay as CanvasOverlayEndpoint,
    )
from ..models.image import Image
from ..models.namecard import GenshinNamecard
from ..models.tweet import Tweet
from ..models.youtube_comment import YoutubeComment


if TYPE_CHECKING:
    from ..internals.http import HTTPClient

__all__ = ("CanvasClient",)


class CanvasClient:
    """Represents the ``Canvas`` endpoint.

    This class is not meant to be instantiated by the user. Instead, access it through the :attr:`~somerandomapi.Client.canvas` attribute of the :class:`~somerandomapi.Client`.
    """

    __slots__ = ("__http",)

    def __init__(self, http) -> None:
        self.__http: HTTPClient = http

    @property
    def memes(self) -> CanvasMemes:
        """:class:`.CanvasMemes`: Returns a subclient for the memes endpoints."""
        return CanvasMemes(self.__http)

    async def filter(self, avatar_url: str, filter: CanvasFilter) -> Image:
        """Apply a filter to an image.

        The following filters cannot be used with this method:
            - :attr:`.CanvasFilter.BRIGHTNESS` (use :meth:`filter_brightness` instead)
            - :attr:`.CanvasFilter.COLOR` (use :meth:`filter_color` instead)
            - :attr:`.CanvasFilter.THRESHOLD` (use :meth:`filter_threshold` instead)

        The following filters are from a different endpoint but are handled here:
            - :attr:`.enums.CanvasFilter.BLUR`
            - :attr:`.CanvasFilter.JPG`
            - :attr:`.CanvasFilter.PIXELATE`

        Parameters
        ----------
        avatar_url: :class:`str`
            The avatar URL.
        filter: :class:`.CanvasFilter`
            The filter to apply.

        Returns
        -------
        :class:`.Image`
            The filtered image.
        """
        _enum = CanvasFilter
        if not isinstance(filter, _enum):
            raise TypeError(f"Expected CanvasFilter, got {filter.__class__.__name__}")

        # because these require different parameters, we need to check and deny them here
        if filter in (_enum.BRIGHTNESS, _enum.COLOR, _enum.THRESHOLD):
            raise ValueError(
                f"Filter {filter} cannot be used with this method. Use `.filter_{filter.name.lower()}()` instead."
            )


        if filter in (_enum.BLUR, _enum.JPG, _enum.PIXELATE):
            _endpoint = CanvasMiscEndpoint.from_enum(filter)
        else:
            _endpoint = CanvasFilterEndpoint.from_enum(filter)

        return await self.__http.request(_endpoint, avatar=avatar_url)

    async def filter_brightness(self, avatar_url: str, brightness: Optional[int] = None) -> Image:
        """Apply a brightness filter to an image.

        Parameters
        ----------
        avatar_url: :class:`str`
            The avatar URL.
        brightness: :class:`int`
            The brightness value. Must be between 0 and 255. Defaults to a random number.

        Returns
        -------
        :class:`.Image`
            The filtered image.
        """
        if brightness is not None and not 0 <= brightness <= 255:
            raise ValueError("Brightness must be between 0 and 255. Don't specify it to get a random value.")

        brightness = brightness or random.randint(0, 255)
        _enum = CanvasFilter
        _filter = _enum.BRIGHTNESS
        _endpoint = CanvasFilterEndpoint.from_enum(_filter)
        return await self.__http.request(_endpoint, avatar=avatar_url, brightness=brightness)

    async def filter_color(self, avatar_url: str, color: str) -> Image:
        """Apply a color filter to an image.

        Parameters
        ----------
        avatar_url: :class:`str`
            The avatar URL.
        color: :class:`str`
            The hex color to apply. Can put "random" to get a random color.

        Returns
        -------
        :class:`.Image`
            The filtered image.
        """
        _enum = CanvasFilter
        _filter = _enum.COLOR
        _endpoint = CanvasFilterEndpoint.from_enum(_filter)
        _color = _utils._check_colour_value(color, "color")
        return await self.__http.request(_endpoint, avatar=avatar_url, color=_color)

    async def filter_colour(self, avatar_url: str, colour: str) -> Image:
        """Alias for :meth:`.filter_color`."""
        # this is a bit of a hack, but i want the error message to say "colour" instead of "color"
        try:
            return await self.filter_color(avatar_url, colour)
        except ValueError as e:
            INVALID_COLOUR_ERROR = e.args[0].replace("color", "colour")
            raise ValueError(INVALID_COLOUR_ERROR) from None

    async def filter_threshold(self, avatar_url: str, threshold: Optional[int] = None) -> Image:
        """Apply a threshold filter to an image.

        Parameters
        ----------
        avatar_url: :class:`str`
            The avatar URL.
        threshold: :class:`int`
            The threshold value. Must be between 1 and 255. Defaults to a random number.

        Returns
        -------
        :class:`.Image`
            The filtered image.
        """
        if threshold and not None and not 1 <= threshold <= 255:
            raise ValueError(f"Threshold must be between 1 and 255. Don't specify it to get a random value.")

        threshold = threshold or random.randint(1, 255)
        _enum = CanvasFilter
        _filter = _enum.THRESHOLD
        _endpoint = CanvasFilterEndpoint.from_enum(_filter)
        return await self.__http.request(_endpoint, avatar=avatar_url, threshold=threshold)

    async def overlay(self, avatar_url: str, overlay: CanvasOverlay) -> Image:
        """Apply an overlay to an image.

        Parameters
        ----------
        avatar_url: :class:`str`
            The avatar URL.
        overlay: :class:`.CanvasOverlay`
            The overlay to apply.

        Returns
        -------
        :class:`.Image`
            The filtered image.
        """
        _enum = CanvasOverlay
        if not isinstance(overlay, _enum):
            raise TypeError(f"Expected CanvasOverlay, got {overlay.__class__.__name__}")

        _endpoint = CanvasOverlayEndpoint.from_enum(overlay)
        return await self.__http.request(_endpoint, avatar=avatar_url)

    async def border(self, avatar_url: str, border: CanvasBorder) -> Image:
        """Add a border to an image.

        Parameters
        ----------
        avatar_url: :class:`str`
            The avatar URL.
        border: :class:`.CanvasBorder`
            The border to add.

        Returns
        -------
        :class:`.Image`
            The filtered image.
        """
        _enum = CanvasBorder
        if not isinstance(border, _enum):
            raise TypeError(f"Expected CanvasBorder, got {border.__class__.__name__}")

        border_to_endpoint = {
            _enum.LGBT: CanvasMiscEndpoint.LGBT_BORDER,
            _enum.LESBIAN: CanvasMiscEndpoint.LESBIAN_BORDER,
            _enum.NONBINARY: CanvasMiscEndpoint.NONBINARY_BORDER,
            _enum.PANSEXUAL: CanvasMiscEndpoint.PANSEXUAL_BORDER,
            _enum.TRANSGENDER: CanvasMiscEndpoint.TRANSGENDER_BORDER,
        }
        return await self.__http.request(border_to_endpoint[border], avatar=avatar_url)

    async def crop(self, avatar_url: str, shape: CanvasCrop) -> Image:
        """Crop an image into various shapes.

        Parameters
        ----------
        avatar_url: :class:`str`
            The avatar URL.
        shape: :class:`.CanvasCrop`
            The shape to apply.

        Returns
        -------
        :class:`.Image`
            The filtered image.
        """
        _enum = CanvasCrop
        if not isinstance(shape, _enum):
            raise TypeError(f"Expected CanvasCrop, got {shape.__class__.__name__}")

        shape_to_endpoint = {
            _enum.CIRCLE: CanvasMiscEndpoint.CIRCLE_CROP,
            _enum.HEART: CanvasMiscEndpoint.HEART_CROP,
        }
        return await self.__http.request(shape_to_endpoint[shape], avatar=avatar_url)

    async def generate_tweet(
        self,
        obj: Optional[Tweet] = None,
        *,
        display_name: Optional[str] = None,
        username: Optional[str] = None,
        avatar_url: Optional[str] = None,
        text: Optional[str] = None,
        replies: Optional[int] = None,
        retweets: Optional[int] = None,
        likes: Optional[int] = None,
        theme: Literal["light", "dim", "dark"] = "light",
    ) -> Tweet:
        values = (
            ("display_name", display_name, True),
            ("username", username, True),
            ("avatar_url", avatar_url, True),
            ("text", text, True),
            ("replies", replies, False),
            ("retweets", retweets, False),
            ("likes", likes, False),
            ("theme", theme, False),
        )
        obj = _utils._handle_obj_or_args(Tweet, obj, values).copy()
        res = await self.__http.request(CanvasMiscEndpoint.TWEET, **obj.to_dict())
        obj._set_image(res)
        return obj

    async def generate_youtube_comment(
        self,
        obj: Optional[YoutubeComment] = None,
        *,
        avatar_url: Optional[str] = None,
        username: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> YoutubeComment:
        """Generate a real YouTube comment.

        Parameters
        ----------
        obj: Optional[:class:`.YoutubeComment`]
            The object to use. If not provided, one will be created.
        avatar_url: Optional[:class:`str`]
            The avatar URL. This is required if ``obj`` is not provided.
        username: Optional[:class:`str`]
            The username. This is required if ``obj`` is not provided.
        comment: Optional[:class:`str`]
            The comment. This is required if ``obj`` is not provided.

        Returns
        -------
        :class:`.YoutubeComment`
            Object representing the generated YouTube comment.
        """
        values = (("avatar", avatar_url, True), ("username", username, True), ("comment", comment, True))
        obj = _utils._handle_obj_or_args(YoutubeComment, obj, values).copy()
        res = await self.__http.request(CanvasMiscEndpoint.YOUTUBE_COMMENT, **obj.to_dict())
        obj._set_image(res)
        return obj

    async def generate_genshin_namecard(
        self,
        obj: Optional[GenshinNamecard] = None,
        *,
        avatar_url: Optional[str] = None,
        birthday: Optional[str] = None,
        username: Optional[str] = None,
        description: Optional[str] = None,
    ) -> GenshinNamecard:
        """Generate a Genshin Impact namecard.

        Parameters
        ----------
        obj: Optional[:class:`.GenshinNamecard`]
            The object to use. If not passed, the other parameters will be used and a new object will be created.
        avatar_url: Optional[:class:`str`]
            The avatar URL. Required if ``obj`` is not provided.
        birthday: Optional[:class:`str`]
            The birthday. Must be in the format ``MM/DD/YYYY``. Required if ``obj`` is not provided.
        username: Optional[:class:`str`]
            The username. Required if ``obj`` is not provided.
        description: Optional[:class:`str`]
            The description.
        """
        values = (
            ("avatar", avatar_url, True),
            ("birthday", birthday, True),
            ("username", username, True),
            ("description", description, False),
        )
        obj = _utils._handle_obj_or_args(GenshinNamecard, obj, values).copy()
        res = await self.__http.request(CanvasMiscEndpoint.GENSHIN_NAMECARD, **obj.to_dict())
        obj._set_image(res)
        return obj

    async def generate_simpcard(self, avatar_url: str) -> Image:
        """Generate a simpcard.

        Parameters
        ----------
        avatar_url: :class:`str`
            The avatar URL.

        Returns
        -------
        :class:`.Image`
            The simpcard.
        """
        return await self.__http.request(CanvasMiscEndpoint.SIMPCARD, avatar=avatar_url)

    async def color_viewer(self, color: str) -> Image:
        """Get a color as an image.

        Parameters
        ----------
        color: :class:`str`
            The color to get. Can put "random" to get a random color.

        Returns
        -------
        :class:`.Image`
            The color as an image.
        """
        color = _utils._check_colour_value(color)
        return await self.__http.request(CanvasMiscEndpoint.COLOR_VIEWER, hex=color)

    async def colour_viewer(self, colour: str) -> Image:
        """Alias for :meth:`.color_viewer`."""
        # this is a bit of a hack, but i want the error message to say "colour" instead of "color"
        try:
            return await self.color_viewer(colour)
        except ValueError as e:
            INVALID_COLOUR_ERROR = e.args[0].replace("color", "colour")
            raise ValueError(INVALID_COLOUR_ERROR) from None


class CanvasMemes:
    """A class for interacting with the Canvas memes endpoints.

    This class is not meant to be instantiated by the user. Instead, access it through the :attr:`~somerandomapi.CanvasClient.memes` attribute of the :class:`~somerandomapi.CanvasClient` class.
    """

    def __init__(self, http) -> None:
        self.__http = http

    async def oogway(self, quote: str) -> Image:
        """Get an image of Oogway saying a quote.

        Parameters
        ----------
        quote: :class:`str`
            The quote to say.

        Returns
        -------
        :class:`.Image`
            Object representing the generated image.
        """
        return await self.__http.request(CanvasMiscEndpoint.OOGWAY, quote=quote)

    async def oogway2(self, quote: str) -> Image:
        """Get an image of Oogway saying a quote.

        Parameters
        ----------
        quote: :class:`str`
            The quote to say.

        Returns
        -------
        :class:`.Image`
            Object representing the generated image.
        """
        return await self.__http.request(CanvasMiscEndpoint.OOGWAY2, quote=quote)

    async def horny(self, avatar_url: str) -> Image:
        """Horny meme.

        Parameters
        ----------
        avatar_url: :class:`str`
            The avatar URL.

        Returns
        -------
        :class:`.Image`
            Object representing the generated image.
        """
        return await self.__http.request(CanvasMiscEndpoint.HORNY, avatar=avatar_url)

    async def its_so_stupid(self, avatar_url: str) -> Image:
        """It's so stupid meme.

        Parameters
        -----------
        avatar_url: :class:`str`
            The avatar URL.

        Returns
        --------
        :class:`.Image`
            Object representing the generated image.
        """
        return await self.__http.request(CanvasMiscEndpoint.ITS_SO_STUPID, avatar=avatar_url)

    async def lied(self, avatar_url: str, username: str) -> Image:
        """Lied meme.

        Parameters
        -----------
        avatar_url: :class:`str`
            The avatar URL.
        username: :class:`str`
            The username.

        Returns
        --------
        :class:`.Image`
            Object representing the generated image.
        """
        return await self.__http.request(CanvasMiscEndpoint.LIED, avatar=avatar_url, username=username)

    async def lolice(self, avatar_url: str) -> Image:
        """Lolice meme.

        Parameters
        -----------
        avatar_url: :class:`str`
            The avatar URL.

        Returns
        --------
        :class:`.Image`
            Object representing the generated image.
        """
        return await self.__http.request(CanvasMiscEndpoint.LOLICE, avatar=avatar_url)

    async def no_bitches(self, no: str) -> Image:
        """No bitches meme.

        Parameters
        -----------
        no: :class:`str`
            no?

        Returns
        --------
        :class:`.Image`
            Object representing the generated image.
        """
        return await self.__http.request(CanvasMiscEndpoint.NO_BITCHES, no=no)

    async def tonikawa(self, avatar_url: str) -> Image:
        """Tonikawa meme.

        Parameters
        -----------
        avatar_url: :class:`str`
            The avatar URL.

        Returns
        --------
        :class:`.Image`
            Object representing the generated image.
        """
        return await self.__http.request(CanvasMiscEndpoint.TONIKAWA, avatar=avatar_url)
