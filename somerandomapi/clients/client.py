from __future__ import annotations

from typing import Literal, Optional, overload, TYPE_CHECKING, Union

import aiohttp

from .. import utils as _utils
from ..enums import WelcomeBackground, WelcomeTextColor, WelcomeType
from ..internals.endpoints import (
    CanvasMisc as CanvasMiscEndpoint,
    Others as OthersEndpoint,
    WelcomeImages as WelcomeImagesEndpoint,
)
from ..internals.http import HTTPClient
from ..models.dictionary import Dictionary
from ..models.encoding import EncodeResult
from ..models.lyrics import Lyrics
from ..models.rgb import RGB
from ..models.welcome.free import WelcomeFree
from .chatbot import Chatbot


if TYPE_CHECKING:
    from .animal import AnimalClient
    from .animu import AnimuClient
    from .canvas import CanvasClient
    from .pokemon import PokemonClient
    from .premium import PremiumClient


__all__ = ("Client",)


class Client:
    """Class representing the client for the Some Random API.

    Parameters
    ----------
    session: Optional[:class:`aiohttp.ClientSession`]
        The session to use for requests. If not provided, a new session will be created.

    key: Optional[Tuple[Literal[0, 1, 2, 3], :class:`str`]]
        The API key to use for requests as a tuple of tier and key or just the key.
        E,g, ``(0, "key")`` for tier 0 (this can also be used when you don't know the tier)
        OR ``"key"`` which will be treated as tier 0.

        A key can also be passed per-request, in which case it will override the key passed to the client.

        For more information on the tiers, :apidocs:`see the API documentation <#api-keys>`

    """

    __slots__: tuple[str, ...] = ("_http", "__chatbot")

    def __init__(
        self,
        key: Optional[Union[tuple[Literal[0, 1, 2, 3], str], str]] = None,
        *,
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        _key = None
        if key is not None:
            if not isinstance(key, (tuple, str)):
                raise TypeError(f"Expected 'key' to be a tuple or a string, not {type(key)}")

            if isinstance(key, tuple):
                if len(key) != 2:
                    raise ValueError(f"Expected 'key' to be a tuple of length 2, not {len(key)}")

                if not isinstance(key[0], int) and not isinstance(key[1], str):
                    raise TypeError(f"Expected 'key' to be a tuple of (int, str), not ({type(key[0])}, {type(key[1])})")

                if key[0] not in (0, 1, 2, 3):
                    raise ValueError(f"Expected first element of 'key' to be 0, 1, 2 or 3, not {key[0]}")

                _key = key
            else:
                _key = (0, key)

        self._http = HTTPClient(_key, session)
        self.__chatbot: Optional[Chatbot] = None

    async def __aenter__(self) -> Client:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
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

    def chatbot(self, message: Optional[str] = None) -> Chatbot:
        """:apidocs:`See this endpoint's on the API Documentation. <chatbot#chatbot>`.

        The Chatbot endpoint.

        Parameters
        ----------
        message: Optional[:class:`str`]
            The message to send to the chatbot. If not provided, the Chatbot object will be returned instead which has a send method and supports ``async with``
            else :class:`.ChatbotResult` will be returned. ``.response`` on that is the response from the chatbot.

        Returns
        -------
        Union[:class:`.Chatbot`, :class:`.ChatbotResult`]
            The Chatbot object or the ChatbotResult object. ``ChatbotResult`` is returned if ``message`` is provided and ``await`` is used else ``Chatbot``.
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
        return await self._handle_encode_decode("ENCODE", "base64", input)

    async def decode_base64(self, input: str) -> EncodeResult:
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
        return await self._handle_encode_decode("DECODE", "base64", input)

    async def encode_binary(self, input: str) -> EncodeResult:
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
        return await self._handle_encode_decode("ENCODE", "binary", input)

    async def decode_binary(self, input: str) -> EncodeResult:
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
        return await self._handle_encode_decode("DECODE", "binary", input)

    async def generate_bot_token(self, bot_id: Union[str, int]) -> str:
        """Generate a very realistic bot token

        Parameters
        ----------
        bot_id: Union[:class:`str`, :class:`int`]
            The bot ID to generate the token for.

        Returns
        -------
        :class:`str`
            The generated token.
        """
        res = await self._http.request(OthersEndpoint.BOTTOKEN, id=bot_id)
        return res["token"]

    async def dictionary(self, word: str) -> Dictionary:
        """Get the dictionary meaning of a word.

        Parameters
        ----------
        word: :class:`str`
            The word to get the meaning of.

        Returns
        -------
        :class:`.Dictionary`
            Object representing the dictionary result.
        """
        res = await self._http.request(OthersEndpoint.DICTIONARY, word=word)
        return Dictionary.from_dict(**res)

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
        res = await self._http.request(OthersEndpoint.LYRICS, title=song_title)
        return Lyrics.from_dict(**res)  # type: ignore

    async def random_joke(self) -> str:
        """Get a random joke.

        Returns
        -------
        :class:`str`
            The joke.
        """
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
        :class:`.RGB`
            Object containing the RGB values. Use ``.as_tuple`` to get a tuple with the RGB values (``(r, g, b)``).
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
        discriminator: Optional[Union[int, str]] = None,
        server_name: Optional[str] = None,
        member_count: Optional[int] = None,
        text_color: Optional[WelcomeTextColor] = None,
        key: Optional[str] = None,
        font: Optional[int] = None,
    ) -> WelcomeFree:
        """Generate a welcome image.

        Parameters
        ----------
        obj: Optional[:class:`.WelcomeFree`]
            The object to use. If not passed, the other parameters will be used and a new object will be created.
        template: Optional[Literal[1, 2, 3, 4, 5, 6, 7, 8]]
            The template to use. Required if ``obj`` is not passed.
        type: Optional[:class:`.WelcomeType`]
            The type of welcome image to generate. Required if ``obj`` is not passed.
        background: Optional[:class:`.WelcomeBackground`]
            The background to use. Required if ``obj`` is not passed.
        avatar_url: Optional[:class:`str`]
            The avatar URL to use. Required if ``obj`` is not passed.
        username: Optional[:class:`str`]
            The username to use. Required if ``obj`` is not passed.
        discriminator: Optional[Union[:class:`int`, :class:`str`]]
            The discriminator to use. Required if ``obj`` is not passed.
        server_name: Optional[:class:`str`]
            The server name to use. Required if ``obj`` is not passed.
        member_count: Optional[:class:`int`]
            The member count to use. Required if ``obj`` is not passed.
        text_color: Optional[:class:`.WelcomeTextColor`]
            The text color to use. Required if ``obj`` is not passed.
        key: Optional[:class:`str`]
            The key to use. Required if a key was not passed when creating the client.
        font: Optional[:class:`int`]
            The font to use.
        """
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
