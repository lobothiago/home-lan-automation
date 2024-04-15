import argparse

from autolan.lib.cli.env_default import EnvDefault


def log_options(parser: argparse.ArgumentParser):
    """Adds standard logging options to `parser`.

    * **`--log_level`** `DEBUG`, `INFO`, etc.
    * **`--log_prefix`** log to directory/prefix
    * **`--log_stdout`** log to stdout.

    `--log_prefix` and `log_stdout` are mutually exclusive.

    Args:
        parser: To add options to.

    """
    parser.add_argument(
        "--log_level",
        type=str,
        default="INFO",
        required=True,
        action=EnvDefault,
        envvar="LOG_LEVEL",
        metavar="LEVEL",
        help="log level - DEBUG, INFO, WARNING, etc.",
    )
    outputs = parser.add_mutually_exclusive_group()
    outputs.add_argument("--log_stdout", action="store_true", help="log to 'stdout'")
    outputs.add_argument(
        "--log_prefix",
        type=str,
        default="log",
        required=True,
        action=EnvDefault,
        envvar="LOG_PREFIX",
        metavar="PREFIX",
        help="log directory",
    )
