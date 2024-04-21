import logging

from falcon.request import Request
from falcon.response import Response
from falcon.status_codes import HTTP_OK


class SlaveCallbackResource:

    def on_get(self, req: Request, rsp: Response):
        log = logging.getLogger(__name__)

        log.info("Received callback!")

        rsp.status = HTTP_OK
