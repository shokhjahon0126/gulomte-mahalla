import logging
from decouple import config
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters
from apps.news.models import TelegramChannel

logger = logging.getLogger(__name__)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Echo handler that captures chat_id for registered TelegramChannel usernames.
    """
    if not update.message or not update.message.chat:
        return

    chat_username = update.message.chat.username
    if context.bot_data.get('id'):
        pass
    else:
        if chat_username:
            bot = await TelegramChannel.objects.filter(
                username=chat_username
            ).afirst()

            if bot:
                bot.chat_id = str(update.message.chat.id)
                await bot.asave(update_fields=['chat_id'])
                context.bot_data['id'] = True


_telegram_app: Application | None = None


async def get_bot_app() -> Application:
    """
    Returns an initialized Telegram Application singleton instance.
    """
    global _telegram_app
    if _telegram_app is None:
        token = config("TOKEN", default=config("BOT_TOKEN", default=""))
        if not token:
            raise ValueError("TOKEN (or BOT_TOKEN) is not configured in .env file.")
        
        _telegram_app = Application.builder().token(token).build()
        _telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
        await _telegram_app.initialize()
    return _telegram_app
