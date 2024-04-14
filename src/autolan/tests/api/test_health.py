from falcon import HTTP_OK

from autolan.api.resources.health import Health


def test_health(client):
    rsp = client.simulate_get("/health")
    assert rsp.status == HTTP_OK

    data = rsp.json
    assert data

    assert "status" in data and data["status"] == Health.GOOD.name
