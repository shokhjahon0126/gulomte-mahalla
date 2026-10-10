import os
import logging
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

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

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("telegram_bot")


async def save_channel_chat_id(chat):
    """
    Kanal yoki guruh ma'lumotlarini bazadagi TelegramChannel bilan solishtirib, chat_id ni saqlaydi.
    """
    if not chat:
        return False

    chat_id = chat.id
    raw_username = (chat.username or "").lstrip("@").strip()
    title = (chat.title or "").strip()

    logger.info(f"🔎 Tekshirilmoqda: title='{title}', username='{raw_username}', chat_id={chat_id}")

    channel = None

    # 1. Username orqali qidirish (katta-kichik harf farqsiz)
    if raw_username:
        channel = await TelegramChannel.objects.filter(
            Q(username__iexact=raw_username) | 
            Q(username__iexact=f"@{raw_username}")
        ).afirst()

    # 2. Agar username orqali topilmasa, kanal sarlavhasi (title) orqali tekshirish
    if not channel and title:
        channel = await TelegramChannel.objects.filter(
            title__iexact=title
        ).afirst()

    if channel:
        old_id = channel.chat_id
        channel.chat_id = str(chat_id)
        await channel.asave(update_fields=['chat_id'])
        logger.info(f"✅ Kanal muvaffaqiyatli ulandi: '{channel.title}' (@{channel.username}) -> chat_id: {chat_id} (eski: {old_id})")
        return True
    else:
        logger.warning(f"⚠️ Bazada bunday kanal topilmadi: username='{raw_username}', title='{title}'. Iltimos, avval veb-saytda kanalni qo'shing.")
        return False


async def on_message_or_post(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    if not chat:
        return

    logger.info(f"📩 Yangi yangilanish (xabar/post): type={chat.type}, title={chat.title}, username={chat.username}, id={chat.id}")
    await save_channel_chat_id(chat)


async def on_my_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Bot kanalga qo'shilganda yoki admin huquqi berilganda darhol ishga tushadi
    chat = update.effective_chat
    if not chat:
        return

    logger.info(f"🤖 Bot statusi o'zgardi (my_chat_member): title={chat.title}, username={chat.username}, id={chat.id}")
    await save_channel_chat_id(chat)


def main() -> None:
    token = config("TOKEN")
    logger.info("🚀 Telegram bot ishga tushmoqda...")

    application = Application.builder().token(token).build()

    # 1. Bot kanalga qo'shilganda / admin qilinganda
    application.add_handler(ChatMemberHandler(on_my_chat_member, ChatMemberHandler.MY_CHAT_MEMBER))

    # 2. Kanal postlari (channel_post va edited_channel_post)
    application.add_handler(MessageHandler(filters.ChatType.CHANNEL, on_message_or_post))

    # 3. Guruh yoki superguruh xabarlari
    application.add_handler(MessageHandler(filters.ChatType.GROUPS, on_message_or_post))

    # 4. Har qanday boshqa xabarlar uchun umumiy handler
    application.add_handler(MessageHandler(filters.ALL, on_message_or_post))

    logger.info("Bot barcha turdagi yangilanishlarni (ALL_TYPES) tinglamoqda...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()