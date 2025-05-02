from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self
from collections.abc import Callable
import logging
from urllib.parse import quote_plus, urlencode

from .. import enums

if TYPE_CHECKING:
    from .http import HTTPClient


_log: logging.Logger = logging.getLogger("somerandomapi.endpoints")


class Endpoint:
    __slots__: tuple[str, ...] = (
        "parameters",
        "path",
    )

    def __init__(
        self,
        path: str,
        **parameters: Parameter,
    ) -> None:
        self.path: str = path
        self.parameters: dict[str, Parameter] = parameters.copy()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} path={self.path!r} parameters={len(self.parameters)}>"

    def _set_param_values(self, client: HTTPClient, **values: Any) -> Self:
        _log.debug("Setting parameter values for %r endpoint", self.path)
        # new class to avoid mutating the original
        cls = self.__class__(self.path, **self.parameters)
        params = cls.parameters.copy()

        if not params:
            _log.debug("No parameters found for %r endpoint", self.path)
            return cls

        for name, param in params.items():
            if not param.required and name not in values:
                _log.debug("Skipping optional parameter %r", name)
                continue

            if param.required:
                if name not in values:
                    msg = f"Missing required parameter {name}"
                    raise TypeError(msg)
                if not values[name]:
                    msg = f"Missing required value for parameter {name}"
                    raise TypeError(msg)

            _log.debug("Setting value for %s parameter to %r", name, values[name])
            param.value = values[name]

        return cls

    def get_constructed_url(self) -> str:
        if not self.parameters:
            return self.path

        url = self.path
        body_params = sorted(
            [
                (name, param)
                for name, param in self.parameters.items()
                if param.value is not None and param.is_body_parameter
            ],
            key=lambda p: (p[1].index if p[1].index is not None else float("inf")),
        )
        params = {name: param.value for name, param in self.parameters.items() if param.value is not None}
        for name, param in body_params:
            url += f"/{param.value}"
            params.pop(name)

        if params:
            url += "?" + urlencode(params, quote_via=quote_plus)

        return url


class BaseEndpointMeta(type):
    if TYPE_CHECKING:
        _handle_endpoint: Callable[[Endpoint], None]

    def __new__(mcs, name: str, bases: tuple[type, ...], attrs: dict[str, Any]) -> BaseEndpointMeta:
        cls = super().__new__(mcs, name, bases, attrs)
        if "path" not in attrs:
            return cls

        for attr in attrs.values():
            if isinstance(attr, Endpoint):
                cls._handle_endpoint(attr)
        return cls


class BaseEndpoint(metaclass=BaseEndpointMeta):
    path: str = "/"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} path={self.path}>"

    @classmethod
    def ratelimit(cls) -> tuple[int, int]:
        raise NotImplementedError("Subclasses must implement the 'ratelimit' method.")

    @classmethod
    def from_enum(cls, enum: enums.BaseEnum) -> Endpoint:
        if not isinstance(enum, enums.BaseEnum):
            msg = f"Expected 'enum' to be an instance of BaseEnum, got {type(enum).__name__!r} instead."
            raise TypeError(msg)

        attr_name = enum.value.replace("-", "_").upper()
        try:
            return getattr(cls, attr_name)
        except AttributeError as exc:
            msg = f"Could not find an endpoint matching the passed enum ({enum!r})."
            raise ValueError(msg) from exc

    @classmethod
    def _handle_endpoint(cls, endpoint: Endpoint) -> None:
        if not endpoint.path.startswith(cls.path):
            endpoint.path = f"{cls.path}{endpoint.path}"
        for name, param in endpoint.parameters.items():
            param._name = name


class Parameter:
    __slots__ = (
        "_name",
        "_value",
        "extra",
        "index",
        "is_body_parameter",
        "required",
    )

    def __init__(
        self,
        *,
        required: bool = True,
        extra: str | None = None,
        is_body_parameter: bool = False,
        index: int | None = None,
    ) -> None:
        self.required: bool = required
        self.extra: str | None = extra
        self.is_body_parameter: bool = is_body_parameter
        self.index: int | None = index

        self._name: str | None = None  # filled in with values
        self._value: Any | None = None

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self._name!r} value={self._value!r}>"

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        self._value = value


def EndpointWithAvatarParam(path: str) -> Endpoint:
    return Endpoint(
        path,
        avatar=Parameter(extra="use png or jpg"),
    )


class Base(BaseEndpoint):
    path: str = ""
    if TYPE_CHECKING:

        @classmethod
        def from_enum(cls, enum: None) -> None: ...

    BASE64 = Endpoint(
        "base64",
        encode=Parameter(extra="Text to encode into base64", required=False),
        decode=Parameter(extra="Decode base64 into text", required=False),
    )
    BINARY = Endpoint(
        "binary",
        encode=Parameter(extra="Text to encode into binary", required=False),
        decode=Parameter(extra="Decode binary into text", required=False),
    )
    BOTTOKEN = Endpoint(
        "bottoken",
    )
    CHATBOT = Endpoint(
        "chatbot",
        message=Parameter(extra="Message that will be sent to the chatbot"),
    )
    JOKE = Endpoint("joke")
    LYRICS = Endpoint("lyrics", title=Parameter(extra="Title of song to search"))
    WELCOME = Endpoint(
        "welcome/img",
        template=Parameter(index=0, extra="1 to 7", is_body_parameter=True),
        background=Parameter(index=1, is_body_parameter=True),
        type=Parameter(),
        username=Parameter(),
        avatar=Parameter(extra="use png or jpg"),
        discriminator=Parameter(required=False),
        guildName=Parameter(),
        memberCount=Parameter(),
        textcolor=Parameter(extra="red, orange, yellow, green, blue, indigo, purple, pink, black, or white"),
        font=Parameter(required=False, extra="Choose a custom font from our predetermined list, use a number from 1-10"),
    )


class Animu(BaseEndpoint):
    path: str = "animu/"
    if TYPE_CHECKING:

        @classmethod
        def from_enum(cls, enum: enums.Animu) -> Endpoint: ...

    NOM = Endpoint("nom")
    POKE = Endpoint("poke")
    CRY = Endpoint("cry")
    KISS = Endpoint("kiss")
    PAT = Endpoint("pat")
    HUG = Endpoint("hug")
    QUOTE = Endpoint("quote")


class Animal(BaseEndpoint):
    path: str = "animal/"
    if TYPE_CHECKING:

        @classmethod
        def from_enum(cls, enum: enums.Animal) -> Endpoint: ...

    FOX = Endpoint("fox")
    CAT = Endpoint("cat")
    BIRD = Endpoint("bird")
    PANDA = Endpoint("panda")
    RACCOON = Endpoint("raccoon")
    KOALA = Endpoint("koala")
    KANGAROO = Endpoint("kangaroo")
    WHALE = Endpoint("whale")
    DOG = Endpoint("dog")
    REDPANDA = Endpoint(
        "red_panda",
    )  # alias for panda


class Facts(BaseEndpoint):
    path: str = "facts/"
    if TYPE_CHECKING:

        @classmethod
        def from_enum(cls, enum: enums.Fact) -> Endpoint: ...

    CAT = Endpoint("cat")
    FOX = Endpoint("fox")
    PANDA = Endpoint("panda")
    KOALA = Endpoint("koala")
    KANGAROO = Endpoint("kangaroo")
    RACCOON = Endpoint("raccoon")
    GIRAFFE = Endpoint("giraffe")
    WHALE = Endpoint("whale")
    ELEPHANT = Endpoint("elephant")
    DOG = Endpoint("dog")
    BIRD = Endpoint("bird")


class Img(BaseEndpoint):
    path: str = "img/"
    if TYPE_CHECKING:

        @classmethod
        def from_enum(cls, enum: enums.Img) -> Endpoint: ...

    FOX = Endpoint("fox")
    CAT = Endpoint("cat")
    PANDA = Endpoint("panda")
    RED_PANDA = Endpoint("red_panda")
    PIKACHU = Endpoint("pikachu")
    RACOON = Endpoint("racoon")
    KOALA = Endpoint("koala")
    KANGAROO = Endpoint("kangaroo")
    WHALE = Endpoint("whale")
    DOG = Endpoint("dog")
    BIRD = Endpoint("bird")


class BaseCanvas(BaseEndpoint):
    path: str = "canvas/"
    if TYPE_CHECKING:

        @classmethod
        def from_enum(cls, enum: None) -> None: ...

    COLORVIEWER = Endpoint("colorviewer", hex=Parameter(extra="hex color code without the # ie. white is ffffff"))
    HEX = Endpoint("hex", rgb=Parameter(extra="separated by commas"))
    RGB = Endpoint("rgb", hex=Parameter(extra="hex color code without the # ie. white is ffffff"))


class CanvasFilter(BaseCanvas):
    path: str = f"{BaseCanvas.path}filter/"
    if TYPE_CHECKING:

        @classmethod
        def from_enum(
            cls,
            enum: enums.CanvasFilter,
        ) -> Endpoint: ...

    BLUE = EndpointWithAvatarParam("blue")
    BLURPLE = EndpointWithAvatarParam("blurple")
    BLURPLE_2 = EndpointWithAvatarParam("blurple2")
    BRIGHTNESS = Endpoint(
        "brightness",
        avatar=Parameter(extra="use png or jpg"),
        brightness=Parameter(required=False, extra="brightness value from 0-100"),
    )
    COLOR = Endpoint(
        "color",
        avatar=Parameter(extra="use png or jpg"),
        color=Parameter(extra="hex color code without the # ie. white is ffffff"),
    )
    GREEN = EndpointWithAvatarParam("green")
    GREYSCALE = EndpointWithAvatarParam("greyscale")
    INVERT = EndpointWithAvatarParam("invert")
    INVERT_GREYSCALE = EndpointWithAvatarParam("invertgreyscale")
    RED = EndpointWithAvatarParam("red")
    SEPIA = EndpointWithAvatarParam("sepia")
    THRESHOLD = Endpoint(
        "threshold",
        avatar=Parameter(extra="use png or jpg"),
        threshold=Parameter(required=False, extra="threshold value from 0-255"),
    )
    BLUR = EndpointWithAvatarParam("blur")
    PIXELATE = EndpointWithAvatarParam("pixelate")


class CanvasMisc(BaseCanvas):
    path: str = f"{BaseCanvas.path}misc/"
    if TYPE_CHECKING:

        @classmethod
        def from_enum(cls, enum: enums.CanvasCrop | enums.CanvasBorder | enums.CanvasOverlay) -> Endpoint: ...

    BISEXUAL = EndpointWithAvatarParam("bisexual")

    CIRCLE = EndpointWithAvatarParam("circle")
    HEART = EndpointWithAvatarParam("heart")
    HORNY = EndpointWithAvatarParam("horny")
    ITS_SO_STUPID = EndpointWithAvatarParam("its-so-stupid")
    LESBIAN = EndpointWithAvatarParam("lesbian")
    LGBT = EndpointWithAvatarParam("lgbt")
    LIED = Endpoint(
        "lied", avatar=Parameter(extra="use png or jpg"), username=Parameter(extra="must be less than 20 characters")
    )
    LOLICE = EndpointWithAvatarParam("lolice")
    GENSHIN_NAMECARD = Endpoint(
        "namecard",
        avatar=Parameter(extra="use png or jpg"),
        birthday=Parameter(extra="dd/mm/yyyy"),
        username=Parameter(extra="A username"),
        description=Parameter(required=False),
    )
    NO_BITCHES = Endpoint("nobitches", avatar=Parameter(extra="use png or jpg"), no=Parameter(extra="no bitches?"))
    NONBINARY = EndpointWithAvatarParam("nonbinary")
    OOGWAY = Endpoint("oogway", quote=Parameter())
    OOGWAY2 = Endpoint("oogway2", quote=Parameter())
    PANSEXUAL = EndpointWithAvatarParam("pansexual")
    SIMPCARD = EndpointWithAvatarParam("simpcard")
    SPIN = EndpointWithAvatarParam("spin")
    TONIKAWA = EndpointWithAvatarParam("tonikawa")
    TRANSGENDER = EndpointWithAvatarParam("transgender")

    TWEET = Endpoint(
        "tweet",
        displayname=Parameter(extra="Max 32 chars"),
        username=Parameter(extra="max 15 characters"),
        avatar=Parameter(extra="use png or jpg"),
        comment=Parameter(extra="max 1000 characters"),
        replies=Parameter(required=False, extra="number of replies"),
        likes=Parameter(required=False, extra="number of likes"),
        retweets=Parameter(required=False, extra="number of retweets"),
        theme=Parameter(required=False, extra="light, dim or dark"),
    )

    YOUTUBE_COMMENT = Endpoint(
        "youtube-comment",
        username=Parameter(extra="max 25 characters"),
        avatar=Parameter(extra="use png or jpg"),
        comment=Parameter(extra="max 1000 characters"),
    )


class CanvasOverlay(BaseCanvas):
    path: str = f"{BaseCanvas.path}overlay/"
    if TYPE_CHECKING:

        @classmethod
        def from_enum(cls, enum: enums.CanvasOverlay) -> Endpoint: ...

    COMRADE = EndpointWithAvatarParam("comrade")
    GAY = EndpointWithAvatarParam("gay")
    GLASS = EndpointWithAvatarParam("glass")
    JAIL = EndpointWithAvatarParam("jail")
    PASSED = EndpointWithAvatarParam("passed")
    TRIGGERED = EndpointWithAvatarParam("triggered")
    WASTED = EndpointWithAvatarParam("wasted")


class Pokemon(BaseEndpoint):
    path: str = "pokemon/"
    if TYPE_CHECKING:

        @classmethod
        def from_enum(cls, enum: None) -> None: ...

    ABILITIES = Endpoint("abilities", ability=Parameter(extra="Ability name or id of a pokemon ability"))
    ITEMS = Endpoint("items", item=Parameter(extra="Item name or id of a pokemon item"))
    MOVES = Endpoint("moves", move=Parameter(extra="Pokemon move name or id of a pokemon move"))
    POKEDEX = Endpoint("pokedex", pokemon=Parameter(extra="Pokemon name"))


class Premium(BaseEndpoint):
    path: str = "premium/"
    if TYPE_CHECKING:

        @classmethod
        def from_enum(cls, enum: None) -> None: ...

    AMONGUS = Endpoint(
        "amongus",
        avatar=Parameter(extra="use png or jpg"),
        username=Parameter(extra="maximum 30 characters"),
        custom=Parameter(required=False, extra="Custom text rather than ejecting the user"),
    )
    PETPET = EndpointWithAvatarParam("petpet")
    RANK_CARD = Endpoint(
        "rankcard",
        template=Parameter(index=0, extra="1 to 9", is_body_parameter=True),
        username=Parameter(extra="maximum 32 characters"),
        avatar=Parameter(extra="use png or jpg"),
        discriminator=Parameter(required=False),
        level=Parameter(),
        cxp=Parameter(extra="Current XP"),
        nxp=Parameter(extra="Needed XP"),
        bg=Parameter(
            required=False,
            extra="Custom background url, requires tier 2 key",
        ),
        cbg=Parameter(required=False, extra="Custom background color, requires tier 1 key"),
        ctext=Parameter(required=False, extra="Text color"),
        ccxp=Parameter(required=False, extra="Current XP color"),
        cbar=Parameter(required=False, extra="XP bar color"),
    )
    WELCOME = Endpoint(
        "welcome",
        template=Parameter(index=0, extra="1 to 7", is_body_parameter=True),
        type=Parameter(),
        username=Parameter(),
        avatar=Parameter(extra="use png or jpg"),
        discriminator=Parameter(required=False),
        guildName=Parameter(),
        memberCount=Parameter(),
        textcolor=Parameter(extra="red, orange, yellow, green, blue, indigo, purple, pink, black, or white"),
        bg=Parameter(
            required=False,
            extra="Custom background url, requires tier 2 key",
        ),
        font=Parameter(required=False, extra="Choose a custom font from our predetermined list, use a number from 1-10"),
    )


class _Endpoint(enums.BaseEnum):
    # Base
    BASE = Base
    BASE64 = Base.BASE64
    BINARY = Base.BINARY
    BOTTOKEN = Base.BOTTOKEN
    CHATBOT = Base.CHATBOT
    JOKE = Base.JOKE
    LYRICS = Base.LYRICS
    WELCOME = Base.WELCOME

    # Animu
    ANIMU = Animu
    ANIMU_NOM = Animu.NOM
    ANIMU_POKE = Animu.POKE
    ANIMU_CRY = Animu.CRY
    ANIMU_KISS = Animu.KISS
    ANIMU_PAT = Animu.PAT
    ANIMU_HUG = Animu.HUG
    ANIMU_QUOTE = Animu.QUOTE

    # Animal
    ANIMAL = Animal
    ANIMAL_FOX = Animal.FOX
    ANIMAL_CAT = Animal.CAT
    ANIMAL_BIRD = Animal.BIRD
    ANIMAL_PANDA = Animal.PANDA
    ANIMAL_RACCOON = Animal.RACCOON
    ANIMAL_KOALA = Animal.KOALA
    ANIMAL_KANGAROO = Animal.KANGAROO
    ANIMAL_WHALE = Animal.WHALE
    ANIMAL_DOG = Animal.DOG
    ANIMAL_REDPANDA = Animal.REDPANDA

    # Facts
    FACTS = Facts
    FACTS_CAT = Facts.CAT
    FACTS_FOX = Facts.FOX
    FACTS_PANDA = Facts.PANDA
    FACTS_KOALA = Facts.KOALA
    FACTS_KANGAROO = Facts.KANGAROO
    FACTS_RACCOON = Facts.RACCOON
    FACTS_GIRAFFE = Facts.GIRAFFE
    FACTS_WHALE = Facts.WHALE
    FACTS_ELEPHANT = Facts.ELEPHANT
    FACTS_DOG = Facts.DOG
    FACTS_BIRD = Facts.BIRD

    # Img
    IMG = Img
    IMG_FOX = Img.FOX
    IMG_CAT = Img.CAT
    IMG_PANDA = Img.PANDA
    IMG_RED_PANDA = Img.RED_PANDA
    IMG_PIKACHU = Img.PIKACHU
    IMG_RACOON = Img.RACOON
    IMG_KOALA = Img.KOALA
    IMG_KANGAROO = Img.KANGAROO
    IMG_WHALE = Img.WHALE
    IMG_DOG = Img.DOG
    IMG_BIRD = Img.BIRD

    # BaseCanvas
    BASECANVAS = BaseCanvas
    CANVAS_COLORVIEWER = BaseCanvas.COLORVIEWER
    CANVAS_HEX = BaseCanvas.HEX
    CANVAS_RGB = BaseCanvas.RGB

    # CanvasFilter
    CANVASFILTER = CanvasFilter
    CANVAS_FILTER_BLUE = CanvasFilter.BLUE
    CANVAS_FILTER_BLURPLE = CanvasFilter.BLURPLE
    CANVAS_FILTER_BLURPLE_2 = CanvasFilter.BLURPLE_2
    CANVAS_FILTER_BRIGHTNESS = CanvasFilter.BRIGHTNESS
    CANVAS_FILTER_COLOR = CanvasFilter.COLOR
    CANVAS_FILTER_GREEN = CanvasFilter.GREEN
    CANVAS_FILTER_GREYSCALE = CanvasFilter.GREYSCALE
    CANVAS_FILTER_INVERT = CanvasFilter.INVERT
    CANVAS_FILTER_INVERT_GREYSCALE = CanvasFilter.INVERT_GREYSCALE
    CANVAS_FILTER_RED = CanvasFilter.RED
    CANVAS_FILTER_SEPIA = CanvasFilter.SEPIA
    CANVAS_FILTER_THRESHOLD = CanvasFilter.THRESHOLD
    CANVAS_FILTER_BLUR = CanvasFilter.BLUR
    CANVAS_FILTER_PIXELATE = CanvasFilter.PIXELATE

    # CanvasMisc
    CANVASMISC = CanvasMisc
    CANVAS_MISC_BISEXUAL = CanvasMisc.BISEXUAL
    CANVAS_MISC_CIRCLE = CanvasMisc.CIRCLE
    CANVAS_MISC_HEART = CanvasMisc.HEART
    CANVAS_MISC_HORNY = CanvasMisc.HORNY
    CANVAS_MISC_ITS_SO_STUPID = CanvasMisc.ITS_SO_STUPID
    CANVAS_MISC_LESBIAN = CanvasMisc.LESBIAN
    CANVAS_MISC_LGBT = CanvasMisc.LGBT
    CANVAS_MISC_LIED = CanvasMisc.LIED
    CANVAS_MISC_LOLICE = CanvasMisc.LOLICE
    CANVAS_MISC_GENSHIN_NAMECARD = CanvasMisc.GENSHIN_NAMECARD
    CANVAS_MISC_NO_BITCHES = CanvasMisc.NO_BITCHES
    CANVAS_MISC_NONBINARY = CanvasMisc.NONBINARY
    CANVAS_MISC_OOGWAY = CanvasMisc.OOGWAY
    CANVAS_MISC_OOGWAY2 = CanvasMisc.OOGWAY2
    CANVAS_MISC_PANSEXUAL = CanvasMisc.PANSEXUAL
    CANVAS_MISC_SIMPCARD = CanvasMisc.SIMPCARD
    CANVAS_MISC_SPIN = CanvasMisc.SPIN
    CANVAS_MISC_TONIKAWA = CanvasMisc.TONIKAWA
    CANVAS_MISC_TRANSGENDER = CanvasMisc.TRANSGENDER
    CANVAS_MISC_TWEET = CanvasMisc.TWEET
    CANVAS_MISC_YOUTUBE_COMMENT = CanvasMisc.YOUTUBE_COMMENT

    # CanvasOverlay
    CANVASOVERLAY = CanvasOverlay
    CANVAS_OVERLAY_COMRADE = CanvasOverlay.COMRADE
    CANVAS_OVERLAY_GAY = CanvasOverlay.GAY
    CANVAS_OVERLAY_GLASS = CanvasOverlay.GLASS
    CANVAS_OVERLAY_JAIL = CanvasOverlay.JAIL
    CANVAS_OVERLAY_PASSED = CanvasOverlay.PASSED
    CANVAS_OVERLAY_TRIGGERED = CanvasOverlay.TRIGGERED
    CANVAS_OVERLAY_WASTED = CanvasOverlay.WASTED

    # Pokemon
    POKEMON = Pokemon
    POKEMON_ABILITIES = Pokemon.ABILITIES
    POKEMON_ITEMS = Pokemon.ITEMS
    POKEMON_MOVES = Pokemon.MOVES
    POKEMON_POKEDEX = Pokemon.POKEDEX

    # Premium
    PREMIUM = Premium
    PREMIUM_AMONGUS = Premium.AMONGUS
    PREMIUM_PETPET = Premium.PETPET
    PREMIUM_RANK_CARD = Premium.RANK_CARD
    PREMIUM_WELCOME = Premium.WELCOME
