from dataclasses import field
from typing import Any, Dict, List, Optional, Set, Union, cast

from marshmallow_dataclass import dataclass

from autolan.lib.domain.config.base import BaseConfig
from autolan.lib.util.wake_on_lan import is_mac_address


@dataclass
class SlaveConfig(BaseConfig):

    mac_address: str
    management_user: Optional[str]
    aliases: List[str] = field(default_factory=list)
    os_to_grub_option_map: Dict[str, int] = field(default_factory=lambda: {})

    def __post_init__(self) -> None:
        if not is_mac_address(self.mac_address):
            raise ValueError(f"mac_address `{self.mac_address}` is invalid!")

    def get_grub_option_for_os_name(self, os_name: str) -> Optional[int]:
        return self.os_to_grub_option_map.get(os_name, None)


@dataclass
class TelegramConfig(BaseConfig):

    api_key: str
    default_alert_user_id: Union[Optional[int], Optional[str]]


@dataclass
class AutoLANConfig(BaseConfig):

    telegram: Optional[TelegramConfig]
    slaves: List[SlaveConfig] = field(default_factory=lambda: [])

    def __post_init__(self):
        new_slaves: List[SlaveConfig] = []

        # Initialize SlaveConfigs
        for slave in self.slaves:
            new_slaves.append(
                slave
                if isinstance(slave, SlaveConfig)
                else SlaveConfig.from_dict(**cast(Dict[str, Any], slave))
            )

        self.slaves = new_slaves

        # Verify that all aliases are unique
        aliases_memoization: Set[str] = set()

        for slave in self.slaves:
            aliases_set = set(slave.aliases)

            if len(aliases_memoization.intersection(aliases_set)) > 0:
                raise ValueError(
                    f"At least one of the aliases in `{slave.aliases}` have been used in another SlaveConfig"
                )

            aliases_memoization.update(slave.aliases)

        # Initialize TelegramConfig
        if isinstance(self.telegram, dict):
            self.telegram = TelegramConfig.from_dict(
                **cast(Dict[str, Any], self.telegram)
            )

    def get_slave_config_by_alias(self, alias: str) -> Optional[SlaveConfig]:
        for slave in self.slaves:
            if alias in slave.aliases:
                return slave

        return None
