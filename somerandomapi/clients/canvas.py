from __future__ import annotations

from typing import TYPE_CHECKING, Literal, overload
import random

from .. import utils as _utils
from ..enums import CanvasBorder, CanvasCrop, CanvasFilter, CanvasOverlay, TweetTheme
from ..internals.endpoints import (
    CanvasFilter as CanvasFilterEndpoint,
    CanvasMisc as CanvasMiscEndpoint,
    CanvasOverlay as CanvasOverlayEndpoint,
)
from ..models.namecard import GenshinNamecard
from ..models.tweet import Tweet
from ..models.youtube_comment import YoutubeComment
from .abc import BaseClient

if TYPE_CHECKING:
    from ..models.image import Image
    from ..types.canvas import Borders, Crops, Filters, Overlays

# fmt: off
NumbersTill100 = Literal[
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
    31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
    60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88,
    89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100
]

NumbersTill255 = Literal[
    NumbersTill100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113,
    114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136,
    137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159,
    160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182,
    183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205,
    206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228,
    229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251,
    252, 253, 254, 255,
]
# fmt: on

__all__ = ("CanvasClient",)


class CanvasClient(BaseClient):
    """Represents the ``Canvas`` endpoint.

    This class is not meant to be instantiated by you. Instead, access it through the :attr:`~somerandomapi.Client.canvas`
    attribute of the :class:`~somerandomapi.Client`.
    """

    @property
    def memes(self) -> CanvasMemes:
        """:class:`.CanvasMemes`: Returns a subclient for the memes endpoints."""
        return CanvasMemes(self)

    async def _handle_filters(self, _filter: CanvasFilter, /, avatar_url: str, **extras: str | int | None) -> Image:
        # because these require different parameters, we need to check and deny them here
        if _filter in (CanvasFilter.BRIGHTNESS, CanvasFilter.COLOR, CanvasFilter.THRESHOLD):
            if _filter is CanvasFilter.BRIGHTNESS:
                error_msg = "Brightness must be a number between 0 and 100. Don't specify it to get a random value."
                brightness = extras.get("brightness")
                if brightness is not None:
                    try:
                        brightness = int(brightness)
                    except ValueError:
                        raise ValueError(error_msg) from None

                    if not 0 <= brightness <= 100:
                        raise ValueError(
                            "Brightness must be a number between 0 and 100. Don't specify it to get a random value."
                        )

                brightness = brightness if brightness is not None else random.randint(0, 100)  # noqa: S311
                return await self._http.request(
                    CanvasFilterEndpoint.from_enum(CanvasFilter.BRIGHTNESS), avatar=avatar_url, brightness=brightness
                )
            if _filter is CanvasFilter.COLOR:
                color = _utils._check_colour_value(extras.get("color"), "color")
                return await self._http.request(
                    CanvasFilterEndpoint.from_enum(CanvasFilter.COLOR), avatar=avatar_url, color=color
                )
            if _filter is CanvasFilter.THRESHOLD:
                error_msg = "Threshold must be a number between 0 and 255. Don't specify it to get a random value."
                threshold = extras.get("threshold")
                if threshold is not None:
                    try:
                        threshold = int(threshold)
                    except ValueError:
                        raise ValueError(error_msg) from None

                if threshold is not None and not 0 <= threshold <= 255:
                    raise ValueError("Threshold must be a number between 0 and 255. Don't specify it to get a random value.")

                threshold = threshold or random.randint(1, 255)  # noqa: S311
                return await self._http.request(
                    CanvasFilterEndpoint.from_enum(CanvasFilter.THRESHOLD), avatar=avatar_url, threshold=threshold
                )

        return await self._http.request(CanvasFilterEndpoint.from_enum(_filter), avatar=avatar_url)

    async def filter(self, avatar_url: str, filter: CanvasFilter | Filters) -> Image:  # noqa: A002
        """Apply a filter to an image.

        Parameters
        ----------
        avatar_url: :class:`str`
            The URL of the image to apply the filter to.
        filter: Union[:class:`.CanvasFilter`, :class:`str`]
            The filter to apply. Can be a :class:`.CanvasFilter` enum value or a string representing the filter name.

        Returns
        -------
        :class:`.Image`
            Object representing the filtered image. Use the ``.url`` attribute to access the image URL.
        """
        return await self._handle_filters(_utils._str_or_enum(filter, CanvasFilter), avatar_url=avatar_url)

    @BaseClient._proxy_to(filter, pre_args=((1, CanvasFilter.BLUE),), copy_params_of="DECORATED")
    async def blue_filter(self, avatar_url: str, /) -> Image:
        """Shortcut for :meth:`.filter` with :attr:`.CanvasFilter.BLUE`."""
        ...

    @BaseClient._proxy_to(filter, pre_args=((1, CanvasFilter.BLURPLE),), copy_params_of="DECORATED")
    async def blurple_filter(self, avatar_url: str, /) -> Image:
        """Shortcut for :meth:`.filter` with :attr:`.CanvasFilter.BLURPLE`."""
        ...

    @BaseClient._proxy_to(
        filter,
        pre_args=(
            (
                1,
                CanvasFilter.BLURPLE_2,
            ),
        ),
        copy_params_of="DECORATED",
    )
    async def blurple2_filter(self, avatar_url: str, /) -> Image:
        """Shortcut for :meth:`.filter` with :attr:`.CanvasFilter.BLURPLE_2`."""
        ...

    @BaseClient._proxy_to(filter, pre_args=((1, CanvasFilter.GREEN),), copy_params_of="DECORATED")
    async def green_filter(self, avatar_url: str, /) -> Image:
        """Shortcut for :meth:`.filter` with :attr:`.CanvasFilter.GREEN`."""
        ...

    @BaseClient._proxy_to(filter, pre_args=((1, CanvasFilter.GREYSCALE),), copy_params_of="DECORATED")
    async def greyscale_filter(self, avatar_url: str, /) -> Image:
        """Shortcut for :meth:`.filter` with :attr:`.CanvasFilter.GREYSCALE`."""
        ...

    @BaseClient._proxy_to(filter, pre_args=((1, CanvasFilter.INVERT),), copy_params_of="DECORATED")
    async def invert_filter(self, avatar_url: str, /) -> Image:
        """Shortcut for :meth:`.filter` with :attr:`.CanvasFilter.INVERT`."""
        ...

    @BaseClient._proxy_to(filter, pre_args=((1, CanvasFilter.INVERT_GREYSCALE),), copy_params_of="DECORATED")
    async def invertgreyscale_filter(self, avatar_url: str, /) -> Image:
        """Shortcut for :meth:`.filter` with :attr:`.CanvasFilter.INVERT_GREYSCALE`."""
        ...

    @BaseClient._proxy_to(filter, pre_args=((1, CanvasFilter.RED),), copy_params_of="DECORATED")
    async def red_filter(self, avatar_url: str, /) -> Image:
        """Shortcut for :meth:`.filter` with :attr:`.CanvasFilter.RED`."""
        ...

    @BaseClient._proxy_to(filter, pre_args=((1, CanvasFilter.SEPIA),), copy_params_of="DECORATED")
    async def sepia_filter(self, avatar_url: str, /) -> Image:
        """Shortcut for :meth:`.filter` with :attr:`.CanvasFilter.SEPIA`."""
        ...

    @BaseClient._proxy_to(filter, pre_args=((1, CanvasFilter.BLUR),), copy_params_of="DECORATED")
    async def blur_filter(self, avatar_url: str, /) -> Image:
        """Shortcut for :meth:`.filter` with :attr:`.CanvasFilter.BLUR`."""
        ...

    @BaseClient._proxy_to(filter, pre_args=((1, CanvasFilter.PIXELATE),), copy_params_of="DECORATED")
    async def pixelate_filter(self, avatar_url: str, /) -> Image:
        """Shortcut for :meth:`.filter` with :attr:`.CanvasFilter.PIXELATE`."""
        ...

    async def brightness_filter(self, avatar_url: str, brightness: NumbersTill100 | None = None) -> Image:
        """Apply a brightness filter to an image.

        Parameters
        ----------
        avatar_url: :class:`str`
            The URL of the image to apply the filter to.
        brightness: :class:`int`
            The brightness value. Must be between 0 and 100. Defaults to a random number between 0 and 100.

        Returns
        -------
        :class:`.Image`
            Object representing the filtered image. Use the ``.url`` attribute to access the image URL.
        """
        return await self._handle_filters(CanvasFilter.BRIGHTNESS, avatar_url, brightness=brightness)

    async def color_filter(self, avatar_url: str, color: str | int = _utils.NOVALUE) -> Image:
        """Apply a color filter to an image.

        Parameters
        ----------
        avatar_url: :class:`str`
            The URL of the image to apply the filter to.
        color: Union[:class:`str`, :class:`int`]
            The color to apply. Can be a hex value (e.g. ``#FF0000``) or an integer (e.g. ``16711680``).
            Defaults to a random color.

        Returns
        -------
        :class:`.Image`
            Object representing the filtered image. Use the ``.url`` attribute to access the image URL.
        """
        return await self._handle_filters(CanvasFilter.COLOR, avatar_url, color=color)

    async def colour_filter(self, avatar_url: str, colour: str) -> Image:
        """Alias for :meth:`.color_filter`."""
        # this is a bit of a hack, but i want the error message to say "colour" instead of "color"
        try:
            return await self._handle_filters(CanvasFilter.COLOR, avatar_url, color=colour)
        except ValueError as e:
            INVALID_COLOUR_ERROR = e.args[0].replace("color", "colour")
            raise ValueError(INVALID_COLOUR_ERROR) from None

    async def threshold_filter(self, avatar_url: str, threshold: NumbersTill255 | None = None) -> Image:
        """Apply a threshold filter to an image.

        Parameters
        ----------
        avatar_url: :class:`str`
            The URL of the image to apply the filter to.
        threshold: :class:`int`
            The threshold value. Must be between 0 and 255. Defaults to a random number between 1 and 255.

        Returns
        -------
        :class:`.Image`
            Object representing the filtered image. Use the ``.url`` attribute to access the image URL.
        """
        return await self._handle_filters(CanvasFilter.THRESHOLD, avatar_url, threshold=threshold)

    async def overlay(self, avatar_url: str, overlay: CanvasOverlay | Overlays) -> Image:
        """Add an overlay to an image.

        Parameters
        ----------
        avatar_url: :class:`str`
            The URL of the image to apply the overlay to.
        overlay: Union[:class:`.CanvasOverlay`, :class:`str`]
            The overlay to apply. Can be a :class:`.CanvasOverlay` enum value or a string representing the overlay name.

        Returns
        -------
        :class:`.Image`
            Object representing the image with the overlay applied. Use the ``.url`` attribute to access the image URL.
        """
        endpoint = CanvasOverlayEndpoint.from_enum(_utils._str_or_enum(overlay, CanvasOverlay))
        return await self._http.request(endpoint, avatar=avatar_url)

    async def border(self, avatar_url: str, border: CanvasBorder | Borders) -> Image:
        """Add a border to an image.

        Parameters
        ----------
        avatar_url: :class:`str`
            The avatar URL.
        border: Union[:class:`.CanvasBorder`, :class:`str`]
            The border to add.

        Returns
        -------
        :class:`.Image`
            The filtered image.
        """
        return await self._http.request(
            CanvasMiscEndpoint.from_enum(_utils._str_or_enum(border, CanvasBorder)), avatar=avatar_url
        )

    async def crop(self, avatar_url: str, shape: CanvasCrop | Crops) -> Image:
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
        return await self._http.request(
            CanvasMiscEndpoint.from_enum(_utils._str_or_enum(shape, CanvasCrop)), avatar=avatar_url
        )

    @overload
    async def generate_tweet(
        self,
        obj: Tweet = ...,
    ) -> Tweet: ...

    @overload
    async def generate_tweet(
        self,
        *,
        display_name: str,
        username: str,
        avatar_url: str,
        text: str,
        replies: int | None = ...,
        retweets: int | None = ...,
        likes: int | None = ...,
        theme: TweetTheme = ...,
    ) -> Tweet: ...

    async def generate_tweet(
        self,
        obj: Tweet = _utils.NOVALUE,
        *,
        display_name: str = _utils.NOVALUE,
        username: str = _utils.NOVALUE,
        avatar_url: str = _utils.NOVALUE,
        text: str = _utils.NOVALUE,
        replies: int | None = _utils.NOVALUE,
        retweets: int | None = _utils.NOVALUE,
        likes: int | None = _utils.NOVALUE,
        theme: TweetTheme = TweetTheme.LIGHT,
    ) -> Tweet:
        """Generate an image of a tweet (or post ...).

        Parameters
        ----------
        obj: :class:`.Tweet`
            The object to use. If not provided, one will be created with the other parameters.
        display_name: :class:`str`
            The display name of the user.
        username: :class:`str`
            The username of the user.
        avatar_url: :class:`str`
            The avatar URL of the user. Must be .png or .jpg.
        text: :class:`str`
            The text of the tweet. Max 1000 characters.
        replies: Optional[:class:`int`]
            The amount of replies the tweet is supposed to have.
        retweets: Optional[:class:`int`]
            The amount of retweets the tweet is supposed to have.
        likes: Optional[:class:`int`]
            The amount of likes the tweet is supposed to have.
        theme: :class:`.TweetTheme`
            The theme of the tweet. Can be either light, dark or dim. Defaults to light.

        Raises
        ------
        TypeError
            If ``obj`` is not a :class:`.Tweet`.
        ValueError
            If ``display_name``, ``username``, ``avatar_url`` and ``text`` are not provided and ``obj`` is not passed.

        Returns
        -------
        :class:`.Tweet`
            An object representing the generated tweet image. Use the ``.url`` attribute to access the image URL.
        """
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
        res = await self._http.request(CanvasMiscEndpoint.TWEET, **obj.to_dict())
        obj._set_image(res)
        return obj

    @overload
    async def generate_youtube_comment(
        self,
        obj: YoutubeComment,
    ) -> YoutubeComment: ...

    @overload
    async def generate_youtube_comment(
        self,
        *,
        avatar_url: str,
        username: str,
        text: str,
    ) -> YoutubeComment: ...

    async def generate_youtube_comment(
        self,
        obj: YoutubeComment = _utils.NOVALUE,
        *,
        avatar_url: str = _utils.NOVALUE,
        username: str = _utils.NOVALUE,
        text: str = _utils.NOVALUE,
    ) -> YoutubeComment:
        """Generate a Youtube comment image.


        Parameters
        ----------
        obj: :class:`.YoutubeComment`
            The object to use. If not provided, a new object will be created with the other parameters.
        avatar_url: :class:`str`
            The avatar URL of the user.
        username: :class:`str`
            The username of the user.
        text: :class:`str`
            The text of the comment.

        Raises
        ------
        TypeError
            If ``obj`` is not a :class:`.YoutubeComment`.
        ValueError
            If ``avatar_url``, ``username`` and ``comment`` are not provided and ``obj`` is not passed.

        Returns
        -------
        :class:`.YoutubeComment`
            An object representing the generated Youtube comment image. Use the ``.url`` attribute to access the image URL.
        """
        values = (("avatar_url", avatar_url, True), ("username", username, True), ("text", text, True))
        obj = _utils._handle_obj_or_args(YoutubeComment, obj, values).copy()
        res = await self._http.request(CanvasMiscEndpoint.YOUTUBE_COMMENT, **obj.to_dict())
        obj._set_image(res)
        return obj

    @overload
    async def generate_genshin_namecard(
        self,
        obj: GenshinNamecard,
    ) -> GenshinNamecard: ...

    @overload
    async def generate_genshin_namecard(
        self,
        *,
        avatar_url: str,
        birthday: str,
        username: str,
        description: str | None = ...,
    ) -> GenshinNamecard: ...

    async def generate_genshin_namecard(
        self,
        obj: GenshinNamecard = _utils.NOVALUE,
        *,
        avatar_url: str = _utils.NOVALUE,
        birthday: str = _utils.NOVALUE,
        username: str = _utils.NOVALUE,
        description: str | None = _utils.NOVALUE,
    ) -> GenshinNamecard:
        """Generate a Genshin Impact namecard.

        Parameters
        ----------
        obj: :class:`.GenshinNamecard`
            The object to use. If not provided, a new object will be created with the other parameters.
        avatar_url: :class:`str`
            The avatar URL.
        birthday: :class:`str`
            The birthday. Must be in the format ``MM/DD/YYYY``.
        username: :class:`str`
            The username.
        description: Optional[:class:`str`]
            An optional description.

        Raises
        ------
        TypeError
            If ``obj`` is not a :class:`.GenshinNamecard`.
        ValueError
            If ``avatar_url``, ``birthday`` and ``username``are not provided and ``obj`` is not passed.

        Returns
        -------
        :class:`.GenshinNamecard`
            An object representing the generated Genshin Impact namecard. Use the ``.url`` attribute to access the image URL.
        """
        values = (
            ("avatar", avatar_url, True),
            ("birthday", birthday, True),
            ("username", username, True),
            ("description", description, False),
        )
        obj = _utils._handle_obj_or_args(GenshinNamecard, obj, values).copy()
        res = await self._http.request(CanvasMiscEndpoint.GENSHIN_NAMECARD, **obj.to_dict())
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
        return await self._http.request(CanvasMiscEndpoint.SIMPCARD, avatar=avatar_url)

    async def color_viewer(self, color: str | int = _utils.NOVALUE) -> Image:
        """Get a color as an image.

        Parameters
        ----------
        color: :class:`str`
            The hex value to get. Defaults to a random color.

        Returns
        -------
        :class:`.Image`
            The color as an image. Use the ``.url`` attribute to access the image URL.
        """
        color = _utils._check_colour_value(color)
        return await self._http.request(CanvasMiscEndpoint.COLORVIEWER, hex=color)

    async def colour_viewer(self, colour: str | int = _utils.NOVALUE) -> Image:
        """Alias for :meth:`.color_viewer`."""
        # this is a bit of a hack, but i want the error message to say "colour" instead of "color"
        try:
            return await self.color_viewer(colour)
        except ValueError as e:
            INVALID_COLOUR_ERROR = e.args[0].replace("color", "colour")
            raise ValueError(INVALID_COLOUR_ERROR) from None


class CanvasMemes:
    """A class for interacting with the Canvas memes endpoints.

    This class is not meant to be instantiated by the user. Instead, access it through the
    :attr:`~somerandomapi.CanvasClient.memes` attribute of the :class:`~somerandomapi.CanvasClient` class.
    """

    def __init__(self, client: CanvasClient, /) -> None:
        self.__client: CanvasClient = client

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
        return await self.__client._http.request(CanvasMiscEndpoint.OOGWAY, quote=quote)

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
        return await self.__client._http.request(CanvasMiscEndpoint.OOGWAY2, quote=quote)

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
        return await self.__client._http.request(CanvasMiscEndpoint.HORNY, avatar=avatar_url)

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
        return await self.__client._http.request(CanvasMiscEndpoint.ITS_SO_STUPID, avatar=avatar_url)

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
        return await self.__client._http.request(CanvasMiscEndpoint.LIED, avatar=avatar_url, username=username)

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
        return await self.__client._http.request(CanvasMiscEndpoint.LOLICE, avatar=avatar_url)

    async def no_bitches(self, *, avatar_url: str, no: str, bottom_text: str | None = None) -> Image:
        """No bitches meme.

        Parameters
        -----------
        avatar_url: :class:`str`
            The avatar URL.
        no: :class:`str`
            no?
        bottom_text: :class:`str`
            The text to display at the bottom of the image.
            Defaults to nothing.

            .. versionadded:: 0.2.0

        Returns
        --------
        :class:`.Image`
            Object representing the generated image.
        """
        return await self.__client._http.request(
            CanvasMiscEndpoint.NO_BITCHES, avatar=avatar_url, no=no, bottomtext=bottom_text
        )

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
        return await self.__client._http.request(CanvasMiscEndpoint.TONIKAWA, avatar=avatar_url)
