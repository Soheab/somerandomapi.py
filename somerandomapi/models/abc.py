from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, Field, field, fields, MISSING
from typing import Any, ClassVar, Type, TYPE_CHECKING

from somerandomapi.errors import TypingError
from somerandomapi.models.image import Image

from .. import utils as _utils
from ..enums import BaseEnum


if TYPE_CHECKING:
    from typing_extensions import Self

    from ..internals.endpoints import BaseEndpoint

__all__ = ()


@dataclass
class BaseModel:
    _endpoint: ClassVar[BaseEndpoint]

    def _validate_types(self, lcs: dict[str, Any], glbs: dict[str, Any]) -> None:
        # issubclass throws a TypeError if the first argument is not a class
        def is_enum(field: Field):
            try:
                return issubclass(field.type, BaseEnum)
            except TypeError:
                return False

        for field in fields(self):
            name = field.name
            attr_value = getattr(self, name, None)

            if not attr_value or str(field.type).startswith("ClassVar["):
                continue
            if min_length := field.metadata.get("min_length"):
                if len(str(attr_value)) < min_length:
                    raise TypingError(
                        self,
                        field,
                        attr_value,
                        message="{field_name} must be more than {min_length} characters.",
                        min_length=min_length,
                    )
            elif max_length := field.metadata.get("max_length"):
                if len(str(attr_value)) > max_length:
                    raise TypingError(
                        self,
                        field,
                        attr_value,
                        message="{field_name} must be less than {max_length} characters.",
                        max_length=max_length,
                    )
            elif length := field.metadata.get("length"):
                if len(str(attr_value)) != length:
                    raise TypingError(
                        self,
                        field,
                        attr_value,
                        message="{field_name} must be exactly {length} characters.",
                        length=length,
                    )
            elif must_be_one_of := field.metadata.get("must_be_one_of"):
                if not str(attr_value) not in must_be_one_of:
                    raise TypingError(
                        self,
                        field,
                        attr_value,
                        message="{field_name} must be one of: {must_be_one_of}",
                        one_of=must_be_one_of,
                    )
            elif _range := field.metadata.get("range"):
                if not isinstance(attr_value, int):
                    raise TypingError(self, field, attr_value)
                if not _range[0] <= attr_value <= _range[1]:
                    raise TypingError(
                        self,
                        field,
                        attr_value,
                        message="{field_name} must be a number between {_range[0]} and {_range[1]}",
                        _range=_range,
                    )
            elif is_enum(field):
                if not isinstance(attr_value, field.type):
                    raise TypingError(
                        self,
                        field,
                        attr_value,
                        message="Expected {field_name} to be an enum of {enum_type}, got {field_value_type}.",
                        enum_type=field.type.__name__,
                    )

            _utils._check_types(self, field, field.type, attr_value, glbs, lcs)

    @classmethod
    def _from_endpoint(cls: Type[Self], endpoint: BaseEndpoint) -> Self:
        if endpoint is not cls._endpoint:
            raise TypeError(f"Expected endpoint to be {cls._endpoint}, got {endpoint}")

        params_dict = {name: param.value for name, param in endpoint.value.parameters.items()}
        return cls.from_dict(**params_dict)

    def to_dict(self: Self) -> dict[str, Any]:
        """Converts this model to a dictionary."""
        base = {}
        for name, field in self.__dataclass_fields__.items():
            if name.startswith("_"):
                continue

            alias = field.metadata.get("alias_of")
            base[alias or name] = getattr(self, name)
        return base

    @classmethod
    def from_dict(cls: Type[Self], **original_kwargs: Any) -> Self:
        """Converts a dictionary to this model."""
        reserved_attrs = ("_endpoint",)
        kwargs = {}
        original_kwargs = original_kwargs.copy()
        fields = cls.__dataclass_fields__.copy()
        for name, value in fields.items():
            if name in reserved_attrs:
                continue

            alias = value.metadata.get("alias_of")

            if value.default is MISSING and not any(key in original_kwargs for key in (name, alias)):
                if name.startswith("_") and name[1:] in original_kwargs:
                    kwargs[name] = original_kwargs[name[1:]]
                    continue
                raise TypeError(f"Missing required argument: {name}")

            _type = value.type
            kwarg_name = alias if alias in original_kwargs else name

            if issubclass(_type.__class__, BaseEnum):
                kwargs[name] = _type(original_kwargs[kwarg_name])
            else:
                kwargs[name] = original_kwargs[kwarg_name]

        return cls(**kwargs)

    def copy(self: Self) -> Self:
        """Returns a copy of this model."""
        return deepcopy(self)


@dataclass
class BaseImageModel(BaseModel, Image):
    _image: ClassVar[Image] = field(repr=False, init=False)

    def _set_image(self, image: Image) -> None:
        self._image = image  # type: ignore
        self._url = image._url
        self._http = image._http
