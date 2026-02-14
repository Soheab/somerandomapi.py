import pytest

from somerandomapi.models.encoding import EncodeResult


def test_encode_result_model_roundtrip() -> None:
    model = EncodeResult(_type="ENCODE", name="BASE64", input="hello", text="aGVsbG8=")
    assert str(model) == "aGVsbG8="
    assert model.to_dict() == {"encode": "hello"}
    restored = EncodeResult.from_dict(_input="hello", _type="ENCODE", name="BASE64", text="aGVsbG8=")
    assert restored.name == "BASE64"


def test_encode_result_type_property_current_behavior() -> None:
    model = EncodeResult(_type="ENCODE", name="BASE64", input="hello", text="aGVsbG8=")
    with pytest.raises(ValueError):
        _ = model.type

