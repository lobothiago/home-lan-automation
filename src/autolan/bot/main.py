import logging

from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from autolan.lib.service.config_service import ConfigService


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user

    if update.message is not None and user is not None:
        await update.message.reply_html(
            rf"Hi {user.mention_html()} {user.id} {user.username}!",
            reply_markup=ForceReply(selective=True),
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    if update.message is not None:
        await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    if update.message is not None and update.message.text is not None:
        await update.message.reply_text(update.message.text)


def entrypoint(config_service: ConfigService) -> None:
    """Start the bot."""
    if config_service.telegram is None:
        raise ValueError("`telegram` is missing in loaded settings!")

    logging.getLogger("httpx").setLevel(logging.WARNING)

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(config_service.telegram.api_key).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
