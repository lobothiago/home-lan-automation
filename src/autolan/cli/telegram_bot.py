"""Sub-command: `split`"""

import logging
import os

from autolan.bot.main import entrypoint
from autolan.lib.cli import output_options, setup_cli
from autolan.lib.service.config_service import ConfigService


def command(opt):
    """Sub-command."""
    log = logging.getLogger(__name__)

    start_time, start_time_str = setup_cli(opt)

    settings_file_path = os.environ.get("SETTINGS_FILE_PATH")
    config_service = ConfigService(settings_file_path=settings_file_path)

    log.info("Will call telegram bot entrypoint()")
    entrypoint(config_service)


def options(subparsers):
    """Sub-command options."""
    parser_desc = "Telegram Bot CLI invocator."

    parser = subparsers.add_parser(
        "telegram-bot",
        help=parser_desc,
        description=parser_desc,
    )
    parser.set_defaults(func=command)

    # parser.add_argument(
    #     "test",
    #     type=str,
    #     metavar="PATH",
    #     help="input to path of pdf",
    # )

    # parser.add_argument(
    #     "--somevar",
    #     required=False,
    #     type=int,
    #     help="some var",
    #     default=None,
    # )

    output_options(parser)
