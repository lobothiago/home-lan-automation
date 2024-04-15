import logging
import os
import sys
from typing import Any, List, Optional

# def setup_logging():
#     logging.basicConfig(
#         handlers=[logging.StreamHandler(sys.stdout)],
#         level=os.environ.get("LOG_LEVEL", "INFO"),
#         format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
#     )


def setup_logging(opt: Optional[Any] = None, log_id: Optional[str] = ""):
    """Setup CLI runtime logging.

    See `log_options` for option details.

    Args:
        opt: Selected CLI options.
        log_id: Log file identifier if not `--log_stdout`.

    """
    handlers: List[logging.Handler] = []

    # Before configuring logging, let's first clean up all current handlers that other libs might have added
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    if opt is None:
        logging.basicConfig(
            handlers=[logging.StreamHandler(sys.stdout)],
            level=os.environ.get("LOG_LEVEL", "INFO"),
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        )

    else:
        if opt.log_stdout:
            handlers.append(logging.StreamHandler(sys.stdout))

        else:
            log_dir = opt.log_prefix
            if not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)
            elif not os.path.isdir(log_dir):
                print("bad log prefix - already exists, not a directory")
                sys.exit(1)

            handlers.append(
                logging.FileHandler(
                    filename=os.path.join(log_dir, f"log-{log_id}.log"), mode="a"
                )
            )

        logging.basicConfig(
            handlers=handlers,
            level=getattr(logging, opt.log_level.upper(), None),
            format="%(asctime)s - %(levelname)s - %(processName)s - %(threadName)s - %(name)s - %(message)s",
        )
