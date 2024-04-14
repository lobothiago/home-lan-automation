import logging
import os
import sys


def setup_logging():
    logging.basicConfig(
        handlers=[logging.StreamHandler(sys.stdout)],
        level=os.environ.get("LOG_LEVEL", "INFO"),
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
