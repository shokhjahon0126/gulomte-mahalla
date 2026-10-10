import logging
from django.conf import settings
from django.db.models import Q
from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    ChatMemberHandler,
    filters,
)

from apps.news.models import TelegramChannel

logger = logging.getLogger("telegram_webhook")


async def save_channel_chat_id(chat):
    if not chat:
        return False

    chat_id = chat.id
    raw_username = (chat.username or "").lstrip("@").strip()
    title = (chat.title or "").strip()

    logger.info(f"🔎 Webhook tekshirmoqda: title='{title}', username='{raw_username}', chat_id={chat_id}")

    channel = None
    if raw_username:
        channel = await TelegramChannel.objects.filter(
            Q(username__iexact=raw_username) | 
            Q(username__iexact=f"@{raw_username}")
        ).afirst()

    if not channel and title:
        channel = await TelegramChannel.objects.filter(
            title__iexact=title
        ).afirst()

    if channel:
        channel.chat_id = str(chat_id)
        await channel.asave(update_fields=["chat_id"])
        logger.info(f"✅ Webhook orqali kanal ulandi: '{channel.title}' -> {chat_id}")
        return True
    return False


async def on_message_or_post(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    if chat:
        await save_channel_chat_id(chat)


async def on_my_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    if chat:
        await save_channel_chat_id(chat)


application = (
    Application.builder()
    .token(settings.TELEGRAM_BOT_TOKEN)
    .updater(None)
    .build()
)

application.add_handler(ChatMemberHandler(on_my_chat_member, ChatMemberHandler.MY_CHAT_MEMBER))
application.add_handler(MessageHandler(filters.ChatType.CHANNEL, on_message_or_post))
application.add_handler(MessageHandler(filters.ChatType.GROUPS, on_message_or_post))
application.add_handler(MessageHandler(filters.ALL, on_message_or_post))