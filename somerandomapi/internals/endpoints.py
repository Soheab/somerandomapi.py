from __future__ import annotations
from email.charset import BASE64
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, ClassVar, Literal, Optional, TypeVar, Union

from urllib.parse import urlencode, quote_plus


if TYPE_CHECKING:
    from typing_extensions import Self

    from ..enums import BaseEnum

    from ..types.http import APIKeys

ValidPaths = Literal[
    "animal/",
    "animu/",
    "canvas/",
    "canvas/filter/",
    "canvas/misc/",
    "canvas/overlay/",
    "facts/",
    "img/",
    "others/",
    "pokemon",
    "premium/",
    "chatbot",
    "welcome/img/",
]


class BaseEndpoint(Enum):
    @classmethod
    def base(cls):
        raise NotImplementedError

    @classmethod
    def _from_enum(cls, enum: BaseEnum) -> Self:
        try:
            val = enum.value.replace("-", "_").upper()
            return getattr(cls, val)
        except AttributeError:
            raise AttributeError("No endpoint found for this enum") from None


class Parameter:
    __slots__ = ("required", "extra", "required_minimum_tier_key", "_name", "_value")

    def __init__(
        self, required: bool = True, extra: Optional[str] = None, required_minimum_tier_key: Optional[int] = None
    ) -> None:
        self.required: bool = required
        self.extra: Optional[str] = extra
        self.required_minimum_tier_key: Optional[int] = required_minimum_tier_key  # None means no tier required

        self._name: Optional[str] = None  # filled in with values
        self._value: Optional[Any] = None

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        self._value = value


class KeyParameter(Parameter):
    __slots__ = ("_minimum_tier",)

    def __init__(self, tier: Literal[0, 1, 2, 3], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._minimum_tier: Literal[0, 1, 2, 3] = tier
        # 0 means no tier required

    @classmethod
    def _validate_key_per_param(
        cls,
        keys: Optional[APIKeys],
        endpoint: Endpoint,
        param: Parameter,
        values: dict[str, Any],
    ) -> Optional[str]:
        param_value = values.get(param._name)  # type: ignore
        key_value = values.get("key")  # it's a key parameter so it's always called key
        # no way to check which tier the key is
        if key_value:
            return param_value

        MISSING_KEYS_ERROR = (
            f"Missing required key tier level for parameter {param._name} for {endpoint.path} endpoint. "
            f"Expected a tier {param.required_minimum_tier_key} or above key. "
            "Either pass a key when calling the method or set it in the Client constructor."
        )
        # no need to validate if not required
        if not param.required and not param_value:
            return param_value

        if not keys:
            raise TypeError(MISSING_KEYS_ERROR)

        int_tiers = [int(tier[5:]) for tier in keys.keys()]
        if param.required_minimum_tier_key not in int_tiers:
            raise TypeError(MISSING_KEYS_ERROR)

        for key, value in keys.items():
            if int(key[5:]) == param.required_minimum_tier_key:
                return param_value

        raise TypeError(MISSING_KEYS_ERROR)

    def _validate(self, endpoint: Endpoint, value: Any, keys: Optional[APIKeys]) -> str:
        MISSING_KEYS_ERROR = (
            f"Missing required key for {endpoint.path} endpoint. "
            f"Expected a tier {self._minimum_tier} or above key. "
            "Either pass a key when calling the method or set it in the Client constructor."
        )
        # no need to validate if not required
        if not self.required or self._minimum_tier == 0:
            return value

        if not keys and not value:
            raise TypeError(MISSING_KEYS_ERROR)

        # no way to check which tier the key is
        if value:
            return value

        # bail early if no keys
        if not keys:
            raise TypeError(MISSING_KEYS_ERROR)

        int_tiers = [int(tier[5:]) for tier in keys.keys()]
        if self._minimum_tier not in int_tiers:
            raise TypeError(MISSING_KEYS_ERROR)

        for key, value in keys.items():
            if int(key[5:]) >= self._minimum_tier:
                return value

        raise TypeError(MISSING_KEYS_ERROR)


class Endpoint:
    __slots__: tuple[str, ...] = ("path", "parameters")

    def __init__(
        self,
        path: str,
        **parameters: Parameter,
    ) -> None:
        self.path: str = path
        self.parameters: dict[str, Union[KeyParameter, Parameter]] = parameters
        self.__set_param_names()

    def __set_param_names(self) -> None:
        for name, param in self.parameters.items():
            param._name = name

    def _set_param_values(self, _keys: Optional[APIKeys] = None, **values: Any) -> Self:
        # new class to avoid mutating the original
        cls = self.__class__(self.path, **self.parameters)
        for name, param in cls.parameters.items():
            print("params loop", name, param, values)

            if not param.required and name not in values:
                continue
            if param.required and name not in values:
                if name == "key":
                    param.value = param._validate(self, values.get(name), _keys)  # type: ignore
                    continue

                raise TypeError(f"Missing required parameter {name}")
            elif param.required_minimum_tier_key is not None:
                key_param = cls.parameters.get("key")
                if key_param is None:
                    raise TypeError(f"Missing required parameter key for {name}")

                param.value = KeyParameter._validate_key_per_param(_keys, self, param, values)  # type: ignore
            elif isinstance(param, KeyParameter):
                param.value = param._validate(self, values.get(name), _keys)
            else:
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
    @classmethod
    def base(cls):
        return "animu/"

    FACE_PALM = Endpoint("face-palm")
    HUG = Endpoint("hug")
    PAT = Endpoint("pat")
    QUOTE = Endpoint("quote")
    WINK = Endpoint("wink")


class BaseCanvas(BaseEndpoint):
    @classmethod
    def base(cls):
        return "canvas/"


class CanvasFilter(BaseCanvas):
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


"""
class BaseAnimals(BaseEndpoint):
    BIRD = Endpoint("bird")
    CAT = Endpoint("cat")
    DOG = Endpoint("dog")
    FOX = Endpoint("fox")
    KOALA = Endpoint("koala")
    PANDA = Endpoint("panda")
"""


class Facts(BaseEndpoint):
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
    @classmethod
    def base(cls):
        return "pokemon"

    ABILITIES = Endpoint("abilities", ability=Parameter(extra="Ability name or id of a pokemon ability"))
    ITEMS = Endpoint("items", item=Parameter(extra="Item name or id of a pokemon item"))
    MOVES = Endpoint("moves", move=Parameter(extra="Pokemon move name or id of a pokemon move"))
    POKEDEX = Endpoint("pokedex", pokemon=Parameter(extra="Pokemon name"))


class Premium(BaseEndpoint):
    @classmethod
    def base(cls):
        return "premium/"

    AMONGUS = Endpoint(
        "amongus",
        avatar=Parameter(extra="use png or jpg"),
        username=Parameter(extra="maximum 30 characters"),
        key=KeyParameter(tier=1, extra="At least tier 1"),
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
        key=KeyParameter(tier=1),  # assuming tier 1 is the minimum
        bg=Parameter(required=False, extra="Custom background url, requires tier 2 key", required_minimum_tier_key=2),
        cbg=Parameter(
            required=False, extra="Custom background color, requires tier 1 key", required_minimum_tier_key=1
        ),
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
        key=KeyParameter(
            tier=2, extra="Tier 2 for this endpoint, use the free endpoint if you do not have a tier 2 key"
        ),
        bg=Parameter(required=False, extra="Custom background url, requires tier 2 key"),
        font=Parameter(
            required=False, extra="Choose a custom font from our predetermined list, use a number from 1-10"
        ),
    )


class Chatbot(BaseEndpoint):
    @classmethod
    def base(cls):
        return "chatbot"

    CHATBOT = Endpoint(
        "chatbot",
        message=Parameter(extra="Message that will be sent to the chatbot"),
        key=KeyParameter(tier=1),  # assuming tier 1 is the minimum
    )


class WelcomeImages(BaseEndpoint):
    @classmethod
    def base(cls):
        return "welcome/img/"

    WELCOME = Endpoint(
        "welcome",
        type=Parameter(),
        username=Parameter(),
        avatar=Parameter(extra="use png or jpg"),
        discriminator=Parameter(),
        guildName=Parameter(),
        memberCount=Parameter(),
        textcolor=Parameter(extra="red, orange, yellow, green, blue, indigo, purple, pink, black, or white"),
        key=KeyParameter(tier=0, extra="requires a key but does not need to be active"),
        font=Parameter(
            required=False, extra="Choose a custom font from our predetermined list, use a number from 1-10"
        ),
    )
