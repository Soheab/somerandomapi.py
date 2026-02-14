from __future__ import annotations

import pytest

from somerandomapi.models.abc import BaseModel, attribute


class Dummy(BaseModel):
    name: str
    age: int = attribute(in_range=(0, 130))
    nickname: str | None = None


def test_base_model_init_and_repr() -> None:
    model = Dummy(name="Soheab", age=22)
    assert model.name == "Soheab"
    assert model.age == 22
    assert "Dummy(" in repr(model)


def test_base_model_to_from_dict_and_copy() -> None:
    model = Dummy(name="Soheab", age=22, nickname="s")
    data = model.to_dict()
    assert data["name"] == "Soheab"
    restored = Dummy.from_dict(data)
    assert restored.nickname == "s"
    copied = model.copy()
    assert copied is not model
    assert copied.name == model.name


def test_base_model_validation_errors() -> None:
    with pytest.raises(TypeError):
        Dummy(name="Soheab")

    model = Dummy(name="Soheab", age=22)
    with pytest.raises(ValueError):
        model.age = 1000

    with pytest.raises(TypeError):
        model.age = "bad"  # type: ignore[assignment]
