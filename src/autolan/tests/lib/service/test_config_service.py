import pytest

from autolan.lib.service.config_service import ConfigService


def test_config_service(config_service: ConfigService):
    test_dict = {
        "this_setting_does_not_exist": False,
        "slaves": [
            {"mac_address": "12:34:56:78:90:AB"},
            {"mac_address": "AB:CD:EF:01:23:45"},
        ],
    }
    config_service.load_from_dict(test_dict)

    assert config_service.slaves[0].mac_address == "12:34:56:78:90:AB"
    assert config_service.slaves[1].mac_address == "AB:CD:EF:01:23:45"

    test_dict = {
        "slaves": [
            {"mac_address": "12:34:56:78:90:AB123"},
        ]
    }

    with pytest.raises(Exception) as e:
        config_service.load_from_dict(test_dict)

    assert e.type == ValueError
