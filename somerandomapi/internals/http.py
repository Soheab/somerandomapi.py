from __future__ import annotations
from typing import (
    Coroutine,
    Literal,
    Optional,
    Tuple,
    ClassVar,
    Type,
    Union,
    Dict,
    Any,
    TYPE_CHECKING,
    TypeVar,
    overload,
    Dict,
    List,
)

import json
import aiohttp


from ..errors import *
from ..models.image import Image
from ..clients.animal import Animal
from ..clients.canvas import Canvas
from ..clients.animu import Animu

if TYPE_CHECKING:
    from .endpoints import (
        BaseEndpoint,
        Endpoint,
        CanvasFilter,
        CanvasMisc,
        CanvasOverlay,
        Animal as AnimalEndpoint,
        Facts as FactsEndpoint,
        Img as ImgEndpoint,
        Premium as PremiumEndpoint,
        Animu as AnimuEndpoint,
        Others as OthersEndpoint,
        Chatbot as ChatbotEndpoint,
        WelcomeImages as WelcomeImagesEndpoint,
        Pokemon as PokemonEndpoint,
    )
    from ..types.http import APIKeys
    from ..types.animu import AnimuQuote as AnimuQuotePayload, Animu as AnimuPayload
    from ..types.animal import Animal as AnimalPayload
    from ..types.img import Img as ImgPayload
    from ..types.facts import Fact as FactPayload
    from ..types.others import (
        Joke as JokePayload,
        Lyrics as LyricsPayload,
        BotToken as BotTokenPayload,
        Base64 as Base64Payload,
        Binary as BinaryPayload,
        Dictionary as DictionaryPayload,
    )
    from ..types.chatbot import Chatbot as ChatbotPayload
    from ..types.pokemon import (
        PokemonAbility as PokemonAbilityPayload,
        PokemonItem as PokemonItemPayload,
        PokemonMove as PokemonMovePayload,
        PokeDex as PokeDexPayload,
    )
    from ..types.canvas.misc import RGB as RGBPayload, Hex as HexPayload

    T = TypeVar("T")
    Response = Coroutine[Any, Any, T]


# source: https://github.com/Rapptz/discord.py/blob/master/discord/http.py
async def json_or_text(response: aiohttp.ClientResponse) -> Union[Dict[str, Any], str]:
    text = await response.text(encoding="utf-8")
    if response.content_type == "application/json":
        return json.loads(text)

    return text


class HTTPClient:
    BASE_URL: ClassVar[str] = "https://some-random-api.ml"

    __slots__: Tuple[str, ...] = (
        "_keys",
        "_session",
        "_canvas",
        "_animu",
        "_animal",
    )

    def __init__(self, session: Optional[aiohttp.ClientSession] = None, keys: Optional[APIKeys] = None) -> None:
        self._session: Optional[aiohttp.ClientSession] = session
        self._keys: Optional[APIKeys] = keys

        self._canvas: Canvas = Canvas(self)
        self._animu: Animu = Animu(self)
        self._animal: Animal = Animal(self)

    async def initiate_session(self) -> None:
        if not self._session:
            self._session = aiohttp.ClientSession()

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
    async def request(self, endpoint: Union[CanvasFilter, CanvasOverlay], /, **parameters: Any) -> Image:
        ...

    @overload
    async def request(self, endpoint: Literal[CanvasMisc.TWEET], /, **parameters: Any) -> Image:
        ...

    @overload
    async def request(self, endpoint: Literal[CanvasMisc.HEX], /, **parameters: Any) -> HexPayload:
        ...

    @overload
    async def request(self, endpoint: Literal[CanvasMisc.RGB], /, **parameters: Any) -> RGBPayload:
        ...

    @overload
    async def request(self, endpoint: Literal[CanvasMisc.YOUTUBE_COMMENT], /, **parameters: Any) -> Image:
        ...

    @overload
    async def request(self, endpoint: Literal[CanvasMisc.SIMPCARD], /, **parameters: Any) -> Image:
        ...

    @overload
    async def request(self, endpoint: Literal[CanvasMisc.COLOR_VIEWER], /, **parameters: Any) -> Image:
        ...

    @overload
    async def request(self, endpoint: Literal[CanvasMisc.GENSHIN_NAMECARD], /, **parameters: Any) -> Image:
        ...

    @overload
    async def request(self, endpoint: CanvasMisc, /, **parameters: Any) -> Image:
        ...

    # premium
    @overload
    async def request(self, endpoint: PremiumEndpoint, /, **parameters: Any) -> Image:
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
    async def request(self, endpoint: OthersEndpoint, /, **parameters: Any) -> Union[JokePayload, LyricsPayload, BotTokenPayload, Base64Payload, BinaryPayload, DictionaryPayload]:
        ...

    # chatbot
    @overload
    async def request(self, endpoint: Literal[ChatbotEndpoint.CHATBOT], /, **parameters: Any) -> ChatbotPayload:
        ...

    # welcome
    @overload
    async def request(self, endpoint: Literal[WelcomeImagesEndpoint.WELCOME], /, **parameters: Any) -> Image:
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
    async def request(self, endpoint: PokemonEndpoint, /, **parameters: Any) -> Union[PokeDexPayload, PokemonAbilityPayload, PokemonMovePayload, PokemonItemPayload]:
        ...

    # org
    @overload
    async def request(self, endpoint: BaseEndpoint, /, **parameters: Any) -> Any:
        ...

    async def request(self, enum: BaseEndpoint, /, **parameters: Any) -> Any:
        endpoint: Endpoint = enum.value
        if endpoint.parameters:
            if not parameters:
                raise ValueError(f"Endpoint {endpoint.path} requires parameters.")

            endpoint._set_param_values(self._keys, **parameters)

        url = endpoint.get_constructed_url(enum)

        await self.initiate_session()
        if not self._session:
            raise RuntimeError("Session is not initialized. This should never happen.")

        full_url = f"{self.BASE_URL}/{url}"
        print("requesting", full_url, parameters)
        async with self._session.get(full_url) as response:
            data = response
            if response.content_type.startswith("image/"):
                if response.status == 200:
                    return Image(full_url, self._session)
            else:
                data = await json_or_text(response)
            if response.status == 200:
                return data

            elif response.status == 400:
                raise BadRequest(data)
            elif response.status == 403:
                raise Forbidden(data)
            elif response.status == 404:
                raise NotFound(data)
            elif response.status == 429:
                raise RateLimited(data)
            elif response.status == 500:
                raise InternalServerError(data)
            else:
                raise HTTPException(response, data)

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()

        self._session = None  # type: ignore
