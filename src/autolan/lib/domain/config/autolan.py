from dataclasses import field
from typing import Any, Dict, List, Optional, cast

from marshmallow_dataclass import class_schema, dataclass

from autolan.lib.domain.config.base import BaseConfig
from autolan.lib.util.wake_on_lan import is_mac_address


@dataclass
class SlaveConfig(BaseConfig):

    mac_address: str

    def __post_init__(self) -> None:
        if not is_mac_address(self.mac_address):
            raise ValueError(f"mac_address `{self.mac_address}` is invalid!")


@dataclass
class TelegramConfig(BaseConfig):

    api_key: str


@dataclass
class AutoLANConfig(BaseConfig):

    telegram: Optional[TelegramConfig]
    slaves: List[SlaveConfig] = field(default_factory=lambda: [])

    def __post_init__(self):
        new_slaves: List[SlaveConfig] = []

        for slave in self.slaves:
            new_slaves.append(
                slave
                if isinstance(slave, SlaveConfig)
                else SlaveConfig(**cast(Dict[str, Any], slave))
            )

        self.slaves = new_slaves

        if isinstance(self.telegram, dict):
            self.telegram = TelegramConfig(**cast(Dict[str, Any], self.telegram))


Schema = class_schema(AutoLANConfig)()
