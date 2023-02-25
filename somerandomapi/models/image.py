from __future__ import annotations

from io import BytesIO
from typing import Literal, Optional, overload, TYPE_CHECKING, Union


if TYPE_CHECKING:
    from io import BufferedIOBase
    from os import PathLike
    from typing import Any, Protocol

    from typing_extensions import Self

    from ..internals.http import HTTPClient

    class FileLike(Protocol):
        def __call__(
            self,
            fp: Union[str, bytes, PathLike[Any], BufferedIOBase],
            filename: Optional[str] = None,
            **kwargs: Any,
        ) -> Self:
            ...


__all__ = ("Image",)


class Image:
    """Represents a class for all image endpoints.

    attributes
    ----------
    url: :class:`str`
        The image URL.
    """

    __slots__ = ("_url", "_http")

    _url: str
    _http: HTTPClient

    @classmethod
    def construct(cls, url: str, http: HTTPClient) -> Image:
        self = cls.__new__(cls)
        self._url = url
        self._http = http
        return self

    def __str__(self) -> str:
        return self._url

    def __repr__(self) -> str:
        return f"<Image url={self.url!r}>"

    @property
    def url(self) -> str:
        """:class:`str`: The image URL."""
        return self._url

    @overload
    async def read(self, bytesio: Literal[True] = ...) -> BytesIO:
        ...

    @overload
    async def read(self, bytesio: Literal[False] = ...) -> bytes:
        ...

    @overload
    async def read(self, bytesio: bool = ...) -> Union[bytes, BytesIO]:
        ...

    async def read(self, bytesio: bool = True) -> Union[bytes, BytesIO]:
        """Returns the image data.

        Parameters
        ----------
        bytesio: :class:`bool`
            Whether to return the data as a :class:`io.BytesIO` object. Defaults to ``True``.

        Returns
        -------
        Union[:class:`bytes`, :class:`io.BytesIO`]
            The image data.
        """
        data = await self._http._get_image_url(self.url)
        if not bytesio:
            return data

        return BytesIO(data)

    async def file(self, cls: FileLike, filename: str = "image.png", **kwargs) -> FileLike:
        """Converts the image to a file-like object.

        Parameters
        ----------
        cls: Any
            The file-like object to convert the image to.
            E,g, `discord.File` (discord.py)
        filename: str
            The filename to use.

        Returns
        -------
        Any
            An instance of the file-like object.
        """
        return cls(await self.read(), filename=filename, **kwargs)
