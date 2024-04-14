import logging


class Loggable:
    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
