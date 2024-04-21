import pytest

from autolan.lib.service.config_service import ConfigService


def test_config_service(config_service: ConfigService):
    test_dict = {
        "this_setting_does_not_exist": False,
        "slaves": [
            {
                "mac_address": "12:34:56:78:90:AB",
                "aliases": ["john"],
                "management_user": "homelanelf",
                "os_to_grub_option_map": {"ubuntu": 0},
            },
            {
                "mac_address": "AB:CD:EF:01:23:45",
                "aliases": ["jane", "doe"],
                "os_to_grub_option_map": {"windows": 1, "ubuntu": 2},
            },
        ],
    }
    config_service.load_from_dict(test_dict)

    assert config_service.slaves[0].mac_address == "12:34:56:78:90:AB"
    assert config_service.slaves[0].aliases == ["john"]
    assert config_service.slaves[0].management_user == "homelanelf"
    assert config_service.slaves[0].os_to_grub_option_map == {"ubuntu": 0}
    assert config_service.slaves[0].get_grub_option_for_os_name("windows") is None
    assert config_service.slaves[0].get_grub_option_for_os_name("ubuntu") == 0

    assert config_service.slaves[1].mac_address == "AB:CD:EF:01:23:45"
    assert config_service.slaves[1].aliases == ["jane", "doe"]
    assert config_service.slaves[1].os_to_grub_option_map == {"windows": 1, "ubuntu": 2}
    assert config_service.slaves[1].get_grub_option_for_os_name("windows") == 1
    assert config_service.slaves[1].get_grub_option_for_os_name("ubuntu") == 2

    assert config_service.get_slave_config_by_alias("john") == config_service.slaves[0]
    assert config_service.get_slave_config_by_alias("jane") == config_service.slaves[1]
    assert config_service.get_slave_config_by_alias("doe") == config_service.slaves[1]
    assert config_service.get_slave_config_by_alias("woot") is None

    test_dict = {
        "slaves": [
            {"mac_address": "12:34:56:78:90:AB123"},
        ]
    }

    with pytest.raises(Exception) as e:
        config_service.load_from_dict(test_dict)

    assert e.type == ValueError


def test_repeated_aliases(config_service: ConfigService):
    test_dict = {
        "this_setting_does_not_exist": False,
        "slaves": [
            {
                "mac_address": "12:34:56:78:90:AB",
                "aliases": ["john", "doe"],
                "management_user": "homelanelf",
                "os_to_grub_option_map": {"ubuntu": 0},
            },
            {
                "mac_address": "AB:CD:EF:01:23:45",
                "aliases": ["jane", "doe"],
                "os_to_grub_option_map": {"windows": 1, "ubuntu": 2},
            },
        ],
    }

    with pytest.raises(Exception) as e:
        config_service.load_from_dict(test_dict)

    assert e.type == ValueError
