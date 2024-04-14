import pytest
from falcon import testing

from autolan.api.main import application


@pytest.fixture(scope="module")
def client() -> testing.TestClient:
    return testing.TestClient(
        application(url_prefix=""),
    )
