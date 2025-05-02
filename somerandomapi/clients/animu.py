from __future__ import annotations

from typing import TYPE_CHECKING

from .. import utils as _utils
from ..enums import Animu as AnimuEnum
from ..internals.endpoints import (
    Animu as AnimuEndpoint,
    _Endpoint,
)
from ..models.animu import AnimuQuote
from .abc import BaseClient

if TYPE_CHECKING:
    from ..types.animu import ValidAnimu


__all__ = ("AnimuClient",)


class AnimuClient(BaseClient):
    """Represents the "Animu" endpoint.

    This class is not meant to be instantiated you. Instead, access it through the :attr:`~somerandomapi.Client.animu`
    attribute of the :class:`~somerandomapi.Client` class.
    """

    async def get(self, animu_type: ValidAnimu | AnimuEnum, /) -> str:
        """Get a random animu image.

        Parameters
        ----------
        animu_type: Union[:class:`~somerandomapi.Animu`, :class:`str`]
            The type of animu image to get. Can be one of the :class:`~somerandomapi.Animu` enum
            values or a string representing the action.

        Returns
        -------
        :class:`str`
            The URL of the random animu image.
        """
        res = await self._http.request(AnimuEndpoint.from_enum(_utils._str_or_enum(animu_type, AnimuEnum)))
        return res["link"]

    async def random_quote(self) -> AnimuQuote:
        """Get a random quote from a random animu.

        Returns
        -------
        :class:`~somerandomapi.AnimuQuote`
            Object containing the quote and other information.
            Use the ``.quote`` attribute to get the quote string.
        """
        response = await self._http.request(_Endpoint.ANIMU_QUOTE)
        return AnimuQuote(**response)

    @BaseClient._proxy_to(get, pre_args=((0, AnimuEnum.HUG),))
    async def hug(self) -> str:
        """Shortcut for :meth:`~AnimuClient.get` with :attr:`.Animu.HUG`."""
        ...

    @BaseClient._proxy_to(get, pre_args=((0, AnimuEnum.PAT),))
    async def pat(self) -> str:
        """Shortcut for :meth:`~AnimuClient.get` with :attr:`.Animu.PAT`."""
        ...

    @BaseClient._proxy_to(get, pre_args=((0, AnimuEnum.NOM),))
    async def nom(self) -> str:
        """Shortcut for :meth:`~AnimuClient.get` with :attr:`.Animu.NOM`."""
        ...

    @BaseClient._proxy_to(get, pre_args=((0, AnimuEnum.CRY),))
    async def cry(self) -> str:
        """Shortcut for :meth:`~AnimuClient.get` with :attr:`.Animu.CRY`."""
        ...

    @BaseClient._proxy_to(get, pre_args=((0, AnimuEnum.KISS),))
    async def kiss(self) -> str:
        """Shortcut for :meth:`~AnimuClient.get` with :attr:`.Animu.KISS`."""
        ...

    @BaseClient._proxy_to(get, pre_args=((0, AnimuEnum.POKE),))
    async def poke(self) -> str:
        """Shortcut for :meth:`~AnimuClient.get` with :attr:`.Animu.POKE`."""
        ...
