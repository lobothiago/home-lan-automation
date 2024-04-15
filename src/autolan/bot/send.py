import logging

import async_to_sync as sync
from telegram.ext import Application

from autolan.lib.service.config_service import ConfigService


class TelegramMessageSender:

    def __init__(self, config_service: ConfigService) -> None:
        self._config_service = config_service

        if self._config_service.telegram is None:
            raise ValueError("`telegram` is missing in loaded settings!")

        logging.getLogger("httpx").setLevel(logging.WARNING)

        # Create the Application and pass it your bot's token.
        self._application = (
            Application.builder().token(self._config_service.telegram.api_key).build()
        )

    def send(self, user_id: str, message: str) -> None:
        async def _send():
            await self._application.bot.send_message(user_id, message)

        sync.coroutine(_send())
