from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Concatenate,
    Generic,
    Literal,
    ParamSpec,
    Self,
    TypeAlias,
    TypeVar,
    overload,
)
from collections.abc import Callable, Coroutine, Generator
from functools import wraps
import operator

if TYPE_CHECKING:
    from ..internals.http import HTTPClient


__all__ = ()


P = ParamSpec("P")
R_co = TypeVar("R_co", covariant=True)
Coro = Coroutine[Any, Any, R_co]
ClsT = TypeVar("ClsT", bound="BaseClient")

ProxyCallable: TypeAlias = (
    "Callable[Concatenate[ClsT, P], Coro[R_co]] | Callable[Concatenate[ClsT, P], AsyncContextManagerMethod[P, R_co]]"
)
ProxyNoParamSpec: TypeAlias = "Callable[[ClsT], Coro[R_co]] | Callable[[ClsT], AsyncContextManagerMethod[Any, R_co]]"


def mark_as_context_manager(
    func: Callable[Concatenate[Any, P], Coro[R_co]],
) -> Callable[Concatenate[Any, P], AsyncContextManagerMethod[Concatenate[Any, P], R_co]]:
    def inner(self: object, *args: P.args, **kwargs: P.kwargs) -> AsyncContextManagerMethod[Concatenate[Any, P], R_co]:
        return AsyncContextManagerMethod(func(self, *args, **kwargs))

    return inner


class AsyncContextManagerMethod(Generic[P, R_co]):
    def __init__(self, coro: Coro[R_co], /) -> None:
        self.__coro: Coro[R_co] = coro

    # for why __get__ and __call__ are like this, see https://stackoverflow.com/a/74636779/14127228
    # same applies to the decorator above
    def __get__(self, instance: Any, owner: type | None = None) -> Callable[P, R_co]: ...

    def __call__(self_, self: Any, *args: P.args, **kwargs: P.kwargs) -> R_co: ...  # pyright: ignore[reportSelfClsParameterName]

    def __aenter__(self) -> Coro[R_co]:
        return self.__coro

    def __await__(self) -> Generator[Any, None, R_co]:
        return self.__coro.__await__()

    async def __aexit__(self, *_: object) -> None:
        pass

    def __repr__(self) -> str:
        return f"<async with or await {self.__coro!r}>"


class WithContextManager:
    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *_: object) -> None:
        pass

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_: object) -> None:
        pass


class BaseClient(WithContextManager):
    __slots__ = ("_http",)

    def __init__(self, http: HTTPClient, /) -> None:
        self._http: HTTPClient = http

    @staticmethod
    def _contextmanager(
        func: Callable[Concatenate[Any, P], Coro[R_co]],
    ) -> Callable[Concatenate[Any, P], AsyncContextManagerMethod[Concatenate[Any, P], R_co]]:
        raise NotImplementedError("Remove the decorator from the function. it's a WIP.")
        return mark_as_context_manager(func)

    @staticmethod
    @overload
    def _proxy_to(
        method: Callable[Concatenate[Any, P], AsyncContextManagerMethod[P, R_co]],
        *,
        copy_params_of: Literal["NONE", "DECORATED", "METHOD"] = ...,
        pre_args: tuple[tuple[int, Any], ...] | None = ...,
        **partial_kwargs: Any,
    ) -> Callable[
        [Callable[Concatenate[Any, P], AsyncContextManagerMethod[P, R_co]]],
        Callable[Concatenate[Any, P], AsyncContextManagerMethod[P, R_co]],
    ]: ...

    @staticmethod
    @overload
    def _proxy_to(
        method: ProxyCallable[Any, ..., R_co],
        *,
        copy_params_of: Literal["DECORATED"] = ...,
        pre_args: tuple[tuple[int, Any], ...] | None = ...,
        **partial_kwargs: Any,
    ) -> Callable[[ProxyCallable[Any, P, R_co]], ProxyCallable[Any, P, R_co]]: ...

    @staticmethod
    @overload
    def _proxy_to(
        method: ProxyCallable[Any, P, R_co],
        *,
        copy_params_of: Literal["METHOD"] = ...,
        pre_args: tuple[tuple[int, Any], ...] | None = ...,
        **partial_kwargs: Any,
    ) -> Callable[[ProxyCallable[Any, P, R_co]], ProxyCallable[Any, P, R_co]]: ...

    @staticmethod
    @overload
    def _proxy_to(
        method: ProxyCallable[Any, ..., R_co],
        *,
        copy_params_of: Literal["NONE"] = ...,
        pre_args: tuple[tuple[int, Any], ...] | None = ...,
        **partial_kwargs: Any,
    ) -> Callable[[ProxyNoParamSpec[Any, R_co]], ProxyNoParamSpec[Any, R_co]]: ...

    @staticmethod
    def _proxy_to(  # pyright: ignore[reportInconsistentOverload] # it works :)
        method: ProxyCallable[Any, P, R_co] | ProxyCallable[Any, ..., R_co],
        *,
        copy_params_of: Literal["NONE", "DECORATED", "METHOD"] = "NONE",
        pre_args: tuple[tuple[int, Any], ...] | None = None,
        **partial_kwargs: Any,
    ) -> (
        Callable[[ProxyCallable[Any, P, R_co]], ProxyCallable[Any, P, R_co]]
        | Callable[[ProxyCallable[Any, ..., R_co]], ProxyCallable[Any, ..., R_co]]
        | Callable[[ProxyNoParamSpec[Any, R_co]], ProxyNoParamSpec[Any, R_co]]
    ):
        def decorator(
            func: ProxyCallable[Any, P, R_co] | ProxyCallable[Any, ..., R_co],
        ) -> ProxyCallable[Any, P, R_co] | ProxyCallable[Any, ..., R_co]:
            @wraps(func)
            def wrapper(self: Self, *args: Any, **kwargs: Any) -> AsyncContextManagerMethod[P, R_co] | Coro[R_co]:
                # Insert pre_args at their specified positions in args
                if pre_args:
                    args_list = list(args)
                    for idx, value in sorted(pre_args, key=operator.itemgetter(0)):
                        args_list.insert(idx, value)
                    final_args = tuple(args_list)
                else:
                    final_args = args

                return method(self, *final_args, **(partial_kwargs | kwargs))

            return wrapper  # pyright: ignore[reportReturnType] # it works :)

        return decorator
