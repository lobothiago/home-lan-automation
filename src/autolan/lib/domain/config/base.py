import logging
import os
from dataclasses import asdict, dataclass
from typing import Any, ClassVar, Dict, Optional, Type, TypeVar

from marshmallow import EXCLUDE, Schema
from marshmallow_dataclass import class_schema

T = TypeVar("T", bound="BaseConfig")


@dataclass
class BaseConfig:
    class Meta:
        unknown = EXCLUDE

    _SCHEMA: ClassVar[Optional[Schema]] = None

    def __getitem__(self, key):
        return getattr(self, key)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def keys(self):
        log = logging.getLogger(__name__)

        properties = {}

        try:
            properties = self.find_properties()
        except Exception as e:
            log.exception("Couldn't get properties", exc_info=e)

        result = {**properties, **asdict(self)}

        return iter(result.keys())

    def find_properties(self):
        properties = {}
        # Iterate over all attributes of the class
        for name in dir(self):
            # Get the attribute
            attr = getattr(self.__class__, name, None)
            # Check if the attribute is a property
            if isinstance(attr, property):
                # Get the value of the property
                properties[name] = getattr(self, name)

        return properties

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        if cls._SCHEMA is None:
            cls._SCHEMA = class_schema(cls)()

        return cls._SCHEMA.load(data)


class FetchableAsEnvVarStr:

    _ENV_VAR_PREFIX = "env::"

    def __init__(self, default: Optional[str] = None):
        self.default = default

    def __set_name__(self, _, name: str):
        self.hidden_field_name = "_" + name

    def __get__(self, instance, _) -> Optional[str]:
        return getattr(instance, self.hidden_field_name, self.default)

    def __set__(self, instance, value: str):
        if isinstance(value, str):

            # When setting the env var, if it's a string, we check if it's a reference to an env var
            if value.startswith(self._ENV_VAR_PREFIX):
                env_var_name = value[len(self._ENV_VAR_PREFIX) :]
                # If no env var is found, we return the value itself
                value = os.environ.get(env_var_name, value)

            setattr(instance, self.hidden_field_name, value)
