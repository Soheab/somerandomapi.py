from __future__ import annotations

from collections.abc import Iterable
import random
import re
from dataclasses import Field
from typing import Any, get_args, get_origin, Literal, Optional, Tuple, Type, TYPE_CHECKING, TypeVar, Union


if TYPE_CHECKING:
    from .enums import BaseEnum
    from .models.abc import BaseModel

__all__: Tuple[str, ...] = ()


# https://en.wikipedia.org/wiki/Sentinel_value
class _NOVALUE:
    __slots__ = ()

    def __eq__(self, other: Any) -> bool:
        return False

    def __bool__(self) -> bool:
        return False

    def __hash__(self) -> int:
        return 0

    def __repr__(self) -> Literal["..."]:
        return "..."


NOVALUE: Any = _NOVALUE()


EnumT = TypeVar("EnumT", bound="BaseEnum")


def _try_enum(enum: Type[EnumT], _input: Any) -> Optional[EnumT]:
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


def _gen_colour(numbers: Optional[int] = None) -> str:
    random_number = numbers or random.randint(0, 0xFFFFFF)
    hex_number = f"{random_number:06x}"
    return hex_number


def _check_colour_value(hex_input: Optional[Union[str, int]], param_name: Optional[str] = None) -> str:
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
                for color_name, color in zip(["red", "green", "blue"], [r, g, b])
                if not (0 <= color <= 255)
            )
            raise ValueError(
                f"RGB values out of range: {out_of_range}. Expected all values to be between 0 and 255 inclusive."
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
    if len(items) == 1:
        return items[0]

    return f"{sep.join(items[:-1])}{last_sep}{items[-1]}"


def _builin_types_from_str(_type: str) -> Optional[str]:
    if not isinstance(_type, str):
        return _type

    if _type.startswith("ClassVar["):
        _type = _type[9:-1]
    elif _type.startswith("typing."):
        _type = _type[6:]
    elif _type.startswith("typing_extensions."):
        _type = _type[18:]
    elif _type.startswith("collections.abc."):
        _type = _type[17:]

    return _type


def _get_literal_type(_type: Type, gs: dict[str, Any], lc: dict[str, Any]) -> Optional[Literal]:  # type: ignore
    if _type and isinstance(_type, str):
        _type = eval(_type, gs | globals(), lc | locals())

    origin = get_origin(_type)

    if origin is Literal:
        return _type  # type: ignore

    return None


def _check_literal_values(cls, field: Field, _type: type[Literal], values: Tuple[Any, ...]) -> None:  # type: ignore
    # this is here to prevent circular imports.
    from somerandomapi.errors import TypingError

    args = get_args(_type)
    # shouldn't happen.
    if len(args) < 1:
        raise TypeError("Expected more than one argument for Literal type")

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


def _is_optional(_type: Type) -> bool:
    return get_origin(_type) is Union and type(None) in get_args(_type)


def _get_type(_type: Type, gs: dict[str, Any], lc: dict[str, Any]) -> Tuple[Any, ...]:
    origin = get_origin(_type)
    _type = _builin_types_from_str(_type)  # type: ignore
    if literal := _get_literal_type(_type, gs, lc):
        return (literal,)
    elif origin is Union:
        if _is_optional(_type):
            return ([x for x in get_args(_type) if x is not type(None)][0],)

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
    cls, attribute: Any, _type: Type, value: Union[str, int, Any], gls: dict[str, Any], lcs: dict[str, Any]
) -> None:
    # this is here to prevent circular imports.
    from somerandomapi.errors import TypingError

    glbs = gls | globals()
    lcls = lcs | locals()

    if isinstance(_type, str):
        if _type.startswith("ClassVar["):
            _type = _type[9:-1]  # pyright: ignore[reportAssignmentType]
        elif _type.startswith("typing."):
            _type = _type[6:]  # pyright: ignore[reportAssignmentType]
        elif _type.startswith("typing_extensions."):
            _type = _type[18:]  # pyright: ignore[reportAssignmentType]
        elif _type.startswith("collections.abc."):
            _type = _type[17:]  # pyright: ignore[reportAssignmentType]

        _type = eval(_type, glbs, lcs)  # pyright: ignore[reportArgumentType]

    if value is None:
        return

    try:
        if isinstance(value, _type):
            return
    except TypeError:
        pass

    if literal := _get_literal_type(_type, glbs, lcls):
        _check_literal_values(cls, attribute, literal, (value,))  # type: ignore
        return

    origin = get_origin(_type)
    if origin is Union:
        if _is_optional(_type):
            if value is None:
                return
            _type = [x for x in get_args(_type) if x is not type(None)][0]
            _check_types(cls, attribute, _type, value, glbs, lcls)
            return

        args = get_args(_type)
        for arg in args:
            if get_origin(arg) is Literal:
                _check_literal_values(cls, attribute, arg, (value,))
                return

        for arg in args:
            try:
                _check_types(cls, attribute, arg, value, glbs, lcls)
                return
            except TypingError:
                pass

        raise TypingError(
            cls,
            attribute,
            value,
            message="expected instance of {valids}, not {field_value_type}.",
            valids=", ".join(map(str, args)),
        )

    elif origin is list:
        if not isinstance(value, list):
            raise TypingError(cls, attribute, value, message="expected instance of list, not {field_value_type}.")

        for val in value:
            _check_types(cls, attribute, get_args(_type)[0], val, glbs, lcls)

    elif origin is dict:
        if not isinstance(value, dict):
            raise TypingError(cls, attribute, value, message="expected instance of dict, not {field_value_type}.")

        for val in value.values():
            _check_types(cls, attribute, get_args(_type)[1], val, glbs, lcls)

    elif origin is tuple:
        if not isinstance(value, tuple):
            raise TypingError(cls, attribute, value, message="expected instance of tuple, not {field_value_type}.")

        for arg, val in zip(get_args(_type), value):
            _check_types(cls, attribute, arg, val, glbs, lcls)

    elif not isinstance(value, _type):
        raise TypingError(cls, attribute, value, message="expected instance of {field_type}, not {field_value_type}.")

    return


ObjT = TypeVar("ObjT", bound="BaseModel")


def _handle_obj_or_args(required_object: Any, obj: Optional[ObjT], args: Tuple[Tuple[str, Any, bool], ...]) -> ObjT:
    """Handle the obj argument or the required arguments.

    This checks whether the user has passed the correct object or the required arguments,
    and then returns the required object. Raises a TypeError or ValueError if the user
    has passed the wrong object or not passed the required arguments.

    Parameters
    ----------
    required_object: Any
        The required object to return.
    obj: Optional[ObjT]
        The object the user has passed.
    args: Tuple[Tuple[str, Any, bool], ...]
        The arguments to check for.
        In order: name, value, required.

    Raises
    ------
    TypeError
        The user has passed the wrong object.
    ValueError
        The user has not passed the required arguments.

    Returns
    -------
    ObjT
        The required object.
    """
    if obj:
        if not isinstance(obj, required_object):
            raise TypeError(f"Expected instance of {required_object!r} for 'obj', not {obj!r}.")
        return obj

    missing_args = [name for name, value, required in args if required and not value]

    if missing_args:
        raise ValueError(
            f"Expected either an instance of {required_object.__name__} for 'obj' or the following required arguments: {', '.join(missing_args)}"
        )

    return required_object(**{name: value for name, value, _ in args})
