from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Coroutine,
    Generator,
    Generic,
    Literal,
    TypeAlias,
    TypeVar,
    ParamSpec,
    Self,
    Concatenate,
    overload,
)
from functools import wraps

if TYPE_CHECKING:
    from ..internals.http import HTTPClient


__all__ = ()


P = ParamSpec("P")
R = TypeVar("R", covariant=True)
Coro = Coroutine[Any, Any, R]
ClsT = TypeVar("ClsT", bound="BaseClient")

ProxyCallable: TypeAlias = (
    "Callable[Concatenate[ClsT, P], Coro[R]] | Callable[Concatenate[ClsT, P], AsyncContextManagerMethod[P, R]]"
)
ProxyNoParamSpec: TypeAlias = "Callable[[ClsT], Coro[R]] | Callable[[ClsT], AsyncContextManagerMethod[Any, R]]"


def mark_as_context_manager(
    func: Callable[Concatenate[Any, P], Coro[R]],
) -> Callable[Concatenate[Any, P], AsyncContextManagerMethod[Concatenate[Any, P], R]]:
    def inner(self, *args: P.args, **kwargs: P.kwargs) -> AsyncContextManagerMethod[Concatenate[Any, P], R]:
        return AsyncContextManagerMethod(func(self, *args, **kwargs))

    return inner


class AsyncContextManagerMethod(Generic[P, R]):
    def __init__(self, coro: Coro[R], /) -> None:
        self.__coro: Coro[R] = coro

    # for why __get__ and __call__ are like this, see https://stackoverflow.com/a/74636779/14127228
    # same applies to the decorator above
    def __get__(self, instance: Any, owner: type | None = None) -> Callable[P, R]: ...

    def __call__(self_, self: Any, *args: P.args, **kwargs: P.kwargs) -> R:  # type: ignore
        ...

    def __aenter__(self) -> Coro[R]:
        return self.__coro

    def __await__(self) -> Generator[Any, None, R]:
        return self.__coro.__await__()

    async def __aexit__(self, *_: Any) -> None:
        pass

    def __repr__(self) -> str:
        return f"<async with or await {self.__coro!r}>"


class WithContextManager:
    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *_: Any) -> None:
        pass

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_: Any) -> None:
        pass


class BaseClient(WithContextManager):
    """Represents the "{endpoint_name}" endpoint.

    This class is not meant to be instantiated by the user. Instead, access it through the :attr:`~{qualified_class_name}.{attribute_name}` attribute of the :class:`~{qualified_class_name}` class.
    """

    __slots__ = ("_http",)

    def __init__(self, http: HTTPClient, /) -> None:
        self._http: HTTPClient = http

    @staticmethod
    def _contextmanager(
        func: Callable[Concatenate[Any, P], Coro[R]],
    ) -> Callable[Concatenate[Any, P], AsyncContextManagerMethod[Concatenate[Any, P], R]]:
        raise NotImplementedError("Remove the decorator from the function.")
        return mark_as_context_manager(func)

    @staticmethod
    @overload
    def _proxy_to(
        method: Callable[Concatenate[Any, P], AsyncContextManagerMethod[P, R]],
        *,
        copy_params_of: Literal["NONE", "DECORATED", "METHOD"] = ...,
        pre_args: tuple[tuple[int, Any], ...] | None = ...,
        **partial_kwargs: Any,
    ) -> Callable[
        [Callable[Concatenate[Any, P], AsyncContextManagerMethod[P, R]]],
        Callable[Concatenate[Any, P], AsyncContextManagerMethod[P, R]],
    ]: ...

    @staticmethod
    @overload
    def _proxy_to(
        method: ProxyCallable[Any, ..., R],
        *,
        copy_params_of: Literal["DECORATED"] = ...,
        pre_args: tuple[tuple[int, Any], ...] | None = ...,
        **partial_kwargs: Any,
    ) -> Callable[[ProxyCallable[Any, P, R]], ProxyCallable[Any, P, R]]: ...

    @staticmethod
    @overload
    def _proxy_to(
        method: ProxyCallable[Any, P, R],
        *,
        copy_params_of: Literal["METHOD"] = ...,
        pre_args: tuple[tuple[int, Any], ...] | None = ...,
        **partial_kwargs: Any,
    ) -> Callable[[ProxyCallable[Any, P, R]], ProxyCallable[Any, P, R]]: ...

    @staticmethod
    @overload
    def _proxy_to(
        method: ProxyCallable[Any, ..., R],
        *,
        copy_params_of: Literal["NONE"] = ...,
        pre_args: tuple[tuple[int, Any], ...] | None = ...,
        **partial_kwargs: Any,
    ) -> Callable[[ProxyNoParamSpec[Any, R]], ProxyNoParamSpec[Any, R]]: ...

    @staticmethod
    def _proxy_to(
        method: ProxyCallable[Any, P, R] | ProxyCallable[Any, ..., R],
        *,
        copy_params_of: Literal["NONE", "DECORATED", "METHOD"] = "NONE",
        pre_args: tuple[tuple[int, Any], ...] | None = None,
        **partial_kwargs: Any,
    ) -> (
        Callable[[ProxyCallable[Any, P, R]], ProxyCallable[Any, P, R]]
        | Callable[[ProxyCallable[Any, ..., R]], ProxyCallable[Any, ..., R]]
        | Callable[[ProxyNoParamSpec[Any, R]], ProxyNoParamSpec[Any, R]]
    ):
        def decorator(
            func: ProxyCallable[Any, P, R] | ProxyCallable[Any, ..., R],
        ) -> ProxyCallable[Any, P, R] | ProxyCallable[Any, ..., R]:
            @wraps(func)
            def wrapper(self: Self, *args: Any, **kwargs: Any) -> AsyncContextManagerMethod[P, R] | Coro[R]:
                # Insert pre_args at their specified positions in args
                if pre_args:
                    args_list = list(args)
                    for idx, value in sorted(pre_args, key=lambda x: x[0]):
                        args_list.insert(idx, value)
                    final_args = tuple(args_list)
                else:
                    final_args = args

                return method(self, *final_args, **(partial_kwargs | kwargs))

            return wrapper  # type: ignore

        return decorator
