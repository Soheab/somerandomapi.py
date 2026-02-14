from somerandomapi.models.rgb import RGB


def test_rgb_model() -> None:
    model = RGB(r=1, g=2, b=3)
    assert model.as_tuple == (1, 2, 3)
    assert list(model) == [1, 2, 3]
    assert repr(model) == "rgb(1, 2, 3)"
    assert model.to_dict() == {"r": 1, "g": 2, "b": 3}

