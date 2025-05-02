from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, Self
from collections.abc import Callable, Coroutine, Generator
from functools import partial

import aiohttp

from .. import utils as _utils
from ..internals.endpoints import Base
from ..internals.http import HTTPClient
from ..models.chatbot import ChatbotResult

if TYPE_CHECKING:
    from ..clients.client import Client
    from ..types.http import Chatbot as ChatbotPayload


class _ChatbotRequestMethod(Protocol):
    async def __call__(self, *, message: str) -> ChatbotPayload: ...


__all__ = ("Chatbot",)


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

    async def __aexit__(self, *_: object) -> None:
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

    Or if you don't want to use the ``.send()`` method, you can use ``await`` on the instance of this class directly
    with the message set on the ``message`` attribute.

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

    __slots__ = (
        "__http",
        "__request",
        "_has_provided_client",
        "_has_provided_session",
        "_message",
    )

    def __init__(
        self,
        message: str | None = None,
        *,
        client: Client = _utils.NOVALUE,
        session: aiohttp.ClientSession = _utils.NOVALUE,
    ) -> None:
        self._has_provided_client: bool = client is not None
        self._has_provided_session: bool = session is not None

        self._message: str | None = message

        self.__handle(client, session)

    def __handle(
        self,
        client: Client | None,
        session: aiohttp.ClientSession | None,
        /,
    ) -> None:
        attrs = [
            "request",
        ]
        if all(hasattr(self, f"_{self.__class__.__name__}__{attr}") for attr in attrs):
            raise RuntimeError("Chatbot is already initialized.")

        if client:
            self.__http = client._http
            client._Client__chatbot = self  # pyright: ignore[reportAttributeAccessIssue]
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
    def message(self) -> str | None:
        """Optional[:class:`str`]: The message to send to the chatbot.

        This is only used if you use the ``await`` keyword on an instance of this class.
        """
        return self._message

    @message.setter
    def message(self, message: str | None) -> None:
        self._message = message

    def send(self, message: str) -> _ChatbotSendContextManager:
        """Sends a message to the chatbot. See :class:`Chatbot` for more information.

        Parameters
        ----------
        message: :class:`str`
            The message to send to the chatbot.
        """
        return _ChatbotSendContextManager(self.__do_request, self.close, message)

    def chat(self, message: str) -> _ChatbotSendContextManager:
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

    async def __aexit__(self, *_: object) -> None:
        return await self.close()
