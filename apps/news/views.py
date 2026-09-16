from datetime import timezone
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from telegram import Bot
import asyncio
from decouple import config

from .models import News,TelegramChannel
from .serializers import NewsSerializer,TelegramChannelSerializers
from .permissions import IsAdminOrReadOnly

async def send_message(chat_ids, data):
    async with Bot(token=config('TOKEN')) as bot:
        async for chat_id in chat_ids.aiterator():
            await bot.send_message(
                chat_id=chat_id,
                text=f"{data['title']}\n\n{data['description']}",
            )

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

        return Response(serializers.data)


class TelegramChannelViewsets(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = TelegramChannelSerializers
    queryset = TelegramChannel.objects.all()

