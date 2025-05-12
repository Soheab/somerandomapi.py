from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Literal, TypeVar, overload
from collections.abc import Coroutine
import json
import logging

import aiohttp

from .. import utils as _utils
from ..clients.animal import AnimalClient
from ..clients.animu import AnimuClient
from ..clients.canvas import CanvasClient
from ..clients.pokemon import PokemonClient
from ..clients.premium import PremiumClient
from ..errors import *
from ..models.image import Image
from .endpoints import Endpoint, _Endpoint

if TYPE_CHECKING:
    from ..clients.chatbot import Chatbot
    from ..types import (
        animal as animaltypes,
        animu as animutypes,
        canvas as canvastypes,
        facts as facttypes,
        http as httptypes,
        img as imgtypes,
        pokemon as pokemontypes,
    )

    T = TypeVar("T")
    Response = Coroutine[Any, Any, T]


__all__ = ()

_log: logging.Logger = logging.getLogger("somerandomapi.http")


async def json_or_text(response: aiohttp.ClientResponse) -> dict[str, Any] | str:
    text = await response.text(encoding="utf-8")
    if response.content_type == "application/json":
        return json.loads(text)

    return text


AllAnimuEndpoint = Literal[
    _Endpoint.ANIMU_NOM,
    _Endpoint.ANIMU_POKE,
    _Endpoint.ANIMU_CRY,
    _Endpoint.ANIMU_KISS,
    _Endpoint.ANIMU_PAT,
    _Endpoint.ANIMU_HUG,
]
AllAnimalEndpoint = Literal[
    _Endpoint.ANIMAL_FOX,
    _Endpoint.ANIMAL_CAT,
    _Endpoint.ANIMAL_BIRD,
    _Endpoint.ANIMAL_PANDA,
    _Endpoint.ANIMAL_RACCOON,
    _Endpoint.ANIMAL_KOALA,
    _Endpoint.ANIMAL_KANGAROO,
    _Endpoint.ANIMAL_WHALE,
    _Endpoint.ANIMAL_DOG,
    _Endpoint.ANIMAL_REDPANDA,
]

AllFactsEndpoint = Literal[
    _Endpoint.FACTS_CAT,
    _Endpoint.FACTS_FOX,
    _Endpoint.FACTS_PANDA,
    _Endpoint.FACTS_KOALA,
    _Endpoint.FACTS_KANGAROO,
    _Endpoint.FACTS_RACCOON,
    _Endpoint.FACTS_GIRAFFE,
    _Endpoint.FACTS_WHALE,
    _Endpoint.FACTS_ELEPHANT,
    _Endpoint.FACTS_DOG,
    _Endpoint.FACTS_BIRD,
]

AllImgEndpoint = Literal[
    _Endpoint.IMG_FOX,
    _Endpoint.IMG_CAT,
    _Endpoint.IMG_PANDA,
    _Endpoint.IMG_RED_PANDA,
    _Endpoint.IMG_PIKACHU,
    _Endpoint.IMG_RACOON,
    _Endpoint.IMG_KOALA,
    _Endpoint.IMG_KANGAROO,
    _Endpoint.IMG_WHALE,
    _Endpoint.IMG_DOG,
    _Endpoint.IMG_BIRD,
]

AllFiltersEndpoint = Literal[
    _Endpoint.CANVAS_FILTER_BLUE,
    _Endpoint.CANVAS_FILTER_BLURPLE,
    _Endpoint.CANVAS_FILTER_BLURPLE_2,
    _Endpoint.CANVAS_FILTER_GREEN,
    _Endpoint.CANVAS_FILTER_GREYSCALE,
    _Endpoint.CANVAS_FILTER_INVERT,
    _Endpoint.CANVAS_FILTER_INVERT_GREYSCALE,
    _Endpoint.CANVAS_FILTER_RED,
    _Endpoint.CANVAS_FILTER_SEPIA,
    _Endpoint.CANVAS_FILTER_BLUR,
    _Endpoint.CANVAS_FILTER_PIXELATE,
]

EndpointWithNoParameters = Literal[
    _Endpoint.BOTTOKEN,
    _Endpoint.JOKE,
    AllAnimuEndpoint,
    AllAnimalEndpoint,
    AllFactsEndpoint,
    AllImgEndpoint,
]
EndpointWithImageResult = Literal[
    _Endpoint.CANVAS_COLORVIEWER,
    _Endpoint.CANVAS_FILTER_BLUE,
    _Endpoint.CANVAS_FILTER_BLURPLE,
    _Endpoint.CANVAS_FILTER_BLURPLE_2,
    _Endpoint.CANVAS_FILTER_BRIGHTNESS,
    _Endpoint.CANVAS_FILTER_COLOR,
    _Endpoint.CANVAS_FILTER_GREEN,
    _Endpoint.CANVAS_FILTER_GREYSCALE,
    _Endpoint.CANVAS_FILTER_INVERT,
    _Endpoint.CANVAS_FILTER_INVERT_GREYSCALE,
    _Endpoint.CANVAS_FILTER_RED,
    _Endpoint.CANVAS_FILTER_SEPIA,
    _Endpoint.CANVAS_FILTER_THRESHOLD,
    _Endpoint.CANVAS_FILTER_BLUR,
    _Endpoint.CANVAS_FILTER_PIXELATE,
    _Endpoint.CANVAS_MISC_BISEXUAL,
    _Endpoint.CANVAS_MISC_CIRCLE,
    _Endpoint.CANVAS_MISC_HEART,
    _Endpoint.CANVAS_MISC_HORNY,
    _Endpoint.CANVAS_MISC_ITS_SO_STUPID,
    _Endpoint.CANVAS_MISC_LESBIAN,
    _Endpoint.CANVAS_MISC_LGBT,
    _Endpoint.CANVAS_MISC_LIED,
    _Endpoint.CANVAS_MISC_LOLICE,
    _Endpoint.CANVAS_MISC_GENSHIN_NAMECARD,
    _Endpoint.CANVAS_MISC_NO_BITCHES,
    _Endpoint.CANVAS_MISC_NONBINARY,
    _Endpoint.CANVAS_MISC_OOGWAY,
    _Endpoint.CANVAS_MISC_OOGWAY2,
    _Endpoint.CANVAS_MISC_PANSEXUAL,
    _Endpoint.CANVAS_MISC_SIMPCARD,
    _Endpoint.CANVAS_MISC_SPIN,
    _Endpoint.CANVAS_MISC_TONIKAWA,
    _Endpoint.CANVAS_MISC_TRANSGENDER,
    _Endpoint.CANVAS_MISC_TWEET,
    _Endpoint.CANVAS_MISC_YOUTUBE_COMMENT,
    _Endpoint.CANVAS_OVERLAY_COMRADE,
    _Endpoint.CANVAS_OVERLAY_GAY,
    _Endpoint.CANVAS_OVERLAY_GLASS,
    _Endpoint.CANVAS_OVERLAY_JAIL,
    _Endpoint.CANVAS_OVERLAY_PASSED,
    _Endpoint.CANVAS_OVERLAY_TRIGGERED,
    _Endpoint.CANVAS_OVERLAY_WASTED,
    _Endpoint.PREMIUM_AMONGUS,
    _Endpoint.PREMIUM_PETPET,
    _Endpoint.PREMIUM_RANK_CARD,
    _Endpoint.PREMIUM_WELCOME,
]
EndpointsWithAvatarParameter = Literal[
    # fitlers
    AllFiltersEndpoint,
    # misc
    _Endpoint.CANVAS_MISC_CIRCLE,
    _Endpoint.CANVAS_MISC_HEART,
    _Endpoint.CANVAS_MISC_HORNY,
    _Endpoint.CANVAS_MISC_ITS_SO_STUPID,
    _Endpoint.CANVAS_MISC_LESBIAN,
    _Endpoint.CANVAS_MISC_LGBT,
    _Endpoint.CANVAS_MISC_LOLICE,
    _Endpoint.CANVAS_MISC_NONBINARY,
    _Endpoint.CANVAS_MISC_PANSEXUAL,
    _Endpoint.CANVAS_MISC_SIMPCARD,
    _Endpoint.CANVAS_MISC_SPIN,
    _Endpoint.CANVAS_MISC_TONIKAWA,
    _Endpoint.CANVAS_MISC_TRANSGENDER,
    # overlay
    _Endpoint.CANVAS_OVERLAY_COMRADE,
    _Endpoint.CANVAS_OVERLAY_GAY,
    _Endpoint.CANVAS_OVERLAY_GLASS,
    _Endpoint.CANVAS_OVERLAY_JAIL,
    _Endpoint.CANVAS_OVERLAY_PASSED,
    _Endpoint.CANVAS_OVERLAY_TRIGGERED,
    _Endpoint.CANVAS_OVERLAY_WASTED,
    # premium
    _Endpoint.PREMIUM_PETPET,
]


class HTTPClient:
    BASE_URL: ClassVar[str] = "https://api.some-random-api.com"
    USER_AGENT = "somerandomapi.py (https://github.com/soheab/somerandomapi.py)"

    __slots__ = (
        "__chatbot",
        "__user_provided_session",
        "_animal",
        "_animu",
        "_canvas",
        "_pokemon",
        "_premium",
        "_session",
        "_token",
    )

    def __init__(self, token: str | None, session: aiohttp.ClientSession | None) -> None:
        self._token: str | None = token

        self._animal: AnimalClient = AnimalClient(self)
        self._animu: AnimuClient = AnimuClient(self)
        self._canvas: CanvasClient = CanvasClient(self)
        self._pokemon: PokemonClient = PokemonClient(self)
        self._premium: PremiumClient = PremiumClient(self)

        self.__chatbot: Chatbot | None = None

        if session is not _utils.NOVALUE and session is None:
            _log.warning(
                (
                    "You passed `None` to the `session` keyword-argument. This behavior is deprecated and will raise an "
                    "error in the future. Please pass a `aiohttp.ClientSession` instance or leave it empty."
                ),
                FutureWarning,
            )

        self.__user_provided_session: bool = session is not _utils.NOVALUE and session is not None
        self._session: aiohttp.ClientSession | None = session

    async def initiate_session(self) -> aiohttp.ClientSession:
        if not self._session or self._session.closed:
            if self.__user_provided_session:
                _log.debug("Session is closed, but user provided it.")
            _log.debug("Creating a new session.")
            self._session = aiohttp.ClientSession()

        self._session.headers["User-Agent"] = self.USER_AGENT
        if self._token:
            self._session.headers["Authorization"] = str(self._token)
        return self._session

    # BASE
    @overload
    async def request(
        self, _endpoint: Literal[_Endpoint.BASE64,], /, *, encode: str | None = ..., decode: str | None = ...
    ) -> httptypes.Base64: ...
    @overload
    async def request(
        self, _endpoint: Literal[_Endpoint.BINARY,], /, *, encode: str | None = ..., decode: str | None = ...
    ) -> httptypes.Binary: ...
    @overload
    async def request(
        self,
        _endpoint: Literal[_Endpoint.BOTTOKEN],
        /,
    ) -> httptypes.BotToken: ...
    @overload
    async def request(
        self,
        _endpoint: Literal[_Endpoint.CHATBOT],
        /,
        *,
        message: str,
    ) -> httptypes.Chatbot: ...
    @overload
    async def request(
        self,
        _endpoint: Literal[_Endpoint.LYRICS],
        /,
        *,
        title: str,
    ) -> httptypes.Lyrics: ...

    # ANIMU
    @overload
    async def request(
        self,
        _endpoint: AllAnimuEndpoint,
        /,
    ) -> animutypes.Animu: ...
    @overload
    async def request(
        self,
        _endpoint: Literal[_Endpoint.ANIMU_QUOTE],
        /,
    ) -> animutypes.AnimuQuote: ...

    # ANIMAL
    @overload
    async def request(
        self,
        _endpoint: AllAnimalEndpoint,
        /,
    ) -> animaltypes.Animal: ...

    # FACTS
    @overload
    async def request(
        self,
        _endpoint: AllFactsEndpoint,
        /,
    ) -> facttypes.Fact: ...

    # IMG
    @overload
    async def request(
        self,
        _endpoint: AllImgEndpoint,
        /,
    ) -> imgtypes.Img: ...

    # CANVAS
    # base
    @overload
    async def request(
        self,
        _endpoint: Literal[_Endpoint.CANVAS_COLORVIEWER],
        /,
        *,
        hex: str,
    ) -> Image: ...
    @overload
    async def request(
        self,
        _endpoint: Literal[_Endpoint.CANVAS_HEX],
        /,
        *,
        rgb: str,
    ) -> canvastypes.Hex: ...
    @overload
    async def request(
        self,
        _endpoint: Literal[_Endpoint.CANVAS_RGB],
        /,
        *,
        hex: str,
    ) -> canvastypes.RGB: ...
    # filters
    @overload
    async def request(
        self,
        _endpoint: AllFiltersEndpoint,
        /,
        *,
        avatar: str,
    ) -> Image: ...

    @overload
    async def request(
        self,
        _endpoint: Literal[_Endpoint.CANVAS_FILTER_BRIGHTNESS],
        /,
        *,
        avatar: str,
        brightness: int,
    ) -> Any: ...

    @overload
    async def request(
        self,
        _endpoint: Literal[_Endpoint.CANVAS_FILTER_COLOR,],
        /,
        *,
        avatar: str,
        color: str,
    ) -> Any: ...

    @overload
    async def request(
        self,
        _endpoint: Literal[_Endpoint.CANVAS_FILTER_THRESHOLD],
        /,
        *,
        avatar: str,
        threshold: int,
    ) -> Any: ...
    # misc
    @overload
    async def request(
        self,
        _endpoint: Literal[_Endpoint.CANVAS_MISC_LIED],
        /,
        *,
        avatar: str,
        username: str,
    ) -> Any: ...
    @overload
    async def request(
        self,
        _endpoint: Literal[_Endpoint.CANVAS_MISC_GENSHIN_NAMECARD],
        /,
        *,
        avatar: str,
        birthday: str,
        username: str,
        description: str,
    ) -> Any: ...
    @overload
    async def request(
        self,
        _endpoint: Literal[_Endpoint.CANVAS_MISC_NO_BITCHES],
        /,
        *,
        avatar: str,
        no: bool,
        bottomtext: str | None = None,
    ) -> Any: ...

    @overload
    async def request(
        self,
        _endpoint: Literal[_Endpoint.CANVAS_MISC_OOGWAY, _Endpoint.CANVAS_MISC_OOGWAY2],
        /,
        *,
        avatar: str,
        quote: str,
    ) -> Image: ...
    @overload
    async def request(
        self,
        _endpoint: Literal[_Endpoint.CANVAS_MISC_TWEET],
        /,
        *,
        displayname: str,
        username: str,
        avatar: str,
        comment: str,
        replies: int | None = None,
        likes: int | None = None,
        retweets: int | None = None,
        theme: str | None = None,
    ) -> Image: ...

    @overload
    async def request(
        self,
        _endpoint: Literal[_Endpoint.CANVAS_MISC_YOUTUBE_COMMENT],
        /,
        *,
        username: str,
        avatar: str,
        comment: str,
    ) -> Image: ...

    # POKEMON

    @overload
    async def request(
        self, _endpoint: Literal[_Endpoint.POKEMON_ABILITIES], /, *, ability: str
    ) -> pokemontypes.PokemonAbility: ...

    # PREMIUM

    @overload
    async def request(
        self,
        _endpoint: Literal[_Endpoint.PREMIUM_AMONGUS],
        /,
        *,
        avatar: str,
        username: str,
        custom: str,
    ) -> Response[Image]: ...

    @overload
    async def request(
        self,
        _endpoint: Literal[_Endpoint.PREMIUM_RANK_CARD],
        /,
        *,
        username: str,
        avatar: str,
        discriminator: str | None = None,
        level: str,
        cxp: str,
        nxp: str,
        bg: str | None = None,
        cbg: str | None = None,
        ctext: str | None = None,
        ccxp: str | None = None,
        cbar: str | None = None,
    ) -> Response[Image]: ...

    @overload
    async def request(
        self,
        _endpoint: Literal[_Endpoint.PREMIUM_WELCOME],
        /,
        *,
        template: str,
        type: str,
        username: str,
        avatar: str,
        discriminator: str | None = None,
        guildName: str,
        memberCount: str,
        textcolor: str,
        bg: str | None = None,
        font: str | None = None,
    ) -> Response[Image]: ...

    @overload
    async def request(self, _endpoint: Literal[_Endpoint.POKEMON_ITEMS], /, *, item: str) -> pokemontypes.PokemonItem: ...

    @overload
    async def request(self, _endpoint: Literal[_Endpoint.POKEMON_MOVES], /, *, move: str) -> pokemontypes.PokemonMove: ...

    @overload
    async def request(self, _endpoint: Literal[_Endpoint.POKEMON_POKEDEX], /, *, pokemon: str) -> pokemontypes.PokeDex: ...

    @overload
    async def request(self, _endpoint: EndpointsWithAvatarParameter, /, *, avatar: str) -> Any: ...

    @overload
    async def request(self, _endpoint: EndpointWithImageResult, /, **parameters: Any) -> Image: ...

    @overload
    async def request(self, _endpoint: EndpointWithNoParameters, /) -> Any: ...

    @overload
    async def request(self, _endpoint: Endpoint, /, **parameters: Any) -> Any: ...

    @overload
    async def request(self, _endpoint: _Endpoint, /, **parameters: Any) -> Any: ...

    async def request(self, _endpoint: _Endpoint | Endpoint, /, *, pre_url: str | None = None, **parameters: Any) -> Any:
        endpoint: Endpoint = _endpoint.value if not isinstance(_endpoint, Endpoint) else _endpoint  # type: ignore[reportAssignmentType]
        _log.debug(
            "Request called with endpoint: %s, pre_url: %s and parameters: %s",
            endpoint.path,
            pre_url,
            parameters,
        )
        if not pre_url:
            if endpoint.parameters:
                if not parameters:
                    msg = f"Endpoint {endpoint.path} requires parameters."
                    raise ValueError(msg)

                endpoint._set_param_values(self, **parameters)

            url = endpoint.get_constructed_url()
            full_url = f"{self.BASE_URL}/{url}"
        else:
            full_url = pre_url

        _log.debug("Requesting %s with parameters: %s", full_url, parameters)

        session: aiohttp.ClientSession = await self.initiate_session()

        async with session.get(full_url) as response:
            if not response.content_type.startswith("image/"):
                data = await json_or_text(response)
            else:
                data = response

            if isinstance(data, dict) and data.get("error"):
                # sometimes the api returns a 200 with an error
                _log.debug("Request failed with error: %s and data: %s", data["error"], data)
                # we should show the correct status code
                data["code"] = response.status
                raise BadRequest(endpoint, data)

            if response.status == 200:
                if response.content_type.startswith("image/"):
                    return Image.construct(full_url, self)

                return data

            if response.status == 400:
                _log.debug("Request failed with status code 400: %s", data)
                raise BadRequest(endpoint, data)
            elif response.status == 403:  # noqa: RET506
                _log.debug("Request failed with status code 403: %s", data)
                raise Forbidden(endpoint, data)
            elif response.status == 404:
                _log.debug("Request failed with status code 404: %s", data)
                raise NotFound(endpoint, data)
            elif response.status == 429:
                _log.debug("Request failed with status code 429: %s", data)
                raise RateLimited(endpoint, data)
            elif response.status == 500:
                _log.debug("Request failed with status code 500: %s", data)
                raise InternalServerError(endpoint, data)
            else:
                _log.debug("Request failed with status code %s: %s", response.status, data)
                raise HTTPException(endpoint, response, data)

    async def _get_image_url(self, url: str, /) -> bytes:
        await self.initiate_session()
        if not self._session:
            raise RuntimeError("Session is not initialized. This should never happen.")

        _log.debug("Requesting bytes from %s", url)
        async with self._session.get(url) as response:
            if response.status == 200:
                return await response.read()

            raise ImageError(url, response.status)

    async def close(self) -> None:
        _log.debug("Closing the session and chatbot.")
        if not self.__user_provided_session and self._session and not self._session.closed:
            await self._session.close()
            self._session = None
            _log.debug("Session closed.")

        if self.__chatbot:
            await self.__chatbot.close()
            _log.debug("Chatbot closed.")

        self.__chatbot = None
