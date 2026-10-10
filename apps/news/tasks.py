from celery import shared_task
import httpx
from django.conf import settings
from .models import TelegramChannel

@shared_task
def send_news_to_telegram(news_id, title, description):
    bot_token = settings.TELEGRAM_BOT_TOKEN
    channels = TelegramChannel.objects.exclude(chat_id__isnull=True).exclude(chat_id="")
    
    text = f"*{title}*\n\n{description}"
    
    for channel in channels:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": channel.chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        httpx.post(url, data=payload)
        
    return f"News {news_id} sent to {channels.count()} channels."
