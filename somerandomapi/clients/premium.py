from __future__ import annotations

from typing import TYPE_CHECKING, Literal, overload

from somerandomapi.clients.animal import BaseClient

from .. import utils as _utils
from ..internals.endpoints import Premium as PremiumEndpoint
from ..models.rankcard import Rankcard
from ..models.welcome.premium import WelcomePremium

if TYPE_CHECKING:
    from ..enums import WelcomeTextColor, WelcomeType
    from ..models.image import Image

__all__ = ("PremiumClient",)


class PremiumClient(BaseClient):
    """Represents the "Premium" endpoint.

    This class is not meant to be instantiated by the user. Instead, access it through the
    :attr:`~somerandomapi.Client.premium` attribute of the :class:`~somerandomapi.Client` class.
    """

    async def amongus(
        self,
        avatar: str,
        username: str,
        key: str | None = None,
        custom_text: str | None = None,
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
        return await self._http.request(
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
        return await self._http.request(PremiumEndpoint.PETPET, avatar=avatar)

    @overload
    async def rankcard(
        self,
        obj: Rankcard,
    ) -> Rankcard: ...

    @overload
    async def rankcard(
        self,
        *,
        template: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9],
        username: str,
        avatar_url: str,
        level: int,
        current_xp: int,
        needed_xp: int,
        discriminator: int | None = ...,
        background_url: str | None = ...,
        background_color: str | None = ...,
        text_color: str | None = ...,
        current_xp_color: str | None = ...,
        xp_bar_color: str | None = ...,
        username_color: str | None = ...,
    ) -> Rankcard: ...

    async def rankcard(
        self,
        obj: Rankcard = _utils.NOVALUE,
        *,
        template: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9] = _utils.NOVALUE,
        username: str = _utils.NOVALUE,
        avatar_url: str = _utils.NOVALUE,
        level: int = _utils.NOVALUE,
        current_xp: int = _utils.NOVALUE,
        needed_xp: int = _utils.NOVALUE,
        discriminator: int | None = _utils.NOVALUE,
        background_url: str | None = _utils.NOVALUE,
        background_color: str | None = _utils.NOVALUE,
        text_color: str | None = _utils.NOVALUE,
        current_xp_color: str | None = _utils.NOVALUE,
        xp_bar_color: str | None = _utils.NOVALUE,
        username_color: str | None = _utils.NOVALUE,
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
        discriminator: Optional[:class:`int`]
            The discriminator to use. Required if ``obj`` is not passed.
        level: Optional[:class:`int`]
            The level. Required if `obj` is not passed.
        current_xp: Optional[:class:`int`]
            The current XP. Required if `obj` is not passed.
        needed_xp: Optional[:class:`int`]
            The needed XP. Required if `obj` is not passed.
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
        username_color: Optional[:class:`str`]
            The username color hex.
        """
        values = (
            ("template", template, True),
            ("username", username, True),
            ("avatar_url", avatar_url, True),
            ("level", level, True),
            ("current_xp", current_xp, True),
            ("needed_xp", needed_xp, True),
            ("discriminator", discriminator, False),
            ("background_url", background_url, False),
            ("background_color", background_color, False),
            ("text_color", text_color, False),
            ("current_xp_color", current_xp_color, False),
            ("xp_bar_color", xp_bar_color, False),
            ("username_color", username_color, False),
        )
        endpoint = PremiumEndpoint.RANK_CARD

        obj = _utils._handle_obj_or_args(Rankcard, obj, values).copy()
        res = await self._http.request(endpoint, **obj.to_dict())
        new = obj.copy()
        new._set_image(res)
        return new

    @overload
    async def welcome_image(
        self,
        obj: WelcomePremium,
    ) -> WelcomePremium: ...

    @overload
    async def welcome_image(
        self,
        *,
        template: Literal[1, 2, 3, 4, 5, 6, 7],
        type: WelcomeType,
        username: str,
        avatar_url: str,
        discriminator: int,
        server_name: str,
        member_count: int,
        text_color: WelcomeTextColor,
        background_url: str | None = _utils.NOVALUE,
        font: Literal[0, 1, 2, 3, 4, 5, 6, 7] | None = _utils.NOVALUE,
    ) -> WelcomePremium: ...

    async def welcome_image(
        self,
        obj: WelcomePremium = _utils.NOVALUE,
        *,
        template: Literal[1, 2, 3, 4, 5, 6, 7] = _utils.NOVALUE,
        type: WelcomeType = _utils.NOVALUE,  # noqa: A002
        username: str = _utils.NOVALUE,
        avatar_url: str = _utils.NOVALUE,
        discriminator: int = _utils.NOVALUE,
        server_name: str = _utils.NOVALUE,
        member_count: int = _utils.NOVALUE,
        text_color: WelcomeTextColor = _utils.NOVALUE,
        background_url: str | None = _utils.NOVALUE,
        font: Literal[0, 1, 2, 3, 4, 5, 6, 7] | None = _utils.NOVALUE,
    ) -> WelcomePremium:
        """Generate a custom welcome image.

        Parameters
        ----------
        obj: Optional[:class:`WelcomePremium`]
            The object to use. If not passed, the other parameters will be used and a new object will be created.
        template: Optional[Literal[1, 2, 3, 4, 5, 6, 7]`
            The template to use. Must be a number between 1 and 7. Required if `obj` is not passed.
        type: Optional[:class:`.WelcomeType`]
            The type of welcome card. Required if `obj` is not passed.
        username: Optional[:class:`str`]
            The username. Required if `obj` is not passed.
        avatar_url: Optional[:class:`str`]
            The avatar URL. Required if `obj` is not passed.
        discriminator: Optional[:class:`int`]
            The discriminator to use.
        server_name: Optional[:class:`str`]
            The server name. Required if `obj` is not passed.
        member_count: Optional[:class:`int`]
            The member count. Required if `obj` is not passed.
        text_color: Optional[:class:`.WelcomeTextColor`]
            The text color. Required if `obj` is not passed.
        background_url: Optional[:class:`str`]
            The background URL.
        font: Optional[:class:`int`]
            The font from a predefined list. Choose a number between 0 and 7.

            .. versionchanged:: 0.1.0
                This takes a range of 0-7 now instead of 0-8.

        """
        values = (
            ("template", template, True),
            ("type", type, True),
            ("background_url", background_url, True),
            ("avatar_url", avatar_url, True),
            ("username", username, True),
            ("server_name", server_name, True),
            ("member_count", member_count, True),
            ("text_color", text_color, True),
            ("discriminator", discriminator, False),
            ("font", font, False),
        )
        endpoint = PremiumEndpoint.WELCOME

        obj = _utils._handle_obj_or_args(WelcomePremium, obj, values).copy()
        res = await self._http.request(endpoint, **obj.to_dict())
        new = obj.copy()
        new._set_image(res)
        return new
