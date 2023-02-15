from __future__ import annotations
from typing import TYPE_CHECKING, Literal, Optional, Tuple, Union

from .. import utils as _utils
from ..enums import CanvasFilter, CanvasOverlay, CanvasBorder, CanvasCrop
from ..internals.endpoints import (
    CanvasFilter as CanvasFilterEndpoint,
    CanvasOverlay as CanvasOverlayEndpoint,
    CanvasMisc as CanvasMiscEndpoint,
)
from ..models.youtube_comment import YoutubeComment
from ..models.tweet import Tweet
from ..models.rgb import RGB
from ..models.namecard import GenshinNamecard

if TYPE_CHECKING:
    from ..internals.http import HTTPClient

    from ..types.canvas.filter import Filters as FilterLiterals
    from ..types.canvas.overlay import Overlays as OverlayLiterals
    from ..types.canvas.misc import Borders as BorderLiterals, Crops as CropLiterals

    from ..models.image import Image

__all__: Tuple[str, ...] = ("Canvas",)


class Canvas:
    """Represents the "Canvas" endpoint.

    This class is not meant to be instantiated by the user. Instead, access it through the `canvas` attribute of the `Client` class.
    """

    __slots__: Tuple[str, ...] = ("__http",)

    def __init__(self, http: HTTPClient) -> None:
        self.__http: HTTPClient = http

    async def filter(self, avatar: str, filter: CanvasFilter) -> Image:
        """Apply a filter to an image.

        The following filters cannot be used with this method:
            - :attr:`CanvasFilter.BRIGHTNESS` (use :meth:`filter_brightness` instead)
            - :attr:`CanvasFilter.COLOR` (use :meth:`filter_color` instead)
            - :attr:`CanvasFilter.THRESHOLD` (use :meth:`filter_threshold` instead)

        The following filters are from a different endpoint but are handled here:
            - :attr:`CanvasFilter.BLUR`
            - :attr:`CanvasFilter.JPG`
            - :attr:`CanvasFilter.PIXELATE`

        Parameters
        ----------
        avatar: :class:`str`
            The avatar URL.
        filter: :class:`CanvasFilter`
            The filter to apply.

        Returns
        -------
        :class:`Image`
            The filtered image.
        """
        _enum = CanvasFilter
        if not isinstance(filter, _enum):
            raise TypeError(f"Expected CanvasFilter, got {filter.__class__.__name__}")

        # because these require different parameters, we need to check and deny them here
        if filter in (_enum.BRIGHTNESS, _enum.COLOR, _enum.THRESHOLD):
            raise ValueError(
                f"Filter {filter} cannot be used with this method. Use `filter_{filter.name.lower()}` instead."
            )

        _endpoint_cls = (
            CanvasFilterEndpoint if filter not in (_enum.BLUR, _enum.JPG, _enum.PIXELATE) else CanvasMiscEndpoint
        )

        _endpoint = _endpoint_cls._from_enum(filter)
        return await self.__http.request(_endpoint, avatar=avatar)

    async def filter_brightness(self, avatar: str, brightness: int) -> Image:
        """Apply a brightness filter to an image.

        Parameters
        ----------
        avatar: :class:`str`
            The avatar URL.
        brightness: :class:`int`
            The brightness value. Must be between 0 and 100.

        Returns
        -------
        :class:`Image`
            The filtered image.
        """
        _enum = CanvasFilter
        _filter = _enum.BRIGHTNESS
        _endpoint = CanvasFilterEndpoint._from_enum(_filter)
        return await self.__http.request(_endpoint, avatar=avatar, brightness=brightness)

    async def filter_color(self, avatar: str, color: str) -> Image:
        """Apply a color filter to an image.

        Parameters
        ----------
        avatar: :class:`str`
            The avatar URL.
        color: :class:`str`
            The hex color to apply. Can put "random" to get a random color.

        Returns
        -------
        :class:`Image`
            The filtered image.
        """
        _enum = CanvasFilter
        _filter = _enum.COLOR
        _endpoint = CanvasFilterEndpoint._from_enum(_filter)
        _color = _utils._check_colour_value(color)  # type: ignore
        return await self.__http.request(_endpoint, avatar=avatar, color=_color)

    async def filter_threshold(self, avatar: str, threshold: int) -> Image:
        """Apply a threshold filter to an image.

        Parameters
        ----------
        avatar: :class:`str`
            The avatar URL.
        threshold: :class:`int`
            The threshold value. Must be between 1 and 255.

        Returns
        -------
        :class:`Image`
            The filtered image.
        """
        if not 1 <= threshold <= 255:
            raise ValueError(f"Threshold must be between 1 and 255, got {threshold}")

        _enum = CanvasFilter
        _filter = _enum.THRESHOLD
        _endpoint = CanvasFilterEndpoint._from_enum(_filter)
        return await self.__http.request(_endpoint, avatar=avatar, threshold=threshold)

    async def overlay(self, avatar: str, overlay: CanvasOverlay) -> Image:
        """Apply an overlay to an image.

        Parameters
        ----------
        avatar: :class:`str`
            The avatar URL.
        overlay: :class:`CanvasOverlay`
            The overlay to apply.

        Returns
        -------
        :class:`Image`
            The filtered image.
        """
        _enum = CanvasOverlay
        if not isinstance(overlay, _enum):
            raise TypeError(f"Expected CanvasOverlay, got {overlay.__class__.__name__}")

        _endpoint = CanvasOverlayEndpoint._from_enum(overlay)
        return await self.__http.request(_endpoint, avatar=avatar)

    async def border(self, avatar: str, border: CanvasBorder) -> Image:
        """Add a border to an image.

        Parameters
        ----------
        avatar: :class:`str`
            The avatar URL.
        border: :class:`CanvasBorder`
            The border to add.

        Returns
        -------
        :class:`Image`
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
        return await self.__http.request(border_to_endpoint[border], avatar=avatar)

    async def crop(self, avatar: str, shape: CanvasCrop) -> Image:
        """Crop an image into various shapes.

        Parameters
        ----------
        avatar: :class:`str`
            The avatar URL.
        shape: :class:`CanvasCrop`
            The shape to apply.

        Returns
        -------
        :class:`Image`
            The filtered image.
        """
        _enum = CanvasCrop
        if not isinstance(shape, _enum):
            raise TypeError(f"Expected CanvasCrop, got {shape.__class__.__name__}")

        shape_to_endpoint = {
            _enum.CIRCLE: CanvasMiscEndpoint.CIRCLE_CROP,
            _enum.HEART: CanvasMiscEndpoint.HEART_CROP,
        }
        return await self.__http.request(shape_to_endpoint[shape], avatar=avatar)

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
        obj._image = res
        return obj

    async def generate_youtube_comment(
        self,
        obj: Optional[YoutubeComment] = None,
        *,
        avatar: Optional[str] = None,
        username: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> YoutubeComment:
        values = (("avatar", avatar, True), ("username", username, True), ("comment", comment, True))
        obj = _utils._handle_obj_or_args(YoutubeComment, obj, values).copy()
        res = await self.__http.request(CanvasMiscEndpoint.YOUTUBE_COMMENT, **obj.to_dict())
        obj._image = res
        return obj

    async def generate_genshin_namecard(
        self,
        obj: Optional[GenshinNamecard] = None,
        *,
        avatar: Optional[str] = None,
        birthday: Optional[str] = None,
        username: Optional[str] = None,
        description: Optional[str] = None,
    ) -> GenshinNamecard:
        values = (
            ("avatar", avatar, True),
            ("birthday", birthday, True),
            ("username", username, True),
            ("description", description, False),
        )
        obj = _utils._handle_obj_or_args(GenshinNamecard, obj, values).copy()
        res = await self.__http.request(CanvasMiscEndpoint.GENSHIN_NAMECARD, **obj.to_dict())
        obj._image = res
        return obj

    async def generate_simpcard(self, avatar_url: str) -> Image:
        return await self.__http.request(CanvasMiscEndpoint.SIMPCARD, avatar_url=avatar_url)

    async def color_viewer(self, color: str) -> Image:
        """Get a color as an image.

        Parameters
        ----------
        color: :class:`str`
            The color to get. Can put "random" to get a random color.

        Returns
        -------
        :class:`Image`
            The color as an image.
        """
        color = _utils._check_colour_value(color)  # type: ignore
        return await self.__http.request(CanvasMiscEndpoint.COLOR_VIEWER, hex=color)


class CanvasMemes:
    def __init__(self, http: HTTPClient) -> None:
        self.__http = http

    async def oogway(self, quote: str) -> Image:
        return await self.__http.request(CanvasMiscEndpoint.OOGWAY, quote=quote)

    async def oogway2(self, quote: str) -> Image:
        return await self.__http.request(CanvasMiscEndpoint.OOGWAY2, quote=quote)

    async def horny(self, avtar: str) -> Image:
        return await self.__http.request(CanvasMiscEndpoint.HORNY, avatar=avtar)

    async def its_so_stupid(self, avatar: str) -> Image:
        return await self.__http.request(CanvasMiscEndpoint.ITS_SO_STUPID, avatar=avatar)

    async def lied(self, avatar: str, username: str) -> Image:
        return await self.__http.request(CanvasMiscEndpoint.LIED, avatar=avatar, username=username)

    async def lolice(self, avatar: str) -> Image:
        return await self.__http.request(CanvasMiscEndpoint.LOLICE, avatar=avatar)

    async def no_bitches(self, no: str) -> Image:
        return await self.__http.request(CanvasMiscEndpoint.NO_BITCHES, no=no)

    async def tonikawa(self, avatar: str) -> Image:
        return await self.__http.request(CanvasMiscEndpoint.TONIKAWA, avatar=avatar)
