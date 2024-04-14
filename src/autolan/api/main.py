from falcon import App

from autolan.api.resources.health import HealthResource
from autolan.lib.logging import setup_logging


def application(
    title="",
    url_prefix="",
):
    setup_logging()

    app = App(
        sink_before_static_route=False,
        cors_enable=True,
    )

    resource_health = HealthResource()

    app.add_route(f"{url_prefix}/health", resource_health)

    return app
