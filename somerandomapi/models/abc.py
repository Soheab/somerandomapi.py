from __future__ import annotations
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Type

from dataclasses import dataclass
from copy import deepcopy

from .. import utils as _utils
from ..enums import BaseEnum

if TYPE_CHECKING:
    from typing_extensions import Self

    from ..internals.endpoints import BaseEndpoint


@dataclass
class BaseModel:
    _endpoint: ClassVar[BaseEndpoint]

    def __post_init__(self) -> None:
        for name, field in self.__dataclass_fields__.items():
            attr_value = getattr(self, name)
            if max_length := field.metadata.get("max_length"):
                if len(attr_value) > max_length:
                    raise ValueError(f"{name} must be less than {max_length} characters.")
            elif _range := field.metadata.get("range"):
                if not _range[0] <= attr_value <= _range[1]:
                    raise ValueError(f"{name} must be between {_range[0]} and {_range[1]}")
            elif must_be_one_of := field.metadata.get("must_be_one_of"):
                if not str(attr_value) not in must_be_one_of:
                    raise ValueError(f"{name} must be one of: {', '.join(must_be_one_of)}")
            elif literal := _utils._get_literal_type(field.type):
                _utils._check_literal_values(name, literal, attr_value)
            elif issubclass(field.type.__class__, BaseEnum):
                if attr_value is not field.type:
                    raise TypeError(f"Expected {name} to be {field.type}, got {attr_value}")

    @classmethod
    def _from_endpoint(cls: Type[Self], endpoint: BaseEndpoint) -> Self:
        if endpoint is not cls._endpoint:
            raise TypeError(f"Expected endpoint to be {cls._endpoint}, got {endpoint}")

        params_dict = {name: param.value for name, param in endpoint.value.parameters.items()}
        return cls.from_dict(**params_dict)

    def to_dict(self: Self) -> Dict[str, Any]:
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
        kwargs = {}
        original_kwargs = original_kwargs.copy()
        fields = cls.__dataclass_fields__
        if len(original_kwargs) != len(fields):
            raise TypeError(f"Expected {len(fields)} arguments, got {len(original_kwargs)}")

        for name, value in fields.items():
            _type = value.type
            alias = value.metadata.get("alias_of")

            if not value.default and any(x not in original_kwargs for x in (name, alias)):
                raise TypeError(f"Missing required argument {name}")

            kwarg_name = alias if alias in original_kwargs else name

            print("from dict type", name, _type)
            if issubclass(_type.__class__, BaseEnum):
                print("from dict enum", name, _type, original_kwargs[kwarg_name])

                kwargs[name] = _type(original_kwargs[kwarg_name])
            else:
                kwargs[name] = original_kwargs[kwarg_name]

        return cls(**kwargs)  # type: ignore

    def copy(self: Self) -> Self:
        """Returns a copy of this model."""
        return deepcopy(self)
