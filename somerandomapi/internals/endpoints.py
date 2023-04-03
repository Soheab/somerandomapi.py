from __future__ import annotations

from typing import Any, Callable, Literal, Optional, TYPE_CHECKING
from urllib.parse import quote_plus, urlencode

from .. import enums


if TYPE_CHECKING:
    from typing_extensions import Self

    from ..internals.http import APIKey
    from ..types.http import ValidPaths

_TIER_ERROR = (
    "Missing required key tier level for {path} endpoint. "
    "Expected a tier {tier} or above key. "
    "Either pass such key when calling the method or set it in the Client constructor."
)
_TIER_ERROR_PARAMETER = (
    "Missing required key tier level for {param} param for the {path} endpoint. "
    "Expected a tier {tier} or above key. "
    "Either pass such key when calling the method, set it in the Client constructor or don't pass the parameter."
)


class BaseEndpoint(enums.BaseEnum):
    @classmethod
    def ratelimit(cls) -> tuple[int, int]:
        raise NotImplementedError

    @classmethod
    def base(cls) -> ValidPaths:
        raise NotImplementedError

    @classmethod
    def from_enum(cls, enum: enums.BaseEnum) -> Self:
        try:
            val = enum.value.replace("-", "_").upper()
            return getattr(cls, val)
        except AttributeError:
            raise AttributeError("No endpoint found for this enum") from None


class Parameter:
    __slots__ = ("required", "extra", "key_tier", "is_key_parameter", "_key_value", "_name", "_value")

    def __init__(
        self,
        required: bool = True,
        extra: Optional[str] = None,
        key_tier: Optional[int] = None,
        is_key_parameter: bool = False,
    ) -> None:
        self.required: bool = required
        self.extra: Optional[str] = extra
        self.key_tier: Optional[int] = key_tier  # None means no tier required
        self.is_key_parameter: bool = is_key_parameter

        self._name: Optional[str] = None  # filled in with values
        self._value: Optional[Any] = None

        self._key_value: Optional[tuple[int, str]] = None

    def _validate_key(
        self,
        client_key: Optional[APIKey],
        endpoint: Endpoint,
        key_value: Optional[str],
    ) -> None:
        if not client_key and not key_value:
            raise TypeError(
                f"Missing required key for {endpoint.path} endpoint. "
                "Either pass a key when calling the method or set it in the Client constructor."
            )

        # can't check tier if passed as a parameter
        if not client_key and key_value:
            self._key_value = (0, key_value)
            self.value = key_value
            return

        if client_key:
            if self.key_tier:
                # check if client_key.tier is not 0 and is not less than self.key_tier
                if client_key.tier and client_key.tier < self.key_tier:
                    raise TypeError(_TIER_ERROR.format(path=endpoint.path, tier=self.key_tier))
            self._key_value = (client_key.tier, client_key.value)
            self.value = client_key.value
            return

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        self._value = value


class Endpoint:
    __slots__: tuple[str, ...] = ("path", "parameters")

    def __init__(
        self,
        path: str,
        **parameters: Parameter,
    ) -> None:
        self.path: str = path
        self.parameters: dict[str, Parameter] = parameters
        self.__set_param_names()

    def __set_param_names(self) -> None:
        for name, param in self.parameters.items():
            param._name = name

    def _set_param_values(self, _key: Optional[APIKey] = None, **values: Any) -> Self:
        # new class to avoid mutating the original
        cls = self.__class__(self.path, **self.parameters)
        params = cls.parameters.copy()
        if key_param := params.get("key"):
            key_param._validate_key(_key, cls, values.get("key"))

        for name, param in params.items():
            if param.is_key_parameter:
                continue

            if not param.required and name not in values:
                continue

            if param.required:
                if name not in values:
                    raise TypeError(f"Missing required parameter {name}")
                elif not values[name]:
                    raise TypeError(f"Missing required value for parameter {name}")

            if param.key_tier:
                if key_param and key_param._key_value:
                    tier = key_param._key_value[0]
                    if tier and tier < param.key_tier:
                        raise TypeError(_TIER_ERROR_PARAMETER.format(param=name, path=cls.path, tier=param.key_tier))

            param.value = values[name]

        return cls

    def get_constructed_url(self, enum: BaseEndpoint) -> str:
        url = f"{enum.base()}{self.path}"
        if self.parameters:
            params = {name: param.value for name, param in self.parameters.items() if param.value is not None}
            url += "?" + urlencode(params, quote_via=quote_plus)

        return url


EndpointWithAvatarParam: Callable[[str], Endpoint] = lambda path: Endpoint(
    path,
    avatar=Parameter(extra="use png or jpg"),
)


class Animu(BaseEndpoint):
    if TYPE_CHECKING:
        @classmethod
        def from_enum(cls, enum: Literal[None]) -> None:
            ...

    @classmethod
    def base(cls):
        return "animu/"

    FACE_PALM = Endpoint("face-palm")
    HUG = Endpoint("hug")
    PAT = Endpoint("pat")
    QUOTE = Endpoint("quote")
    WINK = Endpoint("wink")


class BaseCanvas(BaseEndpoint):
    if TYPE_CHECKING:
        @classmethod
        def from_enum(cls, enum: Literal[None]) -> None:
            ...

    @classmethod
    def base(cls):
        return "canvas/"


class CanvasFilter(BaseCanvas):
    if TYPE_CHECKING:
        @classmethod
        def from_enum(
            cls,
            enum: Literal[
                enums.CanvasFilter.BLURPLE,
                enums.CanvasFilter.BLURPLE_2,
                enums.CanvasFilter.BRIGHTNESS,
                enums.CanvasFilter.COLOR,
                enums.CanvasFilter.BLUE,
                enums.CanvasFilter.GREEN,
                enums.CanvasFilter.RED,
                enums.CanvasFilter.SEPIA,
                enums.CanvasFilter.GREYSCALE,
                enums.CanvasFilter.INVERT,
                enums.CanvasFilter.INVERT_GREYSCALE,
                enums.CanvasFilter.THRESHOLD,
        ]) -> Self:
            ...

    @classmethod
    def base(cls):
        return super().base() + "filter/"

    BLUE = EndpointWithAvatarParam("blue")
    BLURPLE = EndpointWithAvatarParam("blurple")
    BLURPLE_2 = EndpointWithAvatarParam("blurple2")
    BRIGHTNESS = Endpoint(
        "brightness",
        avatar=Parameter(extra="use png or jpg"),
        brightness=Parameter(required=False, extra="brightness value from 0-255"),
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
        threshold=Parameter(required=False, extra="threshold value from 1-255"),
    )


class CanvasMisc(BaseCanvas):
    if TYPE_CHECKING:
        @classmethod
        def from_enum(cls, enum: Literal[enums.CanvasFilter.BLUR, enums.CanvasFilter.JPG, enums.CanvasFilter.PIXELATE]) -> Self:
            ...

    @classmethod
    def base(cls):
        return super().base() + "misc/"

    BISEXUAL_BORDER = EndpointWithAvatarParam("bisexual")
    BLUR = EndpointWithAvatarParam("blur")
    CIRCLE_CROP = EndpointWithAvatarParam("circle")
    COLOR_VIEWER = Endpoint("colorviewer", hex=Parameter(extra="hex value without the #"))
    HEART_CROP = EndpointWithAvatarParam("heart")
    HEX = Endpoint("hex", rgb=Parameter(extra="rgb value splitted by ,"))
    HORNY = EndpointWithAvatarParam("horny")
    ITS_SO_STUPID = EndpointWithAvatarParam("its-so-stupid")
    JPG = EndpointWithAvatarParam("jpg")
    LESBIAN_BORDER = EndpointWithAvatarParam("lesbian")
    LGBT_BORDER = EndpointWithAvatarParam("lgbt")
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
    NO_BITCHES = Endpoint("nobitches", no=Parameter(extra="no bitches?"))
    NONBINARY_BORDER = EndpointWithAvatarParam("nonbinary")
    OOGWAY = Endpoint("oogway", quote=Parameter())
    OOGWAY2 = Endpoint("oogway2", quote=Parameter())
    PANSEXUAL_BORDER = EndpointWithAvatarParam("pansexual")
    PIXELATE = EndpointWithAvatarParam("pixelate")
    RGB = Endpoint("rgb", hex=Parameter(extra="hex value without the #"))
    SIMPCARD = EndpointWithAvatarParam("simpcard")
    SPIN = EndpointWithAvatarParam("spin")
    TONIKAWA = EndpointWithAvatarParam("tonikawa")
    TRANSGENDER_BORDER = EndpointWithAvatarParam("transgender")

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
    if TYPE_CHECKING:
        @classmethod
        def from_enum(cls, enum: enums.CanvasOverlay) -> Self:
            ...

    @classmethod
    def base(cls):
        return super().base() + "overlay/"

    COMRADE = EndpointWithAvatarParam("comrade")
    GAY = EndpointWithAvatarParam("gay")
    GLASS = EndpointWithAvatarParam("glass")
    JAIL = EndpointWithAvatarParam("jail")
    PASSED = EndpointWithAvatarParam("passed")
    TRIGGERED = EndpointWithAvatarParam("triggered")
    WASTED = EndpointWithAvatarParam("wasted")


class Facts(BaseEndpoint):
    if TYPE_CHECKING:
        @classmethod
        def from_enum(cls, enum: enums.FactAnimal) -> Self:
            ...

    @classmethod
    def base(cls):
        return "facts/"

    # can't subclass BaseAnimals
    BIRD = Endpoint("bird")
    CAT = Endpoint("cat")
    DOG = Endpoint("dog")
    FOX = Endpoint("fox")
    KOALA = Endpoint("koala")
    PANDA = Endpoint("panda")


class Animal(BaseEndpoint):
    if TYPE_CHECKING:
        @classmethod
        def from_enum(cls, enum: enums.Animal) -> Self:
            ...

    @classmethod
    def base(cls):
        return "animal/"

    # can't subclass BaseAnimals
    BIRD = Endpoint("bird")
    CAT = Endpoint("cat")
    DOG = Endpoint("dog")
    FOX = Endpoint("fox")
    KOALA = Endpoint("koala")
    PANDA = Endpoint("panda")

    KANGAROO = Endpoint("kangaroo")
    RACCOON = Endpoint("raccoon")
    RED_PANDA = Endpoint("red_panda")


class Img(BaseEndpoint):
    if TYPE_CHECKING:
        @classmethod
        def from_enum(cls, enum: enums.ImgAnimal) -> Self:
            ...

    @classmethod
    def base(cls):
        return "img/"

    # can't subclass BaseAnimals
    BIRD = Endpoint("bird")
    CAT = Endpoint("cat")
    DOG = Endpoint("dog")
    FOX = Endpoint("fox")
    KOALA = Endpoint("koala")
    PANDA = Endpoint("panda")

    PIKACHU = Endpoint("pikachu")
    WHALE = Endpoint("whale")


class Others(BaseEndpoint):
    if TYPE_CHECKING:
        @classmethod
        def from_enum(cls, enum: Literal[None]) -> None:
            ...

    @classmethod
    def base(cls):
        return "others/"

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
    BOTTOKEN = Endpoint("bottoken", id=Parameter(extra="ID of the discord bot"))
    DICTIONARY = Endpoint("dictionary", word=Parameter(extra="Word to lookup"))
    JOKE = Endpoint("joke")
    LYRICS = Endpoint("lyrics", title=Parameter(extra="Title of song to search"))


class Pokemon(BaseEndpoint):
    if TYPE_CHECKING:
        @classmethod
        def from_enum(cls, enum: Literal[None]) -> None:
            ...

    @classmethod
    def base(cls):
        return "pokemon/"

    ABILITIES = Endpoint("abilities", ability=Parameter(extra="Ability name or id of a pokemon ability"))
    ITEMS = Endpoint("items", item=Parameter(extra="Item name or id of a pokemon item"))
    MOVES = Endpoint("moves", move=Parameter(extra="Pokemon move name or id of a pokemon move"))
    POKEDEX = Endpoint("pokedex", pokemon=Parameter(extra="Pokemon name"))


class Premium(BaseEndpoint):
    if TYPE_CHECKING:
        @classmethod
        def from_enum(cls, enum: Literal[None]) -> None:
            ...

    @classmethod
    def base(cls):
        return "premium/"

    AMONGUS = Endpoint(
        "amongus",
        avatar=Parameter(extra="use png or jpg"),
        username=Parameter(extra="maximum 30 characters"),
        key=Parameter(key_tier=1, is_key_parameter=True, extra="At least tier 1"),
        cusotom=Parameter(required=False, extra="Custom text rather than ejecting the user"),
    )
    PETPET = EndpointWithAvatarParam("petpet")
    RANK_CARD = Endpoint(
        "rankcard",
        username=Parameter(extra="maximum 32 characters"),
        avatar=Parameter(extra="use png or jpg"),
        discriminator=Parameter(),
        level=Parameter(),
        cxp=Parameter(extra="Current XP"),
        nxp=Parameter(extra="Needed XP"),
        key=Parameter(key_tier=1, is_key_parameter=True),  # assuming tier 1 is the minimum
        bg=Parameter(required=False, extra="Custom background url, requires tier 2 key", key_tier=2),
        cbg=Parameter(required=False, extra="Custom background color, requires tier 1 key", key_tier=1),
        ctext=Parameter(required=False, extra="Text color"),
        ccxp=Parameter(required=False, extra="Current XP color"),
        cbar=Parameter(required=False, extra="XP bar color"),
    )
    WELCOME = Endpoint(
        "welcome",
        type=Parameter(),
        username=Parameter(),
        avatar=Parameter(extra="use png or jpg"),
        discriminator=Parameter(),
        guildName=Parameter(),
        memberCount=Parameter(),
        textcolor=Parameter(extra="red, orange, yellow, green, blue, indigo, purple, pink, black, or white"),
        key=Parameter(
            key_tier=2,
            is_key_parameter=True,
            extra="Tier 2 for this endpoint, use the free endpoint if you do not have a tier 2 key",
        ),
        bg=Parameter(required=False, extra="Custom background url, requires tier 2 key", key_tier=2),
        font=Parameter(
            required=False, extra="Choose a custom font from our predetermined list, use a number from 1-10"
        ),
    )


class Chatbot(BaseEndpoint):
    if TYPE_CHECKING:
        @classmethod
        def from_enum(cls, enum: Literal[None]) -> None:
            ...

    @classmethod
    def base(cls):
        return ""

    CHATBOT = Endpoint(
        "chatbot",
        message=Parameter(extra="Message that will be sent to the chatbot"),
        key=Parameter(
            key_tier=1,
            is_key_parameter=True,
        ),  # assuming tier 1 is the minimum
    )


class WelcomeImages(BaseEndpoint):
    if TYPE_CHECKING:
        @classmethod
        def from_enum(cls, enum: Literal[None]) -> None:
            ...

    @classmethod
    def base(cls):
        return "welcome/img/"

    WELCOME = Endpoint(
        "",
        type=Parameter(),
        username=Parameter(),
        avatar=Parameter(extra="use png or jpg"),
        discriminator=Parameter(),
        guildName=Parameter(),
        memberCount=Parameter(),
        textcolor=Parameter(extra="red, orange, yellow, green, blue, indigo, purple, pink, black, or white"),
        key=Parameter(key_tier=0, is_key_parameter=True, extra="requires a key but does not need to be active"),
        font=Parameter(
            required=False, extra="Choose a custom font from our predetermined list, use a number from 1-10"
        ),
    )
