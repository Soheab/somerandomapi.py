from typing import Literal, Union
import asyncio
from dataclasses import dataclass

import pytest

from somerandomapi import enums
from somerandomapi.models.tweet import Tweet
from somerandomapi.utils import (
    NOVALUE,
    _builin_types_from_str,
    _check_colour_value,
    _gen_colour,
    _get_literal_type,
    _get_type,
    _handle_obj_or_args,
    _human_join,
    _is_optional,
    _str_or_enum,
    _try_enum,
)


def test_novalue_basics() -> None:
    assert not NOVALUE
    assert repr(NOVALUE) == "..."
    assert hash(NOVALUE) == 0
    assert object() != NOVALUE


def test_try_enum_resolves_by_name_value_instance() -> None:
    assert _try_enum(enums.Animu, "hug") is enums.Animu.HUG
    assert _try_enum(enums.Animu, "HUG") is enums.Animu.HUG
    assert _try_enum(enums.Animu, enums.Animu.HUG) is enums.Animu.HUG
    assert _try_enum(enums.Animu, "nope") is None
    assert _try_enum(enums.Animu, None) is None


def test_gen_colour_and_check_colour_value_paths() -> None:
    assert _gen_colour(255) == "0000ff"
    assert _check_colour_value("#abcdef") == "abcdef"
    assert _check_colour_value("rgb(255, 0, 1)") == "ff0001"
    assert _check_colour_value(16711680) == "ff0000"


@pytest.mark.parametrize("value", ["rgb(256, 0, 0)", "not-a-color"])
def test_check_colour_value_invalid(value: str) -> None:
    with pytest.raises(ValueError):
        _check_colour_value(value, "color")


def test_human_join_variants() -> None:
    assert not _human_join([])
    assert _human_join(["a"]) == "a"
    assert _human_join(["a", "b", "c"]) == "a, b and c"


def test_builtin_types_from_str() -> None:
    assert _builin_types_from_str("typing.Any") == "Any"
    assert _builin_types_from_str("typing_extensions.Literal") == "Literal"
    assert _builin_types_from_str("collections.abc.Iterable") == "Iterable"
    assert _builin_types_from_str("ClassVar[int]") == "int"


def test_literal_optional_and_get_type() -> None:
    lit = _get_literal_type(Literal["a", "b"], {}, {})
    assert lit is not None
    assert _is_optional(Union[int, None])
    assert _get_type(list[int], {}, {}) == (int,)
    assert _get_type(dict[str, int], {}, {}) == (int,)
    assert _get_type(tuple[int, str], {}, {}) == (int, str)


@dataclass
class _Dummy:
    foo: str | None
    bar: int | None = None


def test_handle_obj_or_args() -> None:
    obj = _Dummy("x", 1)
    same = _handle_obj_or_args(_Dummy, obj, (("foo", "unused", True),))
    assert same is obj

    built = _handle_obj_or_args(_Dummy, None, (("foo", "abc", True), ("bar", 2, False)))
    assert isinstance(built, _Dummy)
    assert built.foo == "abc"

    with pytest.raises(ValueError):
        _handle_obj_or_args(_Dummy, None, (("foo", "", True),))


def test_str_or_enum_success_and_failures() -> None:
    assert _str_or_enum("light", enums.TweetTheme) is enums.TweetTheme.LIGHT
    assert _str_or_enum(enums.TweetTheme.DARK, enums.TweetTheme) is enums.TweetTheme.DARK

    with pytest.raises(TypeError):
        _str_or_enum(123, enums.TweetTheme, "theme")

    with pytest.raises(ValueError):
        _str_or_enum("bad", enums.TweetTheme, "theme")


def test_runtime_type_check_on_model() -> None:
    ok = Tweet(display_name="x", username="abc", avatar_url="https://x", text="ok")
    with pytest.raises(TypeError):
        ok.username = 123
    assert ok.username == "abc"
