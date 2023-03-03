from __future__ import annotations

import io
from typing import Any, Literal, Optional, overload, Protocol, TYPE_CHECKING, Union


if TYPE_CHECKING:
    from os import PathLike

    from typing_extensions import Self

    from ..internals.http import HTTPClient

    class FileLike(Protocol):
        def __call__(
            self,
            fp: Union[str, bytes, PathLike[Any], io.BufferedIOBase],
            filename: Optional[str] = None,
            **kwargs: Any,
        ) -> Self:
            ...


__all__ = ("Image",)


class Image:
    """Represents a class for all image endpoints."""

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
        return getattr(self, "_url", "")

    def __repr__(self) -> str:
        return f"<Image url={self.url!r}>"

    @property
    def url(self) -> str:
        """:class:`str`: The image URL."""
        return self._url

    @overload
    async def read(self, bytesio: Literal[True] = ...) -> io.BytesIO:
        ...

    @overload
    async def read(self, bytesio: Literal[False] = ...) -> bytes:
        ...

    @overload
    async def read(self, bytesio: bool = ...) -> Union[bytes, io.BytesIO]:
        ...

    async def read(self, bytesio: bool = True) -> Union[bytes, io.BytesIO]:
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

        return io.BytesIO(data)

    async def file(self, cls: FileLike, filename: str = "image.png", **kwargs) -> FileLike:
        """Converts the image to a file-like object.

        Parameters
        ----------
        cls: ``FileLike``
            The file-like object to convert the image to.
            E,g, `discord.File` (discord.py)
        filename: str
            The filename to use.

        Returns
        -------
        ``FileLike``
            An instance of the file-like object.
        """
        return cls(await self.read(), filename=filename, **kwargs)
