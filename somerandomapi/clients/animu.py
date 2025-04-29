from __future__ import annotations
from typing import TYPE_CHECKING

from ..internals.endpoints import Animu as AnimuEndpoint, _Endpoint
from .abc import BaseClient
from .. import utils
from ..enums import Animu as AnimuEnum
from ..models.animu import AnimuQuote

if TYPE_CHECKING:
    from ..types.animu import ValidAnimu


__all__ = ("AnimuClient",)


class AnimuClient(BaseClient):
    """Represents the "Animu" endpoint.

    This class is not meant to be instantiated by the user. Instead, access it through the :attr:`~somerandomapi.Client.animu` attribute of the :class:`~somerandomapi.Client` class.
    """

    #    @BaseClient._contextmanager
    async def get(self, animu_type: ValidAnimu | AnimuEnum, /) -> str:
        """Get a random animu image.

        Parameters
        ----------
        animu_type: :class:`~somerandomapi.enums.Animu`
            The type of animu to get.

        Returns
        -------
        :class:`str`
            The URL of the random animu image.
        """
        _animu_type = utils._try_enum(AnimuEnum, animu_type)
        valid_animu = list(map(str, list(AnimuEnum)))
        if not _animu_type:
            not_valid_error: str = (
                f"'animu_type' must be a 'somerandomapi.Animu' or one of {', '.join(valid_animu)}, not {animu_type!r}."
            )
            raise ValueError(not_valid_error)

        res = await self._http.request(AnimuEndpoint.from_enum(_animu_type))
        return res["link"]

    async def random_quote(self) -> AnimuQuote:
        """Get a random animu quote.

        Returns
        -------
        :class:`AnimuQuote`
            Object representing the random quote.
            The quote can be accessed through the ``quote`` attribute.
        """
        response = await self._http.request(_Endpoint.ANIMU_QUOTE)
        return AnimuQuote(**response)

    @BaseClient._proxy_to(get, pre_args=((0, AnimuEnum.HUG),))
    async def hug(self) -> str: ...

    @BaseClient._proxy_to(get, pre_args=((0, AnimuEnum.PAT),))
    async def pat(self) -> str: ...

    @BaseClient._proxy_to(get, pre_args=((0, AnimuEnum.NOM),))
    async def nom(self) -> str: ...

    @BaseClient._proxy_to(get, pre_args=((0, AnimuEnum.CRY),))
    async def cry(self) -> str: ...

    @BaseClient._proxy_to(get, pre_args=((0, AnimuEnum.KISS),))
    async def kiss(self) -> str: ...

    @BaseClient._proxy_to(get, pre_args=((0, AnimuEnum.POKE),))
    async def poke(self) -> str: ...
