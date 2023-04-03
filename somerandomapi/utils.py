from __future__ import annotations

import random
import re
from dataclasses import Field
from typing import Any, get_args, get_origin, Literal, Match, Optional, Tuple, Type, TYPE_CHECKING, TypeVar, Union

from somerandomapi.errors import TypingError


if TYPE_CHECKING:
    from .enums import BaseEnum
    from .models.abc import BaseModel

__all__: Tuple[str, ...] = ()

EnumT = TypeVar("EnumT", bound="BaseEnum")


def _try_enum(enum: Type[EnumT], input: Any) -> Optional[EnumT]:
    if not input:
        return None

    try:
        return enum[input.upper()] # name
    except KeyError:
        try:
            return enum(input.lower()) # value
        except ValueError:
            return None

def _gen_colour(numbers: Optional[int] = None) -> str:
    random_number = numbers or random.randint(0, 16777215)
    hex_number = str(hex(random_number))
    return hex_number[2:]


def _check_colour_value(hex_input: Optional[Union[str, int]], param_name: Optional[str] = None) -> str:
    INVALID_COLOR_ERROR = (
        f"'{param_name or 'colour'}' must be a valid hex value (#000000, 000000 or 0x000000) or 'random'"
    )
    should_random = str(hex_input).lower() == "random"
    if not hex_input and not should_random:
        raise ValueError(INVALID_COLOR_ERROR)

    if should_random:
        return _gen_colour()
    elif hex_input and isinstance(hex_input, int):
        return _gen_colour(int(hex_input))
    else:
        match: Optional[Match[str]] = re.search(r"^#?(?:[0-9a-fA-F]{3}){1,2}$", str(hex_input))
        if match:
            return match.string.strip("#")

    raise ValueError(INVALID_COLOR_ERROR)


def _get_literal_type(_type: Type, gs: dict[str, Any], lc: dict[str, Any]) -> Optional[Literal]:
    if isinstance(_type, str):
        _type = eval(_type, gs.update(globals()), lc.update(locals()))

    origin = get_origin(_type)

    if origin is Literal:
        return _type

    return None


def _check_literal_values(cls, field: Field, _type: Literal, values: Tuple[Any, ...]) -> None:
    args = get_args(_type)
    # shouldn't happen.
    if len(args) < 1:
        raise TypeError("Expected more than one argument for Literal type")

    join_args = ", ".join(map(str, args))
    for val in values:
        if val not in args:
            raise TypingError(
                cls,
                field,
                values,
                messages="'{val}' is not a valid value for argument `{arg_name}`. Expected one of: {join_args}",
                val=val,
                arg_name=field.name,
                join_args=join_args,
            )


def _is_optional(_type: Type) -> bool:
    return get_origin(_type) is Union and type(None) in get_args(_type)


def _get_type(_type: Type, gs: dict[str, Any], lc: dict[str, Any]) -> Tuple[Any, ...]:
    origin = get_origin(_type)
    if literal := _get_literal_type(_type, gs, lc):
        return (literal,)
    elif origin is Union:
        if _is_optional(_type):
            return [x for x in get_args(_type) if x is not type(None)][0]

        args = get_args(_type)
        for arg in args:
            if get_origin(arg) is Literal:
                return (get_args(arg),)

        return args
    elif origin is list:
        return (get_args(_type)[0],)
    elif origin is dict:
        return (get_args(_type)[1],)
    elif origin is tuple:
        return get_args(_type)

    return (_type,)


def _check_types(
    cls, field: Field, _type: Type, value: Union[str, int, Any], gls: dict[str, Any], lcs: dict[str, Any]
) -> None:
    glbs = gls | globals()
    lcls = lcs | locals()

    if isinstance(_type, str):
        _type = eval(_type, glbs, lcls)

    if value is None:
        return

    if literal := _get_literal_type(_type, glbs, lcls):
        _check_literal_values(cls, field, literal, (value,))
        return

    origin = get_origin(_type)
    if origin is Union:
        if _is_optional(_type):
            if value is None:
                return
            _type = [x for x in get_args(_type) if x is not type(None)][0]
            _check_types(cls, field, _type, value, glbs, lcls)
            return

        args = get_args(_type)
        for arg in args:
            if get_origin(arg) is Literal:
                _check_literal_values(cls, field, arg, (value,))
                return

        for arg in args:
            try:
                _check_types(cls, field, arg, value, glbs, lcls)
                return
            except TypingError:
                pass

        raise TypingError(
            cls,
            field,
            value,
            message="expected instance of {valids}, not {field_value_type}.",
            valids=", ".join(map(str, args)),
        )

    elif origin is list:
        if not isinstance(value, list):
            raise TypingError(cls, field, value, message="expected instance of list, not {field_value_type}.")

        for val in value:
            _check_types(cls, field, get_args(_type)[0], val, glbs, lcls)

    elif origin is dict:
        if not isinstance(value, dict):
            raise TypingError(cls, field, value, message="expected instance of dict, not {field_value_type}.")

        for val in value.values():
            _check_types(cls, field, get_args(_type)[1], val, glbs, lcls)

    elif origin is tuple:
        if not isinstance(value, tuple):
            raise TypingError(cls, field, value, message="expected instance of tuple, not {field_value_type}.")

        for arg, val in zip(get_args(_type), value):
            _check_types(cls, field, arg, val, glbs, lcls)

    elif not isinstance(value, _type):
        raise TypingError(cls, field, value, message="expected instance of {field_type}, not {field_value_type}.")

    return


ObjT = TypeVar("ObjT", bound="BaseModel")


def _handle_obj_or_args(required_object: Any, obj: Optional[ObjT], args: Tuple[Tuple[str, Any, bool], ...]) -> ObjT:
    if obj:
        if not isinstance(obj, required_object):
            raise TypeError(f"obj argument expected instance of {required_object.__name__}, not {type(obj).__name__}.")
        return obj

    required_arguments: list[str] = []
    for name, value, required in args:
        if required and not value:
            required_arguments.append(name)

    if not obj and required_arguments:
        raise ValueError(
            f"Expected either an instance of {required_object.__name__} to the obj arg or all of these required arguments: {', '.join(required_arguments)}"
        )

    return required_object(**{name: value for (name, value, _) in args})


"""
from .internals.endpoints import BaseEndpoint, CanvasMisc


T = TypeVar("T")
T2 = TypeVar("T2")
E = TypeVar("E", bound=BaseEndpoint)
CoroT = Coroutine[Any, Any, T]

if TYPE_CHECKING:
    from typing_extensions import ParamSpec

    P = ParamSpec("P")
    P2 = ParamSpec("P2")
else:
    P = TypeVar("P")
    P2 = TypeVar("P2")


class Endpoint(Generic[P, T, E]):
    __client: Client
    __endpoint__: E

    def __init__(
        self,
        func: Callable[P, T],
        endpoint: E,
        to_call: Optional[Optional[Callable[Concatenate[Client, E, P], Callable[P, CoroT[T]]]]],
    ) -> None:
        self._endpoint: E = endpoint
        self._func: Callable[P, T] = func
        self._to_call: Optional[Optional[Callable[Concatenate[Client, E, P], Callable[P, CoroT[T]]]]] = to_call

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        print("funcret call", args, kwargs, self.__client, self._func, self._endpoint)
        if self._to_call is not None:
            return self._to_call(self.__client, self._endpoint, *args, **kwargs)  # type: ignore
        else:
            return self._func(self.__client, *args, **kwargs)  # type: ignore

    def __get__(self, obj, objtype):
        if obj is None:
            raise ValueError("Cannot use this endpoint without a client instance")

        copy = Endpoint(self._func, self._endpoint, self._to_call)
        copy.__client = obj
        return copy


# "Concatenate[Client, P]"
# "Concatenate[Client, E, P]"

# fmt: off

@overload
def endpoint(
    endpoint: E,
    *,
    to_call: Literal[None] = ...,
) -> Callable[[Callable[P, T]], Endpoint[P, T, E]]:
    ...

@overload
def endpoint(
    endpoint: E,
    *,
    to_call: Callable[Concatenate[Client, E, P], Callable[P,  CoroT[T]]] = ...,
) -> Callable[Concatenate[Client, E, P], Callable[Concatenate[Client, E, P],  CoroT[T]]]:
    ...

def endpoint(
    endpoint: E,
    *,
    to_call: Optional[Callable[Concatenate[Client, Type[E], P], Callable[P,  CoroT[T]]]] = None,
) -> Union[
        Callable[[Callable[P, T]], Endpoint[P, T, E]],
        Callable[Concatenate[Client, E, P], Callable[Concatenate[Client, E, P],  CoroT[T]]],
    ]:
    def decorator(func: Callable[P, T]) -> Union[
        Endpoint[P, T, E],
        Callable[Concatenate[Client, E, P],  CoroT[T]]
    ]:
        return Endpoint(func, endpoint, to_call)
    return decorator


# fmt: on


# @endpoint(CanvasMisc.HEX)
# async def rgb_to_hex(red: int, green: int, blue: int) -> str:
#    return f"{red:02x}{green:02x}{blue:02x}"

# reveal_type(rgb_to_hex(1,2,3).__endpoint__)
"""
