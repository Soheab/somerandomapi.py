"""
CREDITS: Discord.py - Permlink: https://github.com/Rapptz/discord.py/blob/4e09c34bbbd034307dbad2713780de60934fe15a/discord/context_managers.py
"""

from __future__ import annotations

from functools import partial
from types import TracebackType
from typing import Any, Callable, Coroutine, Generator, Literal, Optional, Protocol, Type, TYPE_CHECKING

import aiohttp

from ..internals.endpoints import Chatbot as ChatbotEndpoints
from ..internals.http import HTTPClient
from ..models.chatbot import ChatbotResult


if TYPE_CHECKING:
    from typing_extensions import Self

    from ..clients.client import Client
    from ..types.chatbot import Chatbot as ChatbotPayload


class _ChatbotRequestMethod(Protocol):
    async def __call__(self, *, message: str) -> ChatbotPayload:
        ...


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
        The client. If this is not provided, you must provide a key and a key_tier.
        This is also used a session if you don't provide one.

    key: Optional[:class:`str`]
        The key to use. If this is not provided, you must provide a client.
    key_tier: Optional[:class:`int`]
        The tier of the key. This is only used if you provide a key and not a client because the tier should already be set on the client unless
    session: Optional[:class:`aiohttp.ClientSession`]
        The session to use. If this is not provided, a new session will be created.
        You are responsible for closing the session if you provide one.
    """

    """
        Required if ``_handle_ratelimit`` is set to ``True``.
        This is used for the ratelimit handling.
        As of writing:
        - 1: 15 requests per 60 seconds
        - 2: 30 requests per 60 seconds
        - 3: 60 requests per 60 seconds

    _handle_ratelimit: :class:`bool`
        https://some-random-api.com/docs/welcome/ratelimits#chatbot
        Whether to handle the ratelimit automatically. This is subject to change and should not be relied on.
        If this is set to ``True``, you must provide either a client or a key and a key_tier.
    """

    _endpoint = ChatbotEndpoints.CHATBOT
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
        client: Optional[Client] = None,
        key: Optional[str] = None,
        key_tier: Optional[Literal[0, 1, 2, 3]] = None,
        # _handle_ratelimit: bool = False,
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        self._has_provided_client: bool = client is not None
        self._has_provided_session: bool = session is not None
        if key_tier is not None and key_tier not in range(4):
            raise ValueError(f"key_tier must be one of {', '.join(map(str, range(4)))}.")

        self._message: Optional[str] = message
        # self._handle_ratelimit: bool = _handle_ratelimit

        self.__handle(client, key, key_tier, session)

    def __handle(
        self,
        client: Optional[Client],
        key: Optional[str],
        key_tier: Optional[Literal[0, 1, 2, 3]],
        session: Optional[aiohttp.ClientSession],
        /,
    ) -> None:
        attrs = [
            "request",
        ]  # "__ratelimit"]
        if all(hasattr(self, f"_{self.__class__.__name__}__{attr}") for attr in attrs):
            raise RuntimeError("Chatbot is already initialized.")

        # ratelimit_per_tier = {1: (15, 60), 2: (30, 60), 3: (60, 60)}
        key_param = self._endpoint.value.parameters["key"]

        actual_key_tier = key_param.key_tier
        if not client and not key:
            raise ValueError(
                (
                    f"Please provide either a tier {actual_key_tier} or "
                    f"above key via 'key=` or "
                    f"a client instance to get the key from with a tier {actual_key_tier} key set via 'client=' or "
                    "both in the Chatbot constructor."
                )
            )

        if client:
            self.__http = client._http
            client._Client__chatbot = self  # type: ignore
        else:
            self.__http = HTTPClient(None, session=session)
        self.__request = partial(self.__http.request, self._endpoint, key=key)  # type: ignore

        """
        if not self._handle_ratelimit:
            return

        if hasattr(self, f"_{self.__class__.__name__}__ratelimit"):
            raise RuntimeError("Chatbot is already initialized.")

        if client and client._http._key and client._http._key.tier >= actual_key_tier:
            self.__ratelimit = Ratelimit(*ratelimit_per_tier[client._http._key.tier])
        elif key_tier and key_tier >= actual_key_tier:
            self.__ratelimit = Ratelimit(*ratelimit_per_tier[key_tier])
        else:
            raise ValueError(
                (
                    f"_handle_ratelimit is True but no {key_tier} or above tier key was provided. "
                    "Please either pass one in the Chatbot constructor or set it on the Client. "
                    "Or set _handle_ratelimit to False."
                )
            )
        """

    async def __do_request(self, message: str) -> ChatbotResult:
        """
        if self._handle_ratelimit and self.__ratelimit:
            self.__ratelimit._tries += 1
            if self.__ratelimit._almost_ratelimited() and (retry_after := self.__ratelimit.retry_after()):
                print("Waiting", retry_after, "seconds...")
                await asyncio.sleep(int(retry_after))
                self.__ratelimit.maybe_reset()
        """

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
                f"No message was provided. Please provide a message in the constructor or use the `.send()` method."
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
