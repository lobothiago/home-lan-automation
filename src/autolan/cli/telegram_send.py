"""Sub-command: `split`"""

import logging
import os

from autolan.bot.send import TelegramMessageSender
from autolan.lib.cli import output_options, setup_cli
from autolan.lib.service.config_service import ConfigService


def command(opt):
    """Sub-command."""
    log = logging.getLogger(__name__)

    start_time, start_time_str = setup_cli(opt)

    settings_file_path = os.environ.get("SETTINGS_FILE_PATH")
    config_service = ConfigService(settings_file_path=settings_file_path)
    sender = TelegramMessageSender(config_service)

    log.info(f"Will send `{opt.content}` to `{opt.user_id}`")
    sender.send(opt.user_id, opt.content)


def options(subparsers):
    """Sub-command options."""
    parser_desc = "Sends message to specific user via telegram bot."

    parser = subparsers.add_parser(
        "telegram-send",
        help=parser_desc,
        description=parser_desc,
    )
    parser.set_defaults(func=command)

    parser.add_argument(
        "--user_id",
        required=True,
        type=int,
        help="Target Telegram user ID.",
    )

    parser.add_argument(
        "content",
        type=str,
        help="Content to send as Telegram message.",
    )

    output_options(parser)
