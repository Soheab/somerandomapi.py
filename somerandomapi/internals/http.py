from __future__ import annotations

import json
from typing import Any, ClassVar, Coroutine, Literal, NamedTuple, Optional, overload, TYPE_CHECKING, TypeVar, Union
from urllib.parse import quote_plus, urlencode

import aiohttp

from ..clients.animal import AnimalClient
from ..clients.animu import AnimuClient
from ..clients.canvas import CanvasClient
from ..clients.pokemon import PokemonClient
from ..clients.premium import PremiumClient
from ..errors import *
from ..models.image import Image
from ..models.welcome import WelcomeFree, WelcomePremium


if TYPE_CHECKING:
    from ..clients.chatbot import Chatbot
    from ..types.animal import Animal as AnimalPayload
    from ..types.animu import Animu as AnimuPayload, AnimuQuote as AnimuQuotePayload
    from ..types.canvas.misc import Hex as HexPayload, RGB as RGBPayload
    from ..types.chatbot import Chatbot as ChatbotPayload
    from ..types.facts import Fact as FactPayload
    from ..types.img import Img as ImgPayload
    from ..types.others import (
        Base64 as Base64Payload,
        Binary as BinaryPayload,
        BotToken as BotTokenPayload,
        Dictionary as DictionaryPayload,
        Joke as JokePayload,
        Lyrics as LyricsPayload,
    )
    from ..types.pokemon import (
        PokeDex as PokeDexPayload,
        PokemonAbility as PokemonAbilityPayload,
        PokemonItem as PokemonItemPayload,
        PokemonMove as PokemonMovePayload,
    )
    from .endpoints import (
        Animal as AnimalEndpoint,
        Animu as AnimuEndpoint,
        BaseEndpoint,
        CanvasFilter,
        CanvasMisc,
        CanvasOverlay,
        Chatbot as ChatbotEndpoint,
        Endpoint,
        Facts as FactsEndpoint,
        Img as ImgEndpoint,
        Others as OthersEndpoint,
        Pokemon as PokemonEndpoint,
        Premium as PremiumEndpoint,
        WelcomeImages as WelcomeImagesEndpoint,
    )

    T = TypeVar("T")
    Response = Coroutine[Any, Any, T]


__all__ = ()


async def json_or_text(response: aiohttp.ClientResponse) -> Union[dict[str, Any], str]:
    text = await response.text(encoding="utf-8")
    if response.content_type == "application/json":
        return json.loads(text)

    return text


class APIKey(NamedTuple):
    tier: Literal[0, 1, 2, 3]
    value: str


class HTTPClient:
    BASE_URL: ClassVar[str] = "https://some-random-api.com"

    __slots__ = ("_animal", "_animu", "_canvas", "_pokemon", "_premium", "_key", "_session", "__chatbot")

    def __init__(
        self,
        key: Optional[tuple[Literal[0, 1, 2, 3], str]],
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        self._key: Optional[APIKey] = APIKey(*key) if key else None
        self._animal: AnimalClient = AnimalClient(self)
        self._animu: AnimuClient = AnimuClient(self)
        self._canvas: CanvasClient = CanvasClient(self)
        self._pokemon: PokemonClient = PokemonClient(self)
        self._premium: PremiumClient = PremiumClient(self)

        self.__chatbot: Optional[Chatbot] = None

        self._session: Optional[aiohttp.ClientSession] = session

    async def initiate_session(self) -> None:
        if not self._session or self._session.closed:
            self._session = aiohttp.ClientSession()

    ImageEndpoints = Union[
        "CanvasFilter",
        "CanvasOverlay",
        "Literal[CanvasMisc.TWEET]",
        "Literal[CanvasMisc.YOUTUBE_COMMENT]",
        "Literal[CanvasMisc.SIMPCARD]",
        "Literal[CanvasMisc.COLOR_VIEWER]",
        "Literal[CanvasMisc.GENSHIN_NAMECARD]",
        "PremiumEndpoint",
        "Literal[WelcomeImagesEndpoint.WELCOME]",
    ]

    # isort: off
    # fmt: off
    # all Image
    @overload
    async def request(self, endpoint: ImageEndpoints, /, **parameters: Any) -> Image:
        ...
    # animu
    @overload
    async def request(self, endpoint: Literal[AnimuEndpoint.QUOTE], /, **parameters: Any) -> AnimuQuotePayload:
        ...
    @overload
    async def request(
        self,
        endpoint: Literal[AnimuEndpoint.FACE_PALM, AnimuEndpoint.HUG, AnimuEndpoint.PAT, AnimuEndpoint.WINK],
        /,
        **parameters: Any,
    ) -> AnimuPayload:
        ...
    # animals
    @overload
    async def request(self, endpoint: AnimalEndpoint, /, **parameters: Any) -> AnimalPayload:
        ...
    @overload
    async def request(self, endpoint: ImgEndpoint, /, **parameters: Any) -> ImgPayload:
        ...
    @overload
    async def request(self, endpoint: FactsEndpoint, /, **parameters: Any) -> FactPayload:
        ...
    # canvas
    @overload
    async def request(self, endpoint: CanvasOverlay, /, **parameters: Any) -> Image:
        ...
    @overload
    async def request(self, endpoint: CanvasFilter, /, **parameters: Any) -> Image:
        ...
    @overload
    async def request(
        self,
        endpoint: Literal[
            CanvasMisc.TWEET,
            CanvasMisc.YOUTUBE_COMMENT,
            CanvasMisc.SIMPCARD,
            CanvasMisc.COLOR_VIEWER,
            CanvasMisc.GENSHIN_NAMECARD,
        ],
        /,
        **parameters: Any,
    ) -> Image:
        ...
    @overload
    async def request(self, endpoint: Literal[CanvasMisc.HEX], /, **parameters: Any) -> HexPayload:
        ...
    @overload
    async def request(self, endpoint: Literal[CanvasMisc.RGB], /, **parameters: Any) -> RGBPayload:
        ...
    # others
    @overload
    async def request(self, endpoint: Literal[OthersEndpoint.JOKE], /, **parameters: Any) -> JokePayload:
        ...
    @overload
    async def request(self, endpoint: Literal[OthersEndpoint.LYRICS], /, **parameters: Any) -> LyricsPayload:
        ...
    @overload
    async def request(self, endpoint: Literal[OthersEndpoint.BOTTOKEN], /, **parameters: Any) -> BotTokenPayload:
        ...
    @overload
    async def request(self, endpoint: Literal[OthersEndpoint.BASE64], /, **parameters: Any) -> Base64Payload:
        ...
    @overload
    async def request(self, endpoint: Literal[OthersEndpoint.BINARY], /, **parameters: Any) -> BinaryPayload:
        ...
    @overload
    async def request(self, endpoint: Literal[OthersEndpoint.DICTIONARY], /, **parameters: Any) -> DictionaryPayload:
        ...
    @overload
    async def request(
        self, endpoint: OthersEndpoint, /, **parameters: Any
    ) -> Union[JokePayload, LyricsPayload, BotTokenPayload, Base64Payload, BinaryPayload, DictionaryPayload]:
        ...
    # chatbot
    @overload
    async def request(self, endpoint: Literal[ChatbotEndpoint.CHATBOT], /, **parameters: Any) -> ChatbotPayload:
        ...
    # pokemon
    @overload
    async def request(
        self, endpoint: Literal[PokemonEndpoint.ABILITIES], /, **parameters: Any
    ) -> PokemonAbilityPayload:
        ...
    @overload
    async def request(self, endpoint: Literal[PokemonEndpoint.MOVES], /, **parameters: Any) -> PokemonMovePayload:
        ...
    @overload
    async def request(self, endpoint: Literal[PokemonEndpoint.ITEMS], /, **parameters: Any) -> PokemonItemPayload:
        ...
    @overload
    async def request(self, endpoint: Literal[PokemonEndpoint.POKEDEX], /, **parameters: Any) -> PokeDexPayload:
        ...
    @overload
    async def request(
        self, endpoint: PokemonEndpoint, /, **parameters: Any
    ) -> Union[PokeDexPayload, PokemonAbilityPayload, PokemonMovePayload, PokemonItemPayload]:
        ...
    # welcome
    @overload
    async def request(self, endpoint: Literal[WelcomeImagesEndpoint.WELCOME], /, **parameters: Any) -> Image:
        ...
    # premium
    @overload
    async def request(self, endpoint: PremiumEndpoint, /, **parameters: Any) -> Image:
        ...
    # org
    @overload
    async def request(self, endpoint: BaseEndpoint, /, **parameters: Any) -> Any:
        ...
    # fmt: on
    # isort: on

    async def request(self, enum: BaseEndpoint, /, *, pre_url: Optional[str] = None, **parameters: Any) -> Any:
        endpoint: Endpoint = enum.value
        if not pre_url:
            if endpoint.parameters:
                if not parameters:
                    raise ValueError(f"Endpoint {endpoint.path} requires parameters.")

                endpoint._set_param_values(self._key, **parameters)

            url = endpoint.get_constructed_url(enum)
            full_url = f"{self.BASE_URL}/{url}"
        else:
            full_url = pre_url

        await self.initiate_session()
        if not self._session:
            raise RuntimeError("Session is not initialized. This should never happen.")

        async with self._session.get(full_url) as response:
            if not response.content_type.startswith("image/"):
                data = await json_or_text(response)
            else:
                data = response

            if response.status == 200:
                if response.content_type.startswith("image/"):
                    return Image.construct(full_url, self)

                return data

            elif response.status == 400:
                raise BadRequest(enum, data)
            elif response.status == 403:
                raise Forbidden(enum, data)
            elif response.status == 404:
                raise NotFound(enum, data)
            elif response.status == 429:
                raise RateLimited(enum, data)
            elif response.status == 500:
                raise InternalServerError(enum, data)
            else:
                raise HTTPException(enum, response, data)

    async def _get_image_url(self, url: str, /) -> bytes:
        await self.initiate_session()
        if not self._session:
            raise RuntimeError("Session is not initialized. This should never happen.")

        async with self._session.get(url) as response:
            if response.status == 200:
                return await response.read()

            raise ImageError(url, response.status)

    async def _welcome_card(self, enum: BaseEndpoint, card: Union[WelcomeFree, WelcomePremium]) -> Image:
        data = card.to_dict()
        background = data.pop("background", None)
        template = data.pop("template")
        endpoint: Endpoint = enum.value
        if endpoint.parameters:
            endpoint._set_param_values(self._key, **data)

        if not template:
            raise ValueError("Template is required for welcome card.")

        url = f"{self.BASE_URL}/{enum.base()}{template}"

        if background is not None:
            url += f"/{background}"
        if endpoint.parameters:
            params = {name: param.value for name, param in endpoint.parameters.items() if param.value is not None}
            url += "?" + urlencode(params, quote_via=quote_plus)

        return await self.request(enum, pre_url=url)

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()

        if self.__chatbot:
            await self.__chatbot.close()

        self._session = None
        self.__chatbot = None
