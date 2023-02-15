from __future__ import annotations
from typing import TYPE_CHECKING, Any, Literal, Optional, Union, overload, Tuple

from ..internals.http import HTTPClient
from ..internals.endpoints import (
    Others as OthersEndpoint,
    CanvasMisc as CanvasMiscEndpoint,
    WelcomeImages as WelcomeImagesEndpoint,
)
from ..models.lyrics import Lyrics
from ..models.dictionary import Dictionary
from ..models.encoding import EncodeResult
from ..models.rgb import RGB
from ..models.welcome.free import WelcomeFree

from .. import utils as _utils

if TYPE_CHECKING:
    from ..types.http import APIKeys
    from .canvas import Canvas
    from .animu import Animu
    from .animal import Animal
    from ..types.welcome import WelcomeTextColors
    from ..enums import WelcomeType, WelcomeBackground

    from aiohttp import ClientSession


__all__: Tuple[str, ...] = ("Client",)


class Client:
    """Class representing the client for the Some Random API.

    Parameters
    ----------
    session: Optional[:class:`aiohttp.ClientSession`]
        The session to use for requests.

    keys: Optional[Union[:class:`str`, :class:`dict`, :class:`tuple`]]
        The API key(s) to use for the endpoints that require it.

        This can be either a string (`keys="key"`), in which case it will be assumed to be the tier 1 key,
        or a dictionary, with the keys being the tier and the values being the key. For example, ``{"tier_1": "key", "tier_2": "key"}``.
        or a tuple of strings, in which case the first string will be the tier 1 key, the second string will be the tier 2 key, and the
        third string will be the tier 3 key, in that order but not all need to be provided.

        Currently, the only valid tiers are ``tier_1``, ``tier_2``, and ``tier_3``.

        Keys can also be passed per-request, in which case they will override the keys passed to the client.

        For more information on the tiers, see the API documentation: https://somerandomapi.com/docs#api-keys

    """

    __slots__: tuple[str, ...] = ("_http", "__animu_instance", "__animal_instance", "__canvas_instance")

    def __init__(self, session: Optional[ClientSession] = None, *, keys: Optional[Union[str, APIKeys]] = None) -> None:
        keys_dict: APIKeys = {"tier_1": None, "tier_2": None, "tier_3": None}
        if keys is not None:
            if isinstance(keys, str):
                keys_dict["tier_1"] = keys
            elif isinstance(keys, dict):
                invalid_keys = [key for key in keys if key not in keys_dict]
                if invalid_keys:
                    raise ValueError(
                        f"Invalid key(s) passed to 'keys': {', '.join(invalid_keys)}. Valid keys are: {', '.join(keys_dict.keys())}"
                    )
                keys_dict.update(keys)
            elif isinstance(keys, tuple):
                if len(keys) > 3:
                    raise ValueError(f"Expected 'keys' tuple to be of length 3 or less. Got {len(keys)}")
                for i, key in enumerate(keys, start=1):
                    keys_dict[f"tier_{i}"] = key
            else:
                raise TypeError(
                    f"Expected 'keys` to be either a string, " + "dict{}" + "or tuple()." + f"Not {type(keys)}"
                )

        self._http = HTTPClient(session, keys_dict)

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

    async def _handle_encode_decode(
        self, what: Literal["ENCODE", "DECODE"], name: Literal["base64", "binary"], _input: str
    ) -> EncodeResult:
        _type_to_endpoint = {"base64": OthersEndpoint.BASE64, "binary": OthersEndpoint.BINARY}
        res = await self._http.request(_type_to_endpoint[name], **{what.lower(): _input})
        print("ecndeo edco result", res)
        return EncodeResult.from_dict(
            _input=_input,
            _type=what.upper(),  # type: ignore
            text=res[name.lower() if what == "ENCODE" else "text"],
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
        print("rgb or hex", endpoint, input, kwarga)
        res = await self._http.request(endpoint, **kwarga)
        if endpoint == CanvasMiscEndpoint.HEX:
            return res["hex"]  # type: ignore
        else:
            return RGB.from_dict(res)  # type: ignore

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
        # print("rgb to hex", input, self)
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
        # print("hex to rgb", input, self)
        return await self._handle_rgb_or_hex(CanvasMiscEndpoint.RGB, hex)

    async def welcome_image(
        self,
        obj: Optional[WelcomeFree] = None,
        *,
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
        res = await self._http.request(endpoint, **obj.to_dict())
        new = obj.copy()
        new._image = res
        return new

    async def close(self) -> None:
        """Close the client session."""
        await self._http.close()
