from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Self, dataclass_transform
from collections.abc import Iterable
from copy import deepcopy
import inspect
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
        data_name: str = _utils.NOVALUE,
        default: Any = _utils.NOVALUE,
        min_length: int = _utils.NOVALUE,
        max_length: int = _utils.NOVALUE,
        must_be_one_of: Iterable[str] = _utils.NOVALUE,
        in_range: tuple[int, int] = _utils.NOVALUE,
        init: bool = True,
        include_in_repr: bool = True,
        forced_type: type[Any] = _utils.NOVALUE,
        metadata: dict[str, Any] = _utils.NOVALUE,
    ) -> None:
        self._data_name: str = data_name
        self.name: str = ""

        self.default: Any = default
        self.min_length: int = min_length
        self.max_length: int = max_length
        self.must_be_one_of: Iterable[str] = must_be_one_of
        self.in_range: tuple[int, int] = in_range
        self.init: bool = init
        self.include_in_repr: bool = include_in_repr
        self.metadata: dict[str, Any] = metadata or {}
        self.forced_type: type[Any] = forced_type

        self._type: type[Any] = str
        self._value: Any = _utils.NOVALUE

        self._check_types: bool = True

    def __set_name__(self, _: type[Any], name: str) -> None:
        self.name = name

    def __get__(self, instance: BaseModel | None, _: type[Any] | None) -> Any:
        if instance is None:
            return self

        return instance._values.get(self.name, self.default)

    def __set__(self, instance: BaseModel, value: Any) -> None:
        if value in (None, _utils.NOVALUE):
            self._value = value
            return

        if self.forced_type is not _utils.NOVALUE:
            value = self.forced_type(value)

        if self._check_types:
            _utils._check_types(
                cls=self,
                attribute=self,
                value=value,
                _type=self.forced_type if self.forced_type is not _utils.NOVALUE else self._type,
                gls=globals(),
                lcs=locals(),
            )

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
        if self.in_range is not _utils.NOVALUE:
            if not isinstance(value, (int, float)):
                msg = f"{self.name!r} must be a number to validate range, got {type(value).__name__}"
                raise TypeError(msg)
            if not (self.in_range[0] <= value <= self.in_range[1]):
                msg = f"{self.name!r} must be in the range {self.in_range[0]} to {self.in_range[1]}, got {value!r}"
                raise ValueError(msg)

        instance._values[self.name] = value

    @property
    def data_name(self) -> str:
        return self._data_name or self.name

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
    in_range: tuple[int, int] = _utils.NOVALUE,
    init: bool = True,
    include_in_repr: bool = True,
    data_name: str = _utils.NOVALUE,
    metadata: dict[str, Any] = _utils.NOVALUE,
    forced_type: type[Any] = _utils.NOVALUE,
) -> Any:
    return Attribute(
        default=default,
        min_length=min_length,
        max_length=max_length,
        must_be_one_of=must_be_one_of,
        in_range=in_range,
        init=init,
        include_in_repr=include_in_repr,
        data_name=data_name,
        metadata=metadata,
        forced_type=forced_type,
    )


@dataclass_transform(kw_only_default=True, field_specifiers=(attribute,), frozen_default=False)
class BaseModelMeta(type):
    if TYPE_CHECKING:
        _attributes: dict[str, Attribute]
        _endpoint: Endpoint

        _frozen: bool
        _validate_types: bool

    __slots__ = ()

    def __new__(cls, name: str, bases: tuple[type[Any], ...], attrs: dict[str, Any], **options: Any) -> BaseModelMeta:
        possible_options: dict[str, Any] = {
            "frozen": False,
            "validate_types": True,
        }
        if options and not all(key in possible_options for key in options):
            msg = f"Invalid options: {', '.join(key for key in options if key not in possible_options)}"
            raise TypeError(msg)

        if not bases:
            return super().__new__(cls, name, bases, attrs)

        self = super().__new__(cls, name, bases, attrs)
        self._attributes = {}
        self._frozen = options.get("frozen", False)
        self._validate_types = options.get("validate_types", True)

        annotations = inspect.get_annotations(self, eval_str=True)
        for key, type_ in annotations.items():
            value = getattr(self, key, _utils.NOVALUE)
            if isinstance(value, Attribute):
                value.type = type_
                value._check_types = self._validate_types
                self._attributes[key] = value
            else:
                value = attribute(default=value)
                value.__set_name__(self, key)
                value._type = type_
                value._check_types = self._validate_types
                setattr(self, key, value)
                self._attributes[key] = value

        return self


class BaseModel(metaclass=BaseModelMeta):
    def __post_init__(self) -> None:
        self.validate_types()

    def __init__(self, **kwargs: Any) -> None:
        self._values: dict[str, Any] = {}

        attributes: dict[str, Attribute] = self._attributes
        init_attributes: int = sum(1 for attr in attributes.values() if attr.init)
        if len(kwargs) > init_attributes:
            msg = (
                f"Too many keyword arguments passed to {self.__class__.__name__}. "
                f"Expected {init_attributes}, got {len(kwargs)}"
            )
            raise TypeError(msg)

        required_arguments = [
            attr.name for attr in attributes.values() if attr.init and attr.required and attr.name not in kwargs
        ]
        if required_arguments:
            joined = _utils._human_join(map(repr, required_arguments))
            msg = f"Missing required keyword argument(s) {joined} for {self.__class__.__name__}"
            raise TypeError(msg)

        non_init_arguments = [attr.name for attr in attributes.values() if not attr.init and attr.name in kwargs]
        if non_init_arguments:
            joined = _utils._human_join(map(repr, non_init_arguments))
            msg = f"{joined} cannot be passed as keyword arguments by you."
            raise TypeError(msg)

        for attr_name, attribute in attributes.items():
            value = kwargs.pop(attr_name, _utils.NOVALUE)
            self._values[attr_name] = value if value is not _utils.NOVALUE else attribute.default

        required_arguments = _utils._human_join(
            [
                repr(attr.name)
                for attr in self._attributes.values()
                if attr.init and attr.required and attr.name not in kwargs
            ]
        )

        if kwargs:
            first = next(iter(kwargs))
            msg = f"{self.__class__.__name__} got an unexpected keyword argument {first!r}."
            raise TypeError(msg)

        self.__post_init__()

    def validate_types(self) -> None:
        """Validates the types of the attributes."""
        if not self._validate_types:
            return

        for attribute in self._attributes.values():
            if not attribute.init:
                continue

            if attribute._value is not _utils.NOVALUE:
                _utils._check_types(
                    cls=self, attribute=attribute, _type=attribute.type, value=attribute._value, gls=globals(), lcs=locals()
                )

    @recursive_repr()
    def __repr__(self) -> str:
        values: dict[str, Any] = {}
        for key, attribute in self._attributes.items():
            if attribute.init and attribute.include_in_repr:
                values[key] = self._values.get(key, attribute.default)

        attributes = ", ".join(f"{key}={value!r}" for key, value in values.items())
        return f"{self.__class__.__name__}({attributes})"

    def __delattr__(self, name: str) -> None:
        msg = f"Cannot delete attribute {name!r}"
        raise AttributeError(msg)

    @classmethod
    def _from_endpoint(cls: type[Self], endpoint: Any) -> Self:
        if not hasattr(cls, "_endpoint"):
            msg = f"{cls.__name__} does not have an endpoint attribute."
            raise TypeError(msg)

        if endpoint is not cls._endpoint:
            msg = f"Expected endpoint to be {cls._endpoint}, got {endpoint}"
            raise TypeError(msg)

        params_dict = {name: param.value for name, param in endpoint.parameters.items()}
        return cls.from_dict(**params_dict)

    def copy(self) -> Self:
        """Returns a deepcopy of this model."""
        return deepcopy(self)

    def to_dict(self) -> dict[str, Any]:
        result = {}
        for name, attr in self._attributes.items():
            value = self._values.get(name, _utils.NOVALUE)
            if value in (_utils.NOVALUE, None):
                value = attr.default
            else:
                value = value if attr.forced_type is _utils.NOVALUE else attr.forced_type(value)

            if value is not _utils.NOVALUE:
                flattened = value
                if flattened not in (_utils.NOVALUE, None):
                    flattened = flattened.value if isinstance(flattened, BaseEnum) else str(flattened)
                else:
                    flattened = attr.default

                if flattened is not _utils.NOVALUE:
                    result[attr.data_name] = flattened
        return result

    @classmethod
    def from_dict(cls: type[Self], data: dict[str, Any]) -> Self:
        kwrgs = {
            attribute.name: data.get(attribute.data_name, data.get(attribute.name, attribute.default))
            for attribute in cls._attributes.values()
            if attribute.init
        }
        return cls(**kwrgs)


class BaseImageModel(BaseModel, Image):
    _image: ClassVar[Image] = attribute(include_in_repr=False, init=False)

    def _set_image(self, image: Image) -> None:
        self._image = image  # pyright: ignore[reportAttributeAccessIssue]
        self._url = image._url
        self._http = image._http
