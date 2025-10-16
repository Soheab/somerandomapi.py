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
        default: Any = _utils.NOVALUE,
        min_length: int = _utils.NOVALUE,
        max_length: int = _utils.NOVALUE,
        must_be_one_of: Iterable[str] = _utils.NOVALUE,
        in_range: tuple[int, int] = _utils.NOVALUE,
        init: bool = True,
        include_in_repr: bool = True,
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
        self.in_range: tuple[int, int] = in_range
        self.init: bool = init
        self.include_in_repr: bool = include_in_repr
        self.metadata: dict[str, Any] = metadata or {}
        self.forced_type: type[Any] = forced_type

        self._type: type[Any] = str
        self._value: Any = _utils.NOVALUE

    @property
    def data_name(self) -> str:
        return self._data_name or self.name

    def _setname(self, name: str) -> None:
        self.name = name

    def set_value(self, value: Any, *, check_type: bool = False) -> None:
        if value in (None, _utils.NOVALUE):
            self._value = value
            return

        if self.forced_type is not _utils.NOVALUE:
            value = self.forced_type(value)

        if check_type:
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

        # Assign the validated value
        self._value = value

    def get_value(self) -> Any:
        if self._value in (_utils.NOVALUE, None):
            return self.default
        return self._value if self.forced_type is _utils.NOVALUE else self.forced_type(self._value)

    def _get_flatten_value(self) -> Any:
        if self._value in (_utils.NOVALUE, None):
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

    @type.setter  # noqa: A003
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
        _init_attributes: dict[str, Attribute]
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
        self._init_attributes = {}
        self._frozen = options.get("frozen", False)
        self._validate_types = options.get("validate_types", True)

        annotations = inspect.get_annotations(self, eval_str=True)
        for key, _type in annotations.items():
            if key.startswith("_"):
                continue

            value = getattr(self, key, _utils.NOVALUE)
            if isinstance(value, Attribute):
                value._setname(key)
                value.type = _type
                self._attributes[key] = value
            else:
                value = attribute(default=value)
                value._setname(key)
                value._type = _type
                attrs[key] = value
                self._attributes[key] = value

            if value.init:
                self._init_attributes[key] = value

        return self


class BaseModel(metaclass=BaseModelMeta):
    def __post_init__(self) -> None:
        self.validate_types()

    if not TYPE_CHECKING:

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            if args:
                first = self._attributes.get(next(iter(self._attributes)))
                if first and first.init:
                    msg = (
                        f"{self.__class__.__name__}() only accepts keyword arguments. "
                        f"Did you mean to pass {first.name!r} as a keyword argument?"
                    )
                else:
                    msg = f"{self.__class__.__name__}() only accepts keyword arguments."
                raise TypeError(msg)

            self.__initialise(**kwargs)
    else:
        def __init__(self, **kwargs: Any) -> None: ...

    def __initialise(self, **kwargs: Any) -> None:
        if len(kwargs) > len(self._init_attributes):
            msg = (
                f"Too many keyword arguments passed to {self.__class__.__name__}. "
                f"Expected {len(self._init_attributes)}, got {len(kwargs)}"
            )
            raise TypeError(msg)

        required_arguments = _utils._human_join([
            repr(attr.name)
            for attr in self._init_attributes.values()
            if attr.init and attr.required and attr.name not in kwargs
        ])
        for name, attribute in self._init_attributes.items():
            value = kwargs.pop(name, _utils.NOVALUE)
            if value is _utils.NOVALUE:
                if attribute.required:
                    msg = (
                        f"Missing required keyword argument(s) {required_arguments} "
                        f"for {self.__class__.__name__}()"
                    )

                    raise TypeError(msg)

                attribute.set_value(attribute.default)
            else:
                if not attribute.init:
                    msg = f"{name!r} cannot be passed as a keyword argument by you."
                    raise TypeError(msg)
                
                #if value is None and attribute.default is not None:
                #    msg = f"{name!r} cannot be None."
                #    raise TypeError(msg)


                attribute.set_value(value)

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

    if not TYPE_CHECKING:

        def __getattribute__(self, name: str) -> Any:
            attributes = object.__getattribute__(self, "_attributes")
            try:
                return attributes[name].get_value()
            except KeyError:
                return super().__getattribute__(name)

    @recursive_repr()
    def __repr__(self) -> str:
        attributes = ", ".join(
            f"{key}={attribute.get_value()!r}"
            for key, attribute in self._attributes.items()
            if attribute.init and attribute.include_in_repr
        )
        return f"{self.__class__.__name__}({attributes})"

    def __delattr__(self, name: str) -> None:
        msg = f"Cannot delete attribute {name!r}"
        raise AttributeError(msg)

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_"):
            super().__setattr__(name, value)
            return

        try:
            attribute = self._attributes[name]
        except KeyError:
            msg = f"{self.__class__.__name__} has no attribute {name!r}"
            raise AttributeError(msg) from None
        else:
            if self._frozen:
                msg = f"{self.__class__.__name__} is frozen and cannot be modified."
                raise AttributeError(msg)

            try:
                attribute.set_value(value, check_type=self._validate_types)
            except (TypeError, ValueError) as exc:
                from ..errors import TypingError  # noqa: PLC0415

                if not isinstance(exc, TypingError):
                    raise

                exc.args = (f"Error setting attribute {name!r} on {self.__class__.__name__}: {exc.error_message}",)
                raise

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
        return {
            attr.data_name: attr._get_flatten_value()
            for attr in self._attributes.values()
            if attr.get_value() is not _utils.NOVALUE
        }

    @classmethod
    def from_dict(cls: type[Self], data: dict[str, Any]) -> Self:
        kwrgs = {
            attribute.name: data.get(attribute.data_name, data.get(attribute.name, attribute.default))
            for attribute in cls._attributes.values()
            if not attribute.init
        }
        return cls(**kwrgs)


class BaseImageModel(BaseModel, Image):
    _image: ClassVar[Image] = attribute(include_in_repr=False, init=False)

    def _set_image(self, image: Image) -> None:
        self._image = image  # pyright: ignore[reportAttributeAccessIssue]
        self._url = image._url
        self._http = image._http
