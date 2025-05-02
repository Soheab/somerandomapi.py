from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Self, overload
import logging

import aiohttp

from .. import utils as _utils
from ..enums import WelcomeBackground, WelcomeTextColor, WelcomeType
from ..internals.endpoints import (
    Base as BaseEndpoint,
    CanvasMisc as CanvasMiscEndpoint,
    _Endpoint,
)
from ..internals.http import HTTPClient
from ..models.encoding import EncodeResult
from ..models.lyrics import Lyrics
from ..models.rgb import RGB
from ..models.welcome.free import WelcomeFree
from .abc import BaseClient
from .chatbot import Chatbot

if TYPE_CHECKING:
    from .animal import AnimalClient
    from .animu import AnimuClient
    from .canvas import CanvasClient
    from .pokemon import PokemonClient
    from .premium import PremiumClient


__all__ = ("Client",)

_log: logging.Logger = logging.getLogger(__name__)


class Client(BaseClient):
    """Client for interacting with the Some Random API.

    This class provides access to all endpoints of the Some Random API, including both free and premium features.

    Parameters
    ----------
    session: :class:`aiohttp.ClientSession`
        An aiohttp session to use for HTTP requests. If not provided, the client will create and manage its own session.

        .. versionchanged:: 0.1.0
            - If a session is provided, it will not be closed by the client. Otherwise, the client manages its own session.
            - This parameter can no longer be ``None``. Either pass a session or omit it entirely.

    token: str | None
        The token to use for endpoints that require it.

        .. versionadded:: 0.1.0
    """

    __slots__: tuple[str, ...] = (*(BaseClient.__slots__), "__chatbot")

    def __init__(
        self,
        token: str | None = None,
        *,
        session: aiohttp.ClientSession = _utils.NOVALUE,
    ) -> None:
        http = HTTPClient(token, session)
        super().__init__(http)
        self.__chatbot: Chatbot | None = None

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()

    @property
    def animu(self) -> AnimuClient:
        """:class:`.AnimuClient`: The Animu endpoint."""
        return self._http._animu

    @property
    def animal(self) -> AnimalClient:
        """:class:`.AnimalClient`: The Animal endpoint."""
        return self._http._animal

    @property
    def canvas(self) -> CanvasClient:
        """:class:`.CanvasClient`: The Canvas endpoint."""
        return self._http._canvas

    @property
    def pokemon(self) -> PokemonClient:
        """:class:`.PokemonClient`: The Pokemon endpoint."""
        return self._http._pokemon

    @property
    def premium(self) -> PremiumClient:
        """:class:`.PremiumClient`: The Premium endpoint."""
        return self._http._premium

    def chatbot(self, message: str | None = None) -> Chatbot:
        """Chatbot endpoint.

        Parameters
        ----------
        message: Optional[:class:`str`]
            The message to send to the chatbot. If not provided, the Chatbot object will be returned instead which
            has a send method and supports ``async with``
            else :class:`.ChatbotResult` will be returned. ``.response`` on that is the response from the chatbot.

        Example
        --------
        .. code-block:: python

            async with client.chatbot() as bot:
                await bot.send("Hello!")
                print(bot.response)

            # or

            res = await client.chatbot("Hello!")
            print(res.response)

        Returns
        -------
        Union[:class:`.Chatbot`, :class:`.ChatbotResult`]
            The Chatbot object or the ChatbotResult object. ``ChatbotResult`` is returned if ``message``
            is provided and ``await`` is used else ``Chatbot``.
        """
        if self.__chatbot:
            self.__chatbot.message = message
            return self.__chatbot

        self.__chatbot = Chatbot(
            message=message,
            client=self,
        )
        return self.__chatbot

    async def _handle_encode_decode(
        self, what: Literal["ENCODE", "DECODE"], name: Literal["base64", "binary"], _input: str
    ) -> EncodeResult:
        type_to_endpoint = {"base64": BaseEndpoint.BASE64, "binary": BaseEndpoint.BINARY}
        res = await self._http.request(type_to_endpoint[name], **{what.lower(): _input})
        return EncodeResult.from_dict(
            _input=_input,
            _type=what.upper(),  # pyright: ignore[reportArgumentType]]
            text=res[f"{what.lower()}d"],
            name=name.upper(),  # pyright: ignore[reportArgumentType]]
        )

    async def encode_base64(self, _input: str, /) -> EncodeResult:
        """Encode a string to base64.

        Parameters
        ----------
        input: :class:`str`
            The string to encode.

        Returns
        -------
        :class:`.EncodeResult`
            Object representing the result of the encoding.
        """
        return await self._handle_encode_decode("ENCODE", "base64", _input)

    async def decode_base64(self, _input: str, /) -> EncodeResult:
        """Decode a base64 string.

        Parameters
        ----------
        input: :class:`str`
            The base64 string to decode.

        Returns
        -------
        :class:`.EncodeResult`
            Object representing the result of the decoding.
        """
        return await self._handle_encode_decode("DECODE", "base64", _input)

    async def encode_binary(self, _input: str, /) -> EncodeResult:
        """Encode a string to binary.

        Parameters
        ----------
        input: :class:`str`
            The string to encode.

        Returns
        -------
        :class:`.EncodeResult`
            Object representing the result of the encoding.
        """
        return await self._handle_encode_decode("ENCODE", "binary", _input)

    async def decode_binary(self, _input: str) -> EncodeResult:
        """Decode a binary string.

        Parameters
        ----------
        input: :class:`str`
            The binary string to decode.

        Returns
        -------
        :class:`.EncodeResult`
            Object representing the result of the decoding.
        """
        return await self._handle_encode_decode("DECODE", "binary", _input)

    async def generate_bot_token(self) -> str:
        """:class:`str`: Generate a very realistic bot token"""
        res = await self._http.request(
            BaseEndpoint.BOTTOKEN,
        )
        return res["token"]

    async def lyrics(self, song_title: str) -> Lyrics:
        """Get the lyrics of a song.

        Parameters
        ----------
        song_title: :class:`str`
            The title of the song to get the lyrics of.

        Returns
        -------
        :class:`.Lyrics`
            Object representing the lyrics result.
        """
        res = await self._http.request(BaseEndpoint.LYRICS, title=song_title)
        return Lyrics.from_dict(res)

    async def random_joke(self) -> str:
        """Get a random joke.

        Returns
        -------
        :class:`str`
            The joke.
        """
        res = await self._http.request(BaseEndpoint.JOKE)
        return res["joke"]

    @overload
    async def _handle_rgb_or_hex(self, endpoint: Literal[_Endpoint.CANVAS_RGB,], _input: str) -> RGB: ...

    @overload
    async def _handle_rgb_or_hex(self, endpoint: Literal[_Endpoint.CANVAS_HEX], _input: str) -> str: ...

    @overload
    async def _handle_rgb_or_hex(self, endpoint: Literal[_Endpoint.CANVAS_RGB], _input: str) -> RGB: ...

    async def _handle_rgb_or_hex(
        self, endpoint: Literal[_Endpoint.CANVAS_RGB, _Endpoint.CANVAS_HEX], _input: str
    ) -> RGB | str:
        endpoint_to_arg = {CanvasMiscEndpoint.RGB: "hex", CanvasMiscEndpoint.HEX: "rgb"}
        kwarga = {endpoint_to_arg[endpoint.value]: _input.strip("#")}
        res = await self._http.request(endpoint, **kwarga)
        if endpoint is _Endpoint.CANVAS_HEX:
            return res["hex"]
        return RGB.from_dict(res)

    # @_utils.endpoint(CanvasMiscEndpoint.HEX, to_call=_handle_rgb_or_hex)
    async def rgb_to_hex(self, rgb: str) -> str:
        """Converts an RGB value to a hex value.

        Parameters
        ----------
        rgb: :class:`str`
            The RGB value to convert. Must be in the format ``r,g,b``.

        Returns
        -------
        :class:`str`
            The hex value.
        """
        return await self._handle_rgb_or_hex(_Endpoint.CANVAS_HEX, rgb)

    # @_utils.endpoint(CanvasMiscEndpoint.RGB, to_call=_handle_rgb_or_hex)
    async def hex_to_rgb(self, _hex: str, /) -> RGB:
        """Converts a hex value to an RGB value.

        Parameters
        ----------
        hex: :class:`str`
            The hex value to convert. Must be in the format ``123456`` or ``#123456``.

        Returns
        -------
        :class:`.RGB`
            Object containing the RGB values. Use ``.as_tuple`` to get a tuple with the RGB values (``(r, g, b)``).
        """
        return await self._handle_rgb_or_hex(_Endpoint.CANVAS_RGB, _hex)

    @overload
    async def welcome_image(
        self,
        obj: WelcomeFree,
    ) -> WelcomeFree: ...

    @overload
    async def welcome_image(
        self,
        *,
        template: Literal[1, 2, 3, 4, 5, 6, 7],
        type: WelcomeType,
        background: WelcomeBackground,
        avatar_url: str,
        username: str,
        server_name: str,
        member_count: int,
        text_color: WelcomeTextColor,
        discriminator: int | None = ...,
        key: str | None = ...,
        font: Literal[0, 1, 2, 3, 4, 5, 6, 7] | None = ...,
    ) -> WelcomeFree: ...

    async def welcome_image(
        self,
        obj: WelcomeFree = _utils.NOVALUE,
        *,
        template: Literal[1, 2, 3, 4, 5, 6, 7] = _utils.NOVALUE,
        type: WelcomeType = _utils.NOVALUE,  # noqa: A002
        background: WelcomeBackground = _utils.NOVALUE,
        avatar_url: str = _utils.NOVALUE,
        username: str = _utils.NOVALUE,
        server_name: str = _utils.NOVALUE,
        member_count: int = _utils.NOVALUE,
        text_color: WelcomeTextColor = _utils.NOVALUE,
        discriminator: int | None = _utils.NOVALUE,
        key: str | None = _utils.NOVALUE,
        font: Literal[0, 1, 2, 3, 4, 5, 6, 7] | None = _utils.NOVALUE,
    ) -> WelcomeFree:
        """Generate a welcome image.

        Parameters
        ----------
        obj: :class:`.WelcomeFree`
            The object to use. If not passed, the other parameters will be used and a new object will be created.
        template: Literal[1, 2, 3, 4, 5, 6, 7, 8]
            The template to use. Required if ``obj`` is not passed.
        type: :class:`.WelcomeType`
            The type of welcome image to generate. Required if ``obj`` is not passed.
        background: :class:`.WelcomeBackground`
            The background to use. Required if ``obj`` is not passed.
        avatar_url: :class:`str`
            The avatar URL to use. Required if ``obj`` is not passed.
        username: :class:`str`
            The username to use. Required if ``obj`` is not passed.
        discriminator: :class:`int`
            The discriminator to use.
        server_name: :class:`str`
            The server name to use. Required if ``obj`` is not passed.
        member_count: :class:`int`
            The member count to use. Required if ``obj`` is not passed.
        text_color: :class:`.WelcomeTextColor`
            The text color to use. Required if ``obj`` is not passed.
        key: :class:`str`
            The key to use. Required if a key was not passed when creating the client.
        font: :class:`int`
            The font from a predefined list. Choose a number between 0 and 7.

            .. versionchanged:: 0.1.0
                Now takes a range of 1-7 instead of 1-8.
        """
        values = (
            ("template", template, True),
            ("type", type, True),
            ("background", background, True),
            ("avatar_url", avatar_url, True),
            ("username", username, True),
            ("server_name", server_name, True),
            ("member_count", member_count, True),
            ("text_color", text_color, True),
            ("discriminator", discriminator, False),
            ("key", key, False),
            ("font", font, False),
        )
        endpoint = BaseEndpoint.WELCOME

        obj = _utils._handle_obj_or_args(WelcomeFree, obj, values).copy()
        res = await self._http.request(endpoint, **obj.to_dict())
        new = obj.copy()
        new._set_image(res)
        return new

    async def close(self) -> None:
        """Close the client session."""
        await self._http.close()

        if self.__chatbot:
            await self.__chatbot.close()
