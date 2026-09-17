from datetime import timezone
from rest_framework import viewsets, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from telegram import Bot
import asyncio
from decouple import config
from telegram.constants import ParseMode

from .models import News,TelegramChannel
from .serializers import NewsSerializer,TelegramChannelSerializers
from .permissions import IsAdminOrReadOnly

def build_news_text(data):
    return (
        "📰 <b>YANGILIK</b>\n"
        "━━━━━━━━━━━━━━\n\n"
        f"<b>{data['title']}</b>\n\n"
        f"{data['description']}\n\n"
        "━━━━━━━━━━━━━━\n"
        "📌 <i>Gulomte Mahalla</i>"
    )


async def send_message(chat_ids, data):
    async with Bot(token=config("TOKEN")) as bot:

        text = build_news_text(data)

        async for chat_id in chat_ids.aiterator():
            try:
                # 1. Avval yangilik matni
                await bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    parse_mode=ParseMode.HTML,
                )

                # 2. Keyin fayl, agar mavjud bo'lsa
                file = data.get("file")

                if file:
                    file.seek(0)

                    await bot.send_document(
                        chat_id=chat_id,
                        document=file,
                    )

            except Exception as exc:
                print(f"❌ Failed to send to {chat_id}: {exc}")

class NewsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for News CRUD operations.
    GET requests are open to anonymous and authenticated users.
    POST, PUT, PATCH, DELETE operations are restricted to Admin users only.
    """
    authentication_classes = [JWTAuthentication]
    queryset = News.objects.all().order_by('-created_at')
    serializer_class = NewsSerializer
    permission_classes = [IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializers = self.serializer_class(data=request.data)
        serializers.is_valid(raise_exception=True)

        validated_data = serializers.validated_data

        chat_ids = TelegramChannel.objects.values_list(
            'chat_id',
            flat=True,
        )

        asyncio.run(
            send_message(chat_ids, validated_data)
        )
        serializers.save()

        return Response(serializers.data, status=status.HTTP_201_CREATED)


class TelegramChannelViewsets(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = TelegramChannelSerializers
    queryset = TelegramChannel.objects.all()




import json
import asyncio

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from telegram import Update

from .telegram import application


_initialized = False
_lock = asyncio.Lock()


async def initialize_application():
    global _initialized

    if _initialized:
        return

    async with _lock:
        if _initialized:
            return

        await application.initialize()

        _initialized = True


@csrf_exempt
async def telegram_webhook(request):

    if request.method != "POST":
        return JsonResponse(
            {"detail": "Method not allowed"},
            status=405,
        )

    secret = request.headers.get(
        "X-Telegram-Bot-Api-Secret-Token"
    )

    if secret != settings.TELEGRAM_WEBHOOK_SECRET:
        return JsonResponse(
            {"detail": "Forbidden"},
            status=403,
        )

    await initialize_application()

    data = json.loads(request.body)

    update = Update.de_json(
        data=data,
        bot=application.bot,
    )

    await application.process_update(update)

    return JsonResponse({"ok": True})