from __future__ import annotations

from typing import Any, Literal, Optional, overload, TYPE_CHECKING, Union

from .. import utils as _utils
from ..clients.chatbot import Chatbot
from ..internals.endpoints import (
    CanvasMisc as CanvasMiscEndpoint,
    Others as OthersEndpoint,
    WelcomeImages as WelcomeImagesEndpoint,
)
from ..internals.http import APIKey, HTTPClient
from ..models.dictionary import Dictionary
from ..models.encoding import EncodeResult
from ..models.lyrics import Lyrics
from ..models.rgb import RGB
from ..models.welcome.free import WelcomeFree


if TYPE_CHECKING:
    from aiohttp import ClientSession

    from ..enums import WelcomeBackground, WelcomeType
    from ..types.welcome import WelcomeTextColors
    from .animal import Animal
    from .animu import Animu
    from .canvas import Canvas


__all__ = ("Client",)


class Client:
    """Class representing the client for the Some Random API.

    Parameters
    ----------
    session: Optional[:class:`aiohttp.ClientSession`]
        The session to use for requests. If not provided, a new session will be created.

    key: Optional[:class:`tuple[Literal[0, 1, 2, 3], str]]
        The API key to use for requests as a tuple of tier and key.
        E,g, (0, "key") for tier 0 (this can also be used when you don't know the tier)

        A key can also be passed per-request, in which case it will override the key passed to the client.

        For more information on the tiers, see the API documentation: https://somerandomapi.com/docs#api-keys

    """

    __slots__: tuple[str, ...] = ("_http", "__chatbot")

    def __init__(
        self, key: Optional[Union[tuple[Literal[0, 1, 2, 3], str], APIKey]], *, session: Optional[ClientSession] = None
    ) -> None:
        self._http = HTTPClient(key, session)
        self.__chatbot: Optional[Chatbot] = None

    async def __aenter__(self) -> Client:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    @property
    def animu(self) -> Animu:
        """:class:`Animu`: The Animu endpoint."""
        return self._http._animu

    @property
    def animal(self) -> Animal:
        """:class:`Animal`: The Animal endpoint."""
        return self._http._animal

    @property
    def canvas(self) -> Canvas:
        """:class:`Canvas`: The Canvas endpoint."""
        return self._http._canvas

    def chatbot(self, message: Optional[str] = None) -> Chatbot:
        """The Chatbot endpoint.

        Parameters
        ----------
        message: Optional[:class:`str`]
            The message to send to the chatbot.
            If not provided, the Chatbot object will be returned instead which has a send method and supports ``async with``.
            else, :class:`ChatbotResult` will be returned. `.response` on that is the response from the chatbot.


        Returns
        -------
        Union[:class:`Chatbot`, :class:`ChatbotResult`]
            The Chatbot object or the ChatbotResult object.
            ``ChatbotResult``is returned if ``message`` is provided and ``await`` is used else ``Chatbot``.
        """
        if self.__chatbot:
            self.__chatbot.message = message
            return self.__chatbot

        key = self._http._key
        self.__chatbot = Chatbot(
            message=message,
            client=self,
            key=key.value if key else None,
            key_tier=key.tier if key else None,
        )
        return self.__chatbot

    async def _handle_encode_decode(
        self, what: Literal["ENCODE", "DECODE"], name: Literal["base64", "binary"], _input: str
    ) -> EncodeResult:
        _type_to_endpoint = {"base64": OthersEndpoint.BASE64, "binary": OthersEndpoint.BINARY}
        res = await self._http.request(_type_to_endpoint[name], **{what.lower(): _input})
        return EncodeResult.from_dict(
            _input=_input,
            _type=what.upper(),  # type: ignore
            text=res[name.lower() if what == "ENCODE" else "text"],  # type: ignore
            name=name.upper(),  # type: ignore
        )

    async def encode_base64(self, input: str) -> EncodeResult:
        return await self._handle_encode_decode("ENCODE", "base64", input)

    async def decode_base64(self, input: str) -> EncodeResult:
        return await self._handle_encode_decode("DECODE", "base64", input)

    async def encode_binary(self, input: str) -> EncodeResult:
        return await self._handle_encode_decode("ENCODE", "binary", input)

    async def decode_binary(self, input: str) -> EncodeResult:
        return await self._handle_encode_decode("DECODE", "binary", input)

    async def generate_bot_token(self, bot_id: Union[str, int]) -> str:
        res = await self._http.request(OthersEndpoint.BOTTOKEN, id=bot_id)
        return res["token"]

    async def dictionary(self, word: str) -> Any:
        res = await self._http.request(OthersEndpoint.DICTIONARY, word=word)
        return Dictionary.from_dict(**res)

    async def lyrics(self, song_title: str) -> Any:
        res = await self._http.request(OthersEndpoint.LYRICS, title=song_title)
        return Lyrics.from_dict(**res)

    async def random_joke(self) -> str:
        res = await self._http.request(OthersEndpoint.JOKE)
        return res["joke"]

    @overload
    async def _handle_rgb_or_hex(self, endpoint: Literal[CanvasMiscEndpoint.RGB], input: str) -> RGB:
        ...

    @overload
    async def _handle_rgb_or_hex(self, endpoint: Literal[CanvasMiscEndpoint.HEX], input: str) -> str:
        ...

    async def _handle_rgb_or_hex(
        self, endpoint: Literal[CanvasMiscEndpoint.RGB, CanvasMiscEndpoint.HEX], input: str
    ) -> Union[RGB, str]:
        endpoint_to_arg = {CanvasMiscEndpoint.RGB: "hex", CanvasMiscEndpoint.HEX: "rgb"}
        kwarga = {endpoint_to_arg[endpoint]: input.strip("#")}
        res = await self._http.request(endpoint, **kwarga)
        if endpoint == CanvasMiscEndpoint.HEX:
            return res["hex"]
        else:
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
        return await self._handle_rgb_or_hex(CanvasMiscEndpoint.HEX, rgb)

    # @_utils.endpoint(CanvasMiscEndpoint.RGB, to_call=_handle_rgb_or_hex)
    async def hex_to_rgb(self, hex: str) -> RGB:
        """Converts a hex value to an RGB value.

        Parameters
        ----------
        hex: :class:`str`
            The hex value to convert. Must be in the format ``123456`` or ``#123456``.

        Returns
        -------
        :class:`RGB`
            Object containing the RGB values. Use ``.to_tuple()`` to get a tuple with the RGB values (``(r, g, b)``).
        """
        return await self._handle_rgb_or_hex(CanvasMiscEndpoint.RGB, hex)

    async def welcome_image(
        self,
        obj: Optional[WelcomeFree] = None,
        *,
        template: Optional[Literal[1, 2, 3, 4, 5, 6, 7, 8]] = None,
        type: Optional[WelcomeType] = None,
        background: Optional[WelcomeBackground] = None,
        avatar_url: Optional[str] = None,
        username: Optional[str] = None,
        discriminator: Optional[str] = None,
        server_name: Optional[str] = None,
        member_count: Optional[int] = None,
        text_color: Optional[WelcomeTextColors] = None,
        key: Optional[str] = None,
        font: Optional[int] = None,
    ) -> WelcomeFree:
        values = (
            ("template", template, True),
            ("type", type, True),
            ("background", background, True),
            ("avatar_url", avatar_url, True),
            ("username", username, True),
            ("discriminator", discriminator, True),
            ("server_name", server_name, True),
            ("member_count", member_count, True),
            ("text_color", text_color, True),
            ("key", key, False),
            ("font", font, False),
        )
        endpoint = WelcomeImagesEndpoint.WELCOME

        obj = _utils._handle_obj_or_args(WelcomeFree, obj, values).copy()
        res = await self._http._welcome_card(endpoint, obj)
        new = obj.copy()
        new._set_image(res)
        return new

    async def close(self) -> None:
        """Close the client session."""
        await self._http.close()

        if self.__chatbot:
            await self.__chatbot.close()
