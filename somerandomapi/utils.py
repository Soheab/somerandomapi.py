from __future__ import annotations

from types import UnionType
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, get_args, get_origin  # pyright: ignore[reportDeprecated]
import random
import re

if TYPE_CHECKING:
    from collections.abc import Iterable
    from dataclasses import Field

    from .enums import BaseEnum
    from .models.abc import BaseModel

__all__: tuple[str, ...] = ()


# https://en.wikipedia.org/wiki/Sentinel_value
class _NOVALUE:
    __slots__ = ()

    def __eq__(self, other: object) -> bool:
        return False

    def __bool__(self) -> bool:
        return False

    def __hash__(self) -> int:
        return 0

    def __repr__(self) -> Literal["..."]:
        return "..."


NOVALUE: Any = _NOVALUE()


EnumT = TypeVar("EnumT", bound="BaseEnum")


def _try_enum(enum: type[EnumT], _input: Any) -> EnumT | None:
    if not _input:
        return None

    if isinstance(_input, enum):
        return _input

    try:
        return enum[_input.upper()]  # name
    except KeyError:
        try:
            return enum(_input.lower())  # value
        except ValueError:
            return None


def _gen_colour(numbers: int | None = None) -> str:
    random_number = numbers or random.randint(0, 0xFFFFFF)  # noqa: S311
    return f"{random_number:06x}"


def _check_colour_value(hex_input: str | int | None, param_name: str | None = None) -> str:
    INVALID_COLOR_ERROR = (
        f"Invalid value for '{param_name or 'colour'}': {hex_input!r}. "
        "Expected one of the following formats:\n"
        "- A valid hex value (e.g., #000000, 000000, 0x000000)\n"
        "- An RGB value (e.g., rgb(255, 255, 255) or 255,255,255)\n"
        "- The string 'random' to generate a random colour"
    )

    def rgb_to_hex(r: int, g: int, b: int) -> str:
        if not all(0 <= color <= 255 for color in (r, g, b)):
            out_of_range = ", ".join(
                f"{color_name}={color} ({'+' if color > 255 else ''}{color - 255 if color > 255 else color})"
                for color_name, color in zip(["red", "green", "blue"], [r, g, b], strict=False)
                if not (0 <= color <= 255)
            )
            msg = f"RGB values out of range: {out_of_range}. Expected all values to be between 0 and 255 inclusive."
            raise ValueError(
                msg,
            )
        return f"{r:02x}{g:02x}{b:02x}"

    if hex_input in (None, NOVALUE) or (isinstance(hex_input, str) and hex_input.lower() == "random"):
        return _gen_colour()

    if isinstance(hex_input, int):
        return _gen_colour(hex_input)

    hex_input_str = str(hex_input).strip().lstrip("#").lower()
    if re.fullmatch(r"(?:[0-9a-f]{3}){1,2}", hex_input_str):
        return hex_input_str

    rgb_match = re.fullmatch(r"rgb\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)", hex_input_str)
    if rgb_match:
        return rgb_to_hex(*map(int, rgb_match.groups()))

    raise ValueError(INVALID_COLOR_ERROR)


def _human_join(items: Iterable[str], sep: str = ", ", last_sep: str = " and ") -> str:
    """Join a list of items into a human-readable string.

    Parameters
    ----------
    items: Iterable[str]
        The items to join.
    sep: str
        The separator to use between items.
    last_sep: str
        The separator to use before the last item.

    Returns
    -------
    str
        The joined string.
    """
    items = list(items)
    if not items:
        return ""

    if len(items) == 1:
        return items[0]

    return f"{sep.join(items[:-1])}{last_sep}{items[-1]}"


def _builin_types_from_str(_type: str) -> str | None:
    if not isinstance(_type, str):
        return _type

    if _type.startswith("ClassVar["):
        _type = _type.removeprefix("ClassVar[").removesuffix("]")
    elif _type.startswith("typing."):
        _type = _type.removeprefix("typing.")
    elif _type.startswith("typing_extensions."):
        _type = _type.removeprefix("typing_extensions.")
    elif _type.startswith("collections.abc."):
        _type = _type.removeprefix("collections.abc.")

    return _type


def _get_literal_type(_type: type | UnionType, gs: dict[str, Any], lc: dict[str, Any]) -> type | UnionType | None:
    if _type and isinstance(_type, str):
        _type = eval(_type, gs | globals(), lc | locals())  # noqa: S307

    origin = get_origin(_type)

    if origin is Literal:
        return _type

    return None


def _check_literal_values(cls, field: Field, _type: type | UnionType, values: tuple[Any, ...]) -> None:
    # this is here to prevent circular imports.
    from somerandomapi.errors import TypingError  # noqa: PLC0415

    args = get_args(_type)
    # shouldn't happen.
    if len(args) < 1:
        msg = "Expected more than one argument for Literal type"
        raise TypeError(msg)

    join_args = _human_join(
        map(str, args),
        last_sep=" or ",
    )
    for val in values:
        if val not in args:
            raise TypingError(
                cls,
                field,
                values,
                message="'{val}' is not a valid value for argument `{arg_name}`. Expected one of: {join_args}",
                val=val,
                arg_name=field.name,
                join_args=join_args,
            )


def _is_optional(_type: type) -> bool:
    return get_origin(_type) is Union and type(None) in get_args(_type)  # pyright: ignore[reportDeprecated]


def _get_type(_type: type, gs: dict[str, Any], lc: dict[str, Any]) -> tuple[Any, ...]:
    origin = get_origin(_type)
    _type = _builin_types_from_str(_type)  # pyright: ignore[reportAssignmentType, reportArgumentType]
    if literal := _get_literal_type(_type, gs, lc):
        return (literal,)
    if origin is Union:  # pyright: ignore[reportDeprecated]
        if _is_optional(_type):
            return (next(x for x in get_args(_type) if x is not type(None)),)

        args = get_args(_type)
        for arg in args:
            if get_origin(arg) is Literal:
                return (get_args(arg),)

        return args
    if origin is list:
        return (get_args(_type)[0],)
    if origin is dict:
        return (get_args(_type)[1],)
    if origin is tuple:
        return get_args(_type)

    return (_type,)


def _check_types(
    cls,
    attribute: Any,
    _type: type | UnionType,
    value: str | int | Any,
    gls: dict[str, Any],
    lcs: dict[str, Any],
) -> None:
    # this is here to prevent circular imports.
    from somerandomapi.errors import TypingError  # noqa: PLC0415

    EXPECTED_INSTANCE_MESSAGE = "expected instance of {expected_type}, not {field_value_type}."

    glbs = gls | globals()
    lcls = lcs | locals()

    if isinstance(_type, str):
        _type = _builin_types_from_str(_type)  # pyright: ignore[reportAssignmentType]
        _type = eval(_type, glbs, lcs)  # pyright: ignore[reportArgumentType] # noqa: S307

    if value is None:
        if attribute.default is not None:
            raise TypingError(cls, attribute, value, message=EXPECTED_INSTANCE_MESSAGE, expected_type=_type, cast_type=False)
        else:
            return

    try:
        if isinstance(value, _type):
            return
    except TypeError:
        pass

    if literal := _get_literal_type(_type, glbs, lcls):
        _check_literal_values(cls, attribute, literal, (value,))
        return

    origin = get_origin(_type)
    if origin in (Union, UnionType):  # pyright: ignore[reportDeprecated]
        args = get_args(_type)
        if type(None) in args:  # Optional type
            inner_type = next(t for t in args if t is not type(None))
            _check_types(cls, attribute, inner_type, value, glbs, lcls)
            return

        # Union type
        for arg in args:
            try:
                if get_origin(arg) is Literal:
                    _check_literal_values(cls, attribute, arg, (value,))
                else:
                    _check_types(cls, attribute, arg, value, glbs, lcls)
                    return
            except (TypingError, ValueError):  # noqa: S112
                continue

        raise TypingError(
            cls,
            attribute,
            value,
            message=EXPECTED_INSTANCE_MESSAGE,
            expected_type=_human_join(map(str, args), last_sep=" or "),
        )

    if origin in (list, tuple):
        container_type = origin.__name__
        if not isinstance(value, origin):
            raise TypingError(cls, attribute, value, message=EXPECTED_INSTANCE_MESSAGE, expected_type=container_type)

        type_args = get_args(_type)
        if not type_args:  # e.g., list without inner type
            return

        items_to_check = zip(type_args, value, strict=False) if origin is tuple else ((type_args[0], v) for v in value)
        for arg, val in items_to_check:
            _check_types(cls, attribute, arg, val, glbs, lcls)

    elif origin is dict:
        if not isinstance(value, dict):
            raise TypingError(cls, attribute, value, message=EXPECTED_INSTANCE_MESSAGE, expected_type="dict")

        key_type, value_type = get_args(_type)
        for k, v in value.items():
            _check_types(cls, attribute, key_type, k, glbs, lcls)
            _check_types(cls, attribute, value_type, v, glbs, lcls)

    elif not isinstance(value, _type):
        raise TypingError(cls, attribute, value, message=EXPECTED_INSTANCE_MESSAGE, expected_type=_type)


ObjT = TypeVar("ObjT", bound="BaseModel")


def _handle_obj_or_args(required_object: Any, obj: ObjT | None, args: tuple[tuple[str, Any, bool], ...]) -> ObjT:
    if obj:
        if not isinstance(obj, required_object):
            msg = f"Expected instance of {required_object!r} for 'obj', not {obj!r}."
            raise TypeError(msg)
        return obj

    missing_args = [name for name, value, required in args if required and not value]

    if missing_args:
        msg = (
            f"Expected either an instance of {required_object.__name__} for 'obj' "
            f"or the following required arguments: {', '.join(missing_args)}"
        )
        raise ValueError(
            msg,
        )

    return required_object(**{name: value for name, value, _ in args})


def _str_or_enum(_input: Any, enum: type[EnumT], param_name: str | None = None) -> EnumT:
    if isinstance(_input, enum):
        return _input

    if not isinstance(_input, str):
        msg = f"Expected {param_name or 'input'} to be a {enum.__name__} or a string, but got {type(_input).__name__}."
        raise TypeError(
            msg,
        )

    found = _try_enum(enum, _input)
    if not found:
        valid_values = _human_join([e.value for e in enum], last_sep=" or ")
        msg = f"Invalid value for {param_name or 'input'}: {_input!r}. Expected one of: {valid_values}."
        raise ValueError(msg)

    return found
