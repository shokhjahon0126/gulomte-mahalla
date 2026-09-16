import os

from telegram import ForceReply, Update
from telegram.ext import Application,  ContextTypes, MessageHandler, filters
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE','core.settings')

import django 
django.setup()

from apps.news.models import TelegramChannel


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    id = update.message.chat.id

    if context.bot_data.get('id'):
        pass
        # await update.message.reply_text("Siz login qilingansiz")

    else:
        bot = await TelegramChannel.objects.filter(
            username = update.message.chat.username
        ).afirst()

        
        if bot:

            bot.chat_id
            bot.chat_id = update.message.chat.id
            await bot.asave(update_fields=['chat_id'])
            context.bot_data['id'] = True
            

            print(
                update.message.chat.id,
                update.message.chat.username
            )
            await update.message.reply_text('endi login qilindi!')
        else:
            await update.message.reply_text(
                "Bu kanal bazada mavjud emas!"
            )




def main() -> None:
    application = Application.builder().token(config("TOKEN")).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()