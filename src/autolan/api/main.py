from falcon import App

from autolan.api.resources.health import HealthResource
from autolan.api.resources.slave_callback import SlaveCallbackResource
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
    slave_callback_resource = SlaveCallbackResource()

    app.add_route(f"{url_prefix}/health", resource_health)
    app.add_route(f"{url_prefix}/slave/callback", slave_callback_resource)

    return app
