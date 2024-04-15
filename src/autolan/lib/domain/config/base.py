import os
from typing import Optional

from marshmallow import EXCLUDE


class BaseConfig:
    class Meta:
        unknown = EXCLUDE

    def __getitem__(self, key):
        return getattr(self, key)

    def get(self, key, default=None):
        return getattr(self, key, default)


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
