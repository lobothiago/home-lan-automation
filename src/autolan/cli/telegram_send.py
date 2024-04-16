"""Sub-command: `split`"""

import logging
import os
import sys
from typing import Optional, Union

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

    target_user_id_from_settings = (
        config_service.telegram.default_alert_user_id
        if config_service.telegram is not None
        else None
    )

    target_user_id_from_opt = (
        opt.user_id
        if (isinstance(opt.user_id, str) or isinstance(opt.user_id, int))
        else None
    )

    target_user_id: Union[Optional[str], Optional[int]] = (
        target_user_id_from_opt or target_user_id_from_settings
    )

    if target_user_id is None:
        log.error(
            "No target_user_id is available. Add to settings file or pass it with --user_id."
        )
        return

    content = ""

    # If something was passed via opt, let's use it
    if opt.content is not None:
        content = opt.content

    # Otherwise, if there is data being piped in, let's use it
    elif not sys.stdin.isatty():
        for line in sys.stdin:
            content += line

        content = content.strip()

    if len(content) > 0:
        log.info(f"Will send `{content}` to `{target_user_id}`")
        sender.send(target_user_id, content)
    else:
        log.info("Will not send anything because message is empty.")


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
        required=False,
        type=int,
        help="Target Telegram user ID.",
        default=None,
    )

    parser.add_argument(
        "content",
        type=str,
        help="Content to send as Telegram message.",
        default=None,
        nargs="?",
    )

    output_options(parser)
