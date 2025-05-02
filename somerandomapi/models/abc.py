from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Self, dataclass_transform
from collections.abc import Iterable
from copy import deepcopy
from reprlib import recursive_repr

from .. import utils as _utils
from ..enums import BaseEnum
from ..models.image import Image

if TYPE_CHECKING:
    from ..internals.endpoints import Endpoint

__all__ = ()


class Attribute:
    def __init__(
        self,
        *,
        default: Any = _utils.NOVALUE,
        min_length: int = _utils.NOVALUE,
        max_length: int = _utils.NOVALUE,
        must_be_one_of: Iterable[str] = _utils.NOVALUE,
        range_: tuple[int, int] = _utils.NOVALUE,
        init: bool = True,
        repr: bool = True,  # noqa: A002
        data_name: str = _utils.NOVALUE,
        forced_type: type[Any] = _utils.NOVALUE,
        metadata: dict[str, Any] = _utils.NOVALUE,
    ) -> None:
        self._data_name: str = data_name

        self.name: str = ""
        self.default: Any = default
        self.min_length: int = min_length
        self.max_length: int = max_length
        self.must_be_one_of: Iterable[str] = must_be_one_of
        self.range_: tuple[int, int] = range_
        self.init: bool = init
        self.repr: bool = repr
        self.metadata: dict[str, Any] = metadata or {}
        self.forced_type: type[Any] = forced_type

        self._type: type[Any] = str
        self._value: Any = _utils.NOVALUE

    @property
    def data_name(self) -> str:
        return self._data_name or self.name

    def __setname__(self, name: str) -> None:  # noqa: PLW3201
        self.name = name

    def set_value(self, value: Any) -> None:
        if self.forced_type is not _utils.NOVALUE:
            value = self.forced_type(value)

        if value in (None, _utils.NOVALUE):
            self._value = value
            return

        # Validate minimum length
        if self.min_length is not _utils.NOVALUE:
            if not hasattr(value, "__len__"):
                msg = f"{self.name!r} must have a length to validate, got {type(value).__name__}"
                raise TypeError(msg)
            if len(value) < self.min_length:
                msg = f"{self.name!r} must be at least {self.min_length} characters long, got {len(value)}"
                raise ValueError(msg)

        # Validate maximum length
        if self.max_length is not _utils.NOVALUE:
            if not hasattr(value, "__len__"):
                msg = f"{self.name!r} must have a length to validate, got {type(value).__name__}"
                raise TypeError(msg)
            if len(value) > self.max_length:
                msg = f"{self.name!r} must be at most {self.max_length} characters long, got {len(value)}"
                raise ValueError(msg)

        # Validate allowed values
        if self.must_be_one_of is not _utils.NOVALUE and str(value) not in self.must_be_one_of:
            allowed_values = ", ".join(map(repr, self.must_be_one_of))
            msg = f"{self.name!r} must be one of {allowed_values}, got {value!r}"
            raise ValueError(msg)

        # Validate range
        if self.range_ is not _utils.NOVALUE:
            if not isinstance(value, (int, float)):
                msg = f"{self.name!r} must be a number to validate range, got {type(value).__name__}"
                raise TypeError(msg)
            if not (self.range_[0] <= value <= self.range_[1]):
                msg = f"{self.name!r} must be in the range {self.range_[0]} to {self.range_[1]}, got {value!r}"
                raise ValueError(msg)

        # Assign the validated value
        self._value = value

    def get_value(self) -> Any:
        if self._value is _utils.NOVALUE:
            return self.default
        return self._value if self.forced_type is _utils.NOVALUE else self.forced_type(self._value)

    def _get_flatten_value(self) -> Any:
        if self._value is _utils.NOVALUE:
            return self.default

        if isinstance(self._value, BaseEnum):
            return self._value.value

        return str(self._value)

    @property
    def required(self) -> bool:
        return self.default is _utils.NOVALUE

    @property
    def type(self) -> type[Any]:
        return self._type if self.forced_type is _utils.NOVALUE else self.forced_type

    @type.setter
    def type(self, value: type[Any]) -> None:
        if self.forced_type is not _utils.NOVALUE:
            return

        self._type = _utils._get_type(value, globals(), locals())[0]


def attribute(
    *,
    default: Any = _utils.NOVALUE,
    min_length: int = _utils.NOVALUE,
    max_length: int = _utils.NOVALUE,
    must_be_one_of: Iterable[str] = _utils.NOVALUE,
    range: tuple[int, int] = _utils.NOVALUE,  # noqa: A002
    init: bool = True,
    repr: bool = True,  # noqa: A002
    data_name: str = _utils.NOVALUE,
    metadata: dict[str, Any] = _utils.NOVALUE,
    forced_type: type[Any] = _utils.NOVALUE,
) -> Any:
    return Attribute(
        default=default,
        min_length=min_length,
        max_length=max_length,
        must_be_one_of=must_be_one_of,
        range_=range,
        init=init,
        repr=repr,
        data_name=data_name,
        metadata=metadata,
        forced_type=forced_type,
    )


@dataclass_transform(kw_only_default=True, field_specifiers=(attribute,), frozen_default=False)
class BaseModelMeta(type):
    __attributes__: dict[str, Attribute]
    __init_attributes__: dict[str, Attribute]
    __endpoint__: Endpoint
    __reserved_attributes__: set[str] = {"__attributes__", "__reserved_attributes__", "__endpoint__"}  # noqa: RUF012
    __possible_options__: dict[str, Any] = {  # noqa: RUF012
        "frozen": False,
        "validate_types": True,
    }

    __frozen__: bool
    __validate_types__: bool

    def __new__(cls, name: str, bases: tuple[type[Any], ...], attrs: dict[str, Any], **options: Any) -> BaseModelMeta:
        if options and not all(key in cls.__possible_options__ for key in options):
            msg = f"Invalid options: {', '.join(key for key in options if key not in cls.__possible_options__)}"
            raise TypeError(msg)

        if not bases:
            return super().__new__(cls, name, bases, attrs)

        self = super().__new__(cls, name, bases, attrs)
        self.__attributes__ = {}
        self.__init_attributes__ = {}
        self.__reserved_attributes__ = cls.__reserved_attributes__.copy()
        self.__frozen__ = options.get("frozen", False)
        self.__validate_types__ = options.get("validate_types", True)

        annotations = self.__annotations__
        for key, _type in annotations.items():
            if key in self.__reserved_attributes__:
                continue

            value = getattr(self, key, _utils.NOVALUE)
            if isinstance(value, Attribute):
                value.__setname__(key)
                value.type = _type
                self.__attributes__[key] = value
            elif not key.startswith("__"):
                value = attribute(default=value)
                value.__setname__(key)
                value._type = _type
                attrs[key] = value
                self.__attributes__[key] = value

            if value.init:
                self.__init_attributes__[key] = value

        return self


class BaseModel(metaclass=BaseModelMeta):
    def __post_init__(self) -> None:
        self.validate_types()

    def __init__(self, **kwargs: Any) -> None:
        if len(kwargs) > len(self.__init_attributes__):
            msg = (
                f"Too many keyword arguments passed to {self.__class__.__name__}. "
                f"Expected {len(self.__init_attributes__)}, got {len(kwargs)}"
            )
            raise TypeError(msg)

        # fmt: off
        for name, attribute in self.__init_attributes__.items():
            value = kwargs.pop(name, _utils.NOVALUE)
            if value is _utils.NOVALUE:
                if attribute.required:
                    msg = f"Missing required parameter {name!r} for {self.__class__.__name__}"
                    raise TypeError(
                        msg
                    )

                attribute.set_value(attribute.default)
            else:
                if not attribute.init:
                    msg = f"{name!r} cannot be passed as a keyword argument by you."
                    raise TypeError(
                        msg
                    )

                attribute.set_value(value)

        if kwargs:
            first = next(iter(kwargs))
            msg = f"{self.__class__.__name__} got an unexpected keyword argument {first!r}."
            raise TypeError(
                msg
            )

        # fmt: on

        self.__post_init__()

    def validate_types(self) -> None:
        """Validates the types of the attributes."""
        if not self.__validate_types__:
            return

        for attribute in self.__attributes__.values():
            if not attribute.init:
                continue

            if attribute._value is not _utils.NOVALUE:
                _utils._check_types(
                    cls=self, attribute=attribute, _type=attribute.type, value=attribute._value, gls=globals(), lcs=locals()
                )

    def __getattribute__(self, name: str) -> Any:
        attributes = object.__getattribute__(self, "__attributes__")
        try:
            return attributes[name].get_value()
        except KeyError:
            return super().__getattribute__(name)

    @recursive_repr()
    def __repr__(self) -> str:
        attributes = ", ".join(
            f"{key}={attribute.get_value()!r}"
            for key, attribute in self.__attributes__.items()
            if attribute.init and attribute.repr
        )
        return f"{self.__class__.__name__}({attributes})"

    def __delattr__(self, name: str) -> None:
        msg = f"Cannot delete attribute {name!r}"
        raise AttributeError(msg)

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_"):
            super().__setattr__(name, value)
            return

        if name in self.__reserved_attributes__:
            msg = f"{name!r} is a reserved attribute and cannot be set."
            raise AttributeError(msg)

        try:
            attribute = self.__attributes__[name]
        except KeyError:
            msg = f"{self.__class__.__name__} has no attribute {name!r}"
            raise AttributeError(msg) from None
        else:
            if self.__frozen__:
                msg = f"{self.__class__.__name__} is frozen and cannot be modified."
                raise AttributeError(msg)

            attribute.set_value(value)

    @classmethod
    def _from_endpoint(cls: type[Self], endpoint: Any) -> Self:
        if not hasattr(cls, "__endpoint__"):
            msg = f"{cls.__name__} does not have an endpoint attribute."
            raise TypeError(msg)

        if endpoint is not cls.__endpoint__:
            msg = f"Expected endpoint to be {cls.__endpoint__}, got {endpoint}"
            raise TypeError(msg)

        params_dict = {name: param.value for name, param in endpoint.parameters.items()}
        return cls.from_dict(**params_dict)

    def copy(self) -> Self:
        """Returns a deepcopy of this model."""
        return deepcopy(self)

    def to_dict(self) -> dict[str, Any]:
        result = {}
        for attribute in self.__attributes__.values():
            if not attribute.init:
                continue

            result[attribute.data_name] = attribute._get_flatten_value()
        return result

    @classmethod
    def from_dict(cls: type[Self], data: dict[str, Any]) -> Self:
        kwrgs = {}
        for attribute in cls.__attributes__.values():
            if not attribute.init:
                continue

            kwrgs[attribute.data_name] = data.get(attribute.data_name, attribute.default)

        return cls(**kwrgs)


class BaseImageModel(BaseModel, Image):
    _image: ClassVar[Image] = attribute(repr=False, init=False)

    def _set_image(self, image: Image) -> None:
        self._image = image  # pyright: ignore[reportAttributeAccessIssue]
        self._url = image._url
        self._http = image._http
