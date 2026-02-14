from somerandomapi import enums
from somerandomapi.internals.endpoints import (
    Animu,
    Base,
    CanvasFilter,
    Endpoint,
    EndpointWithAvatarParam,
    Parameter,
)


def test_endpoint_constructed_url_and_body_order() -> None:
    endpoint = Endpoint(
        "welcome",
        template=Parameter(index=1, is_body_parameter=True),
        background=Parameter(index=0, is_body_parameter=True),
        username=Parameter(required=False),
    )
    endpoint.parameters["template"].value = 7
    endpoint.parameters["background"].value = "stars"
    endpoint.parameters["username"].value = "soheab"
    assert endpoint.get_constructed_url() == "welcome/stars/7?username=soheab"


def test_set_param_values_and_missing_required() -> None:
    endpoint = Endpoint("x", avatar=Parameter(), optional=Parameter(required=False))
    configured = endpoint._set_param_values(None, avatar="https://a")
    assert configured.parameters["avatar"].value == "https://a"

    try:
        endpoint._set_param_values(None)
        raise AssertionError("expected TypeError")
    except TypeError as exc:
        assert "Missing required parameter avatar" in str(exc)


def test_base_endpoint_from_enum_validation() -> None:
    assert Animu.from_enum(enums.Animu.HUG).path.endswith("hug")

    try:
        Base.from_enum(enums.Animu.HUG)
        raise AssertionError("expected ValueError")
    except ValueError:
        pass

    try:
        Animu.from_enum("hug")
        raise AssertionError("expected TypeError")
    except TypeError:
        pass


def test_endpoint_with_avatar_param() -> None:
    endpoint = EndpointWithAvatarParam("hello")
    assert "avatar" in endpoint.parameters


def test_parameter_repr_and_property() -> None:
    p = Parameter(required=False, extra="x", index=2)
    p._name = "k"
    p.value = 10
    assert "k" in repr(p)
    assert p.value == 10


def test_endpoint_enums_map_paths() -> None:
    assert CanvasFilter.from_enum(enums.CanvasFilter.BLUE).path.endswith("blue")
