from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, Optional

from .. import utils as _utils
from ..internals.endpoints import Premium as PremiumEndpoint
from ..models.welcome.premium import WelcomePremium
from ..models.rankcard import Rankcard

if TYPE_CHECKING:
    from ..internals.http import HTTPClient
    from ..models.image import Image

    from ..types.welcome import WelcomeTextColors
    from ..enums import WelcomeType

__all__: Tuple[str, ...] = ("Premium",)


class Premium:
    """Represents the "Premium" endpoint.

    This class is not meant to be instantiated by the user. Instead, access it through the `premium` attribute of the `Client` class.
    """

    def __init__(self, http: HTTPClient) -> None:
        self.__http: HTTPClient = http

    async def amongus(
        self,
        avatar: str,
        username: str,
        key: Optional[str] = None,
        custom_text: Optional[str] = None,
    ) -> Image:
        """Create a custom AmongUs ejecting animation.

        Parameters
        ----------
        avatar: :class:`str`
            The avatar URL.
        username: :class:`str`
            The username. Max 30 characters.
        key: Optional[:class:`str`]
            The key. At least tier 2. Required if not keys are passed to the client.
        custom_text: Optional[:class:`str`]
            The custom text to show rather than ejecting the user.
        """
        return await self.__http.request(
            PremiumEndpoint.AMONGUS,
            avatar=avatar,
            username=username,
            key=key,
            custom=custom_text,
        )

    async def petpet(self, avatar: str) -> Image:
        """Pet an user's avatar.

        Parameters
        ----------
        avatar: :class:`str`
            The avatar URL.

        Returns
        -------
        :class:`Image`
            The petpet image.
        """
        return await self.__http.request(PremiumEndpoint.PETPET, avatar=avatar)

    async def rankcard(
        self,
        obj: Optional[Rankcard] = None,
        *,
        username: Optional[str] = None,
        avatar_url: Optional[str] = None,
        discriminator: Optional[str] = None,
        level: Optional[int] = None,
        current_xp: Optional[int] = None,
        needed_xp: Optional[int] = None,
        key: Optional[str] = None,
        background_url: Optional[str] = None,
        background_color: Optional[str] = None,
        text_color: Optional[str] = None,
        current_xp_color: Optional[str] = None,
        xp_bar_color: Optional[str] = None,
    ) -> Rankcard:
        values = (
            ("username", username, True),
            ("avatar_url", avatar_url, True),
            ("discriminator", discriminator, True),
            ("level", level, True),
            ("current_xp", current_xp, True),
            ("needed_xp", needed_xp, True),
            ("key", key, False),
            ("background_url", background_url, False),
            ("background_color", background_color, False),
            ("text_color", text_color, False),
            ("current_xp_color", current_xp_color, False),
            ("xp_bar_color", xp_bar_color, False),
        )
        endpoint = PremiumEndpoint.WELCOME

        obj = _utils._handle_obj_or_args(Rankcard, obj, values).copy()
        res = await self.__http.request(endpoint, **obj.to_dict())
        new = obj.copy()
        new._image = res
        return new

    async def welcome_image(
        self,
        obj: Optional[WelcomePremium] = None,
        *,
        type: Optional[WelcomeType] = None,
        username: Optional[str] = None,
        avatar_url: Optional[str] = None,
        discriminator: Optional[str] = None,
        server_name: Optional[str] = None,
        member_count: Optional[int] = None,
        text_color: Optional[WelcomeTextColors] = None,
        key: Optional[str] = None,
        background_url: Optional[str] = None,
        font: Optional[int] = None,
    ) -> WelcomePremium:
        values = (
            ("type", type, True),
            ("background_url", background_url, True),
            ("avatar_url", avatar_url, True),
            ("username", username, True),
            ("discriminator", discriminator, True),
            ("server_name", server_name, True),
            ("member_count", member_count, True),
            ("text_color", text_color, True),
            ("key", key, False),
            ("font", font, False),
        )
        endpoint = PremiumEndpoint.WELCOME

        obj = _utils._handle_obj_or_args(WelcomePremium, obj, values).copy()
        res = await self.__http.request(endpoint, **obj.to_dict())
        new = obj.copy()
        new._image = res
        return new
