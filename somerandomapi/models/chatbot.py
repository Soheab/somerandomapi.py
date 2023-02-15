"""
CREDITS: Discord.py - Permlink: 
"""

from __future__ import annotations
from types import TracebackType
from typing import TYPE_CHECKING, Any, ClassVar, Generator, Literal, Optional

from dataclasses import dataclass
from functools import partial

from ..internals.endpoints import Chatbot as ChatbotEndpoints
from ..internals.http import HTTPClient

if TYPE_CHECKING:
    from typing_extensions import Self


class Chatbot:
    def __init__(self, key: str = "xPaGmDj8KvFkpBf5MXZd2RDsV") -> None:
        self.key = key
        self.__http: HTTPClient = HTTPClient()

    async def do_request(self, message: str) -> None:
        req = partial(self.__http.request, ChatbotEndpoints.CHATBOT, key=self.key)
        return await req(message=message)

    async def send(self, message: str) -> Any:
        await self.do_request(message)

    def __await__(self) -> Generator[None, None, None]:
        return self.send.__await__()

    async def __aenter__(self) -> None:
        return self

    async def __aexit__(self, exc_type, exc, traceback) -> None:
        self.__http.close()
