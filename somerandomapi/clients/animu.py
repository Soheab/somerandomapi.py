from __future__ import annotations

from typing import TYPE_CHECKING

from ..internals.endpoints import Animu as AnimuEndpoint
from ..models.animu_quote import AnimuQuote


if TYPE_CHECKING:
    from ..internals.http import HTTPClient


__all__ = ("AnimuClient",)


class AnimuClient:
    """Represents the "Animu" endpoint.

    This class is not meant to be instantiated by the user. Instead, access it through the :attr:`~somerandomapi.Client.animu` attribute of the :class:`~somerandomapi.Client` class.
    """

    __slots__ = ("__http",)

    def __init__(self, http) -> None:
        self.__http: HTTPClient = http

    async def face_palm(self) -> str:
        """Get a random animu face palm image.

        Returns
        -------
        :class:`str`
            The image URL.
        """
        response = await self.__http.request(AnimuEndpoint.FACE_PALM)
        return response["link"]

    async def facepalm(self) -> str:
        """Alias for :meth:`face_palm`."""
        return await self.face_palm()

    async def hug(self) -> str:
        """Get a random animu hug image.

        Returns
        -------
        :class:`str`
            The image URL.
        """
        response = await self.__http.request(AnimuEndpoint.HUG)
        return response["link"]

    async def pat(self) -> str:
        """Get a random animu pat image.

        Returns
        -------
        :class:`str`
            The image URL.
        """
        response = await self.__http.request(AnimuEndpoint.PAT)
        return response["link"]

    async def wink(self) -> str:
        """Get a random animu wink image.

        Returns
        -------
        :class:`str`
            The image URL.
        """
        response = await self.__http.request(AnimuEndpoint.WINK)
        return response["link"]

    async def quote(self) -> AnimuQuote:
        """Get a random animu quote.

        Returns
        -------
        :class:`AnimuQuote`
            Object representing the random quote.
            The quote can be accessed through the ``sentance`` attribute.
        """
        response = await self.__http.request(AnimuEndpoint.QUOTE)
        return AnimuQuote(**response)
