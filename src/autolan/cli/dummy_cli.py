"""Sub-command: `split`"""

import logging
import os

from autolan.lib.cli import output_options, setup_cli
from autolan.lib.service.config_service import ConfigService


def command(opt):
    """Sub-command."""
    log = logging.getLogger(__name__)

    start_time, start_time_str = setup_cli(opt)

    settings_file_path = os.environ.get("SETTINGS_FILE_PATH")
    config_service = ConfigService(settings_file_path=settings_file_path)

    log.info(f"Hello CLI! {settings_file_path}")
    log.info(f"{config_service.slaves}")


def options(subparsers):
    """Sub-command options."""
    parser_desc = "Dummy CLI tool."

    parser = subparsers.add_parser(
        "dummy-cli",
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
