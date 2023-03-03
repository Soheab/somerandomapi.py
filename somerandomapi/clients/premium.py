from __future__ import annotations

from typing import Literal, Optional, TYPE_CHECKING

from .. import utils as _utils
from ..internals.endpoints import Premium as PremiumEndpoint
from ..models.rankcard import Rankcard
from ..models.welcome.premium import WelcomePremium


if TYPE_CHECKING:
    from ..enums import WelcomeTextColor, WelcomeType
    from ..internals.http import HTTPClient
    from ..models.image import Image

__all__ = ("PremiumClient",)


class PremiumClient:
    """Represents the "Premium" endpoint.

    This class is not meant to be instantiated by the user. Instead, access it through the :attr:`~somerandomapi.Client.premium` attribute of the :class:`~somerandomapi.Client` class.
    """

    __slots__ = ("__http",)

    def __init__(self, http) -> None:
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

        Returns
        -------
        :class:`Image`
            Object representing the generated image.
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
        """Generate a custom rankcard.

        Parameters
        ----------
        obj: Optional[:class:`Rankcard`]
            The object to use. If not passed, the other parameters will be used and a new object will be created.
        username: Optional[:class:`str`]
            The username. Max 32 characters. Required if `obj` is not passed.
        avatar_url: Optional[:class:`str`]
            The avatar URL. Required if `obj` is not passed.
        discriminator: Optional[:class:`str`]
            The discriminator. Required if `obj` is not passed.
        level: Optional[:class:`int`]
            The level. Required if `obj` is not passed.
        current_xp: Optional[:class:`int`]
            The current XP. Required if `obj` is not passed.
        needed_xp: Optional[:class:`int`]
            The needed XP. Required if `obj` is not passed.
        key: Optional[:class:`str`]
            The key. At least tier 2. Required if no key is passed to the client.
        background_url: Optional[:class:`str`]
            The background URL. Cannot be used with `background_color`.
        background_color: Optional[:class:`str`]
            The background color hex. Cannot be used with `background_url`.
        text_color: Optional[:class:`str`]
            The text color hex.
        current_xp_color: Optional[:class:`str`]
            The current XP color hex.
        xp_bar_color: Optional[:class:`str`]
            The XP bar color hex.
        """
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
        new._set_image(res)
        return new

    async def welcome_image(
        self,
        obj: Optional[WelcomePremium] = None,
        *,
        template: Optional[Literal[1, 2, 3, 4, 5, 6, 7, 8]] = None,
        type: Optional[WelcomeType] = None,
        username: Optional[str] = None,
        avatar_url: Optional[str] = None,
        discriminator: Optional[str] = None,
        server_name: Optional[str] = None,
        member_count: Optional[int] = None,
        text_color: Optional[WelcomeTextColor] = None,
        key: Optional[str] = None,
        background_url: Optional[str] = None,
        font: Optional[int] = None,
    ) -> WelcomePremium:
        """Generate a custom welcome image.

        Parameters
        ----------
        obj: Optional[:class:`WelcomePremium`]
            The object to use. If not passed, the other parameters will be used and a new object will be created.
        template: Optional[Literal[1, 2, 3, 4, 5, 6, 7, 8]`
            The template to use. Must be a number between 1 and 7. Required if `obj` is not passed.
        type: Optional[:class:`.WelcomeType`]
            The type of welcome card. Required if `obj` is not passed.
        username: Optional[:class:`str`]
            The username. Required if `obj` is not passed.
        avatar_url: Optional[:class:`str`]
            The avatar URL. Required if `obj` is not passed.
        discriminator: Optional[:class:`str`]
            The discriminator. Required if `obj` is not passed.
        server_name: Optional[:class:`str`]
            The server name. Required if `obj` is not passed.
        member_count: Optional[:class:`int`]
            The member count. Required if `obj` is not passed.
        text_color: Optional[:class:`.WelcomeTextColor`]
            The text color. Required if `obj` is not passed.
        key: Optional[:class:`str`]
            The key. At least tier 2. Required if no key is passed to the client.
        font: Optional[:class:`int`]
            The font to use. Must be a number between 1 and 10.

        """
        values = (
            ("template", template, True),
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
        res = await self.__http._welcome_card(endpoint, obj)
        new = obj.copy()
        new._set_image(res)
        return new
