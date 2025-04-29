"""
CREDITS: Discord.py - Permlink: https://github.com/Rapptz/discord.py/blob/4e09c34bbbd034307dbad2713780de60934fe15a/discord/context_managers.py
"""

from __future__ import annotations

from functools import partial
from types import TracebackType
from typing import Any, Callable, Coroutine, Generator, Optional, Protocol, Type, TYPE_CHECKING

import aiohttp

from ..internals.endpoints import Base
from ..internals.http import HTTPClient
from ..models.chatbot import ChatbotResult
from .. import utils as _utils


if TYPE_CHECKING:
    from typing_extensions import Self

    from ..clients.client import Client
    from ..types.http import Chatbot as ChatbotPayload


class _ChatbotRequestMethod(Protocol):
    async def __call__(self, *, message: str) -> ChatbotPayload: ...


__all__ = ("Chatbot",)

"""
class Ratelimit:
    HEADERS: Tuple[str, ...] = ("ratelimit-limit", "ratelimit-remaining")

    def __init__(self, rate: int, per: Union[int, float]) -> None:
        self._max_tries: int = rate
        self._per_seconds: Union[int, float] = per

        self._resets_at: Optional[datetime.datetime] = None
        self._tries: int = 0

    @property
    def per(self) -> Union[int, float]:
        return self._per_seconds

    @property
    def rate(self) -> int:
        return self._max_tries

    @property
    def reset_at(self) -> Optional[datetime.datetime]:
        return self._resets_at

    @property
    def remaining(self) -> int:
        return self._max_tries - self._tries

    def retry_after(self) -> Optional[float]:
        if not self.reset_at:
            return None

        if not self.is_over():
            return (self.reset_at - datetime.datetime.utcnow()).total_seconds()
        return None

    def is_over(self) -> bool:
        now = datetime.datetime.utcnow()
        to_add = datetime.timedelta(seconds=self._per_seconds)
        if not self.reset_at:
            print("is_ver", "not self._reset_at")
            self._resets_at = now + to_add
            return False

        print(
            "is_over",
            now,
            self._resets_at,
            (self.reset_at - now),
            (self.reset_at - now).total_seconds(),
            (self.reset_at - now).total_seconds() <= 0,
        )
        return (self.reset_at - now).total_seconds() <= 0

    def _almost_ratelimited(self, minus: int = 1) -> bool:
        print(
            "_handle",
            self._tries,
            self.rate,
            self.is_over(),
            self._tries >= self.rate - minus and not self.is_over(),
        )
        self.maybe_reset()
        return self._tries >= self.rate - minus and not self.is_over()

    def maybe_reset(self) -> None:
        print("maybe_reset", self.is_over())
        if self.is_over():
            self._tries = 0
            self._reset_at = None
"""


class _ChatbotSendContextManager:
    def __init__(
        self,
        send_request: Callable[[str], Coroutine[Any, Any, ChatbotResult]],
        close_session: Callable[[], Coroutine[Any, Any, None]],
        message: str,
        /,
    ) -> None:
        self.__send_request: Callable[[str], Coroutine[Any, Any, ChatbotResult]] = send_request
        self.__close_session: Callable[[], Coroutine[Any, Any, None]] = close_session
        self.__message: str = message

    async def __aenter__(self):
        return await self.__send_request(self.__message)

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        return await self.__close_session()

    def __await__(self) -> Generator[Any, None, ChatbotResult]:
        return self.__send_request(self.__message).__await__()


class Chatbot:
    """A client for the chatbot endpoint.

    This is a context manager that should be used with the ``async with`` statement to ensure the session is closed.
    Sending a message is done by calling the send method.

    .. container:: operations

        .. describe:: async with x

            Enters the context manager and returns the client.

        .. describe:: await x(message)

            Sends a message to the chatbot and returns the response.


    Example
    -------

    .. code-block:: python3
        :linenos:

        async with Chatbot(...) as chatbot:
            # response = await chatbot.send("Hello") is also valid.
            async with chatbot.send("Hello") as response:
                print(response.response)

    But you can also use it with the ``await`` keyword.

    .. code-block:: python3
        :linenos:

        chatbot = Chatbot(...)
        response = await chatbot.send("Hello")
        print(response.response)

    Or if you don't want to use the ``.send()`` method, you can use ``await`` on the instance of this class directly with the message set on the ``message`` attribute.

    .. code-block:: python3
        :linenos:

        chatbot = Chatbot(message="Hello")
        response = await chatbot()

    Parameters
    ----------
    message: Optional[:class:`str`]
        The message to send to the chatbot. This is only used if you use the ``await`` keyword on an instance of this class.
    client: Optional[:class:`.Client`]
        The client.
        This is also used a session if you don't provide one.
    session: Optional[:class:`aiohttp.ClientSession`]
        The session to use. If this is not provided, a new session will be created.
        You are responsible for closing the session if you provide one.
    """

    _endpoint = Base.CHATBOT
    __request: _ChatbotRequestMethod
    # __ratelimit: Ratelimit

    __slots__ = (
        "_message",
        "__http",
        "__request",
        "_has_provided_client",
        "_has_provided_session",
        # "_handle_ratelimit",
        # "__ratelimit",
    )

    def __init__(
        self,
        message: Optional[str] = None,
        *,
        client: Client = _utils.NOVALUE,
        session: aiohttp.ClientSession = _utils.NOVALUE,
    ) -> None:
        self._has_provided_client: bool = client is not None
        self._has_provided_session: bool = session is not None

        self._message: Optional[str] = message
        # self._handle_ratelimit: bool = _handle_ratelimit

        self.__handle(client, session)

    def __handle(
        self,
        client: Optional[Client],
        session: Optional[aiohttp.ClientSession],
        /,
    ) -> None:
        attrs = [
            "request",
        ]
        if all(hasattr(self, f"_{self.__class__.__name__}__{attr}") for attr in attrs):
            raise RuntimeError("Chatbot is already initialized.")

        if client:
            self.__http = client._http
            client._Client__chatbot = self  # type: ignore
        else:
            self.__http = HTTPClient(None, session=session)
        self.__request = partial(
            self.__http.request,
            self._endpoint,
        )

    async def __do_request(self, message: str) -> ChatbotResult:
        res = await self.__request(message=message)
        return ChatbotResult(message=message, response=res["response"])

    @property
    def message(self) -> Optional[str]:
        """Optional[:class:`str`]: The message to send to the chatbot.

        This is only used if you use the ``await`` keyword on an instance of this class.
        """
        return self._message

    @message.setter
    def message(self, message: Optional[str]) -> None:
        self._message = message

    def send(self, message: str):
        """Sends a message to the chatbot. See :class:`Chatbot` for more information.

        Parameters
        ----------
        message: :class:`str`
            The message to send to the chatbot.
        """
        return _ChatbotSendContextManager(self.__do_request, self.close, message)

    def chat(self, message: str):
        """Alias for :meth:`send`."""
        return self.send(message)

    async def close(self) -> None:
        if self._has_provided_client or self._has_provided_session:
            return

        await self.__http.close()

    def __await__(self) -> Generator[Any, None, ChatbotResult]:
        if self.message is None:
            raise ValueError(
                "No message was provided. Please provide a message in the constructor or use the `.send()` method."
            )

        return self.send(self.message).__await__()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        return await self.close()
