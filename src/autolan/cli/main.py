"""Entrypoint of CLI."""

import argparse

from autolan.__build__ import version as lib_version
from autolan.cli.dummy_cli import options as dummy_cli_options
from autolan.cli.telegram_bot import options as telegram_bot_cli_options
from autolan.cli.telegram_send import options as telegram_send_cli_options
from autolan.lib.cli import EnvDefault, log_options


def main():
    """Loads options and runs selected sub-command."""
    opt = options().parse_args()
    opt.func(opt)


def options():
    """Builds global options and sub-commands."""

    #
    # top-level command
    #

    parser = argparse.ArgumentParser(
        prog="autolan", description="Home LAN automation utilities."
    )
    subparsers = parser.add_subparsers(required=True, help="Commands:", dest="command")

    #
    # global options
    #

    parser.add_argument("--version", action="version", version=lib_version)
    log_options(parser)
    parser.add_argument(
        "--wkdir",
        type=str,
        default="local-data",
        required=True,
        action=EnvDefault,
        envvar="WKDIR",
        metavar="PATH",
        help="path to working directory",
    )

    #
    # sub-commands
    #
    dummy_cli_options(subparsers)
    telegram_bot_cli_options(subparsers)
    telegram_send_cli_options(subparsers)

    return parser


if __name__ == "__main__":
    main()
