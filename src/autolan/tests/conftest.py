import pytest
from falcon import testing

from autolan.api.main import application
from autolan.lib.service.config_service import ConfigService


@pytest.fixture(scope="module")
def client() -> testing.TestClient:
    return testing.TestClient(
        application(url_prefix=""),
    )


@pytest.fixture
def config_service() -> ConfigService:
    return ConfigService()
