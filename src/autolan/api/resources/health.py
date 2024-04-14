from enum import Enum


class Health(Enum):
    GOOD = 1
    DEGRADED = 2
    DOWN = 3


class HealthResource:

    def on_get(self, req, rsp):
        rsp.media = {"status": Health.GOOD.name}
