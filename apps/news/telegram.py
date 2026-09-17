from django.conf import settings

from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    filters,
)

from apps.news.models import TelegramChannel


async def echo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    username = update.message.chat.username

    if context.bot_data.get("id"):
        return

    bot = await TelegramChannel.objects.filter(
        username=username
    ).afirst()

    if bot:
        bot.chat_id = update.message.chat.id

        await bot.asave(
            update_fields=["chat_id"]
        )

        context.bot_data["id"] = True


application = (
    Application.builder()
    .token(settings.TELEGRAM_BOT_TOKEN)
    .updater(None)
    .build()
)


application.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        echo,
    )
)