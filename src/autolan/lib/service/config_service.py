from typing import Any, Dict, List, Optional

import yaml

from autolan.lib.domain.config import AutoLANConfig


class ConfigService(AutoLANConfig):

    def __init__(self, settings_file_path: Optional[str] = None) -> None:
        self._config_dict: Dict[str, Any] = {}
        self._last_attrs: List[str] = []

        self._set_config_dict(self._config_dict)

        if settings_file_path is not None:
            self.load_from_path(settings_file_path)

    def _deserialize_config_dict(self):
        settings = AutoLANConfig.from_dict(self._config_dict)
        return settings

    def _set_config_dict(self, config_dict: Dict[str, Any]):
        self._config_dict = config_dict

        # Cleanup previously added attributes
        for attr in self._last_attrs:
            self.__delattr__(attr)

        self._last_attrs = []

        # Add new attributes
        settings = self._deserialize_config_dict()
        for attr, value in settings.__dict__.items():
            self.__setattr__(attr, value)

        # Store last attributes to pop later
        self._last_attrs = list(settings.__dict__.keys())

    def load_from_dict(self, settings_dictionary: Dict[str, Any]) -> None:
        # Default values are set here
        # config: Dict[str, Any] = {}
        # config_as_object: AutoLANConfig = Schema.load(config)
        # dumped_to_dict = Schema.dump(config_as_object)
        self._set_config_dict(settings_dictionary)

    def load_from_path(self, settings_file_path: str) -> None:
        with open(settings_file_path, "r") as f:
            settings_dictionary = yaml.safe_load(f)
            self.load_from_dict(settings_dictionary)
