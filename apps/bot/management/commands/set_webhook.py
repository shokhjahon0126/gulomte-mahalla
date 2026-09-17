import asyncio
from django.core.management.base import BaseCommand
from decouple import config
from telegram import Bot


class Command(BaseCommand):
    help = "Sets or deletes the Telegram Bot Webhook URL with Telegram API."

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            type=str,
            help='Public HTTPS URL for the webhook (e.g. https://yourdomain.com/bot/webhook/)',
        )
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete the current webhook set for the Telegram bot.',
        )
        parser.add_argument(
            '--drop-pending',
            action='store_true',
            help='Drop all pending updates when setting/deleting webhook.',
        )

    def handle(self, *args, **options):
        token = config("TOKEN", default=config("BOT_TOKEN", default=""))
        if not token:
            self.stderr.write(self.style.ERROR("TOKEN (or BOT_TOKEN) is not configured in environment or .env file."))
            return

        bot = Bot(token=token)

        async def _set_webhook():
            if options['delete']:
                self.stdout.write("Deleting Telegram webhook...")
                result = await bot.delete_webhook(drop_pending_updates=options['drop_pending'])
                if result:
                    self.stdout.write(self.style.SUCCESS("Webhook successfully deleted!"))
                else:
                    self.stderr.write(self.style.ERROR("Failed to delete webhook."))
            else:
                url = options.get('url')
                if not url:
                    self.stderr.write(self.style.ERROR("Please provide a --url parameter or use --delete."))
                    return

                self.stdout.write(f"Setting webhook URL to: {url}")
                kw = {
                    "url": url,
                    "drop_pending_updates": options['drop_pending']
                }
                secret = config("WEBHOOK_SECRET", default=None)
                if secret:
                    kw["secret_token"] = secret

                result = await bot.set_webhook(**kw)
                if result:
                    self.stdout.write(self.style.SUCCESS(f"Webhook successfully set to {url}!"))
                else:
                    self.stderr.write(self.style.ERROR("Failed to set webhook."))

                info = await bot.get_webhook_info()
                self.stdout.write(f"Current Webhook Info: URL={info.url}, Pending Updates={info.pending_update_count}")

        asyncio.run(_set_webhook())
