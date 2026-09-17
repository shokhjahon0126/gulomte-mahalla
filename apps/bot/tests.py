import json
from unittest.mock import patch, AsyncMock
from django.test import TestCase, AsyncClient
from apps.news.models import TelegramChannel


class TelegramWebhookTests(TestCase):
    def setUp(self):
        self.channel = TelegramChannel.objects.create(
            title="Test Channel",
            username="test_channel_user"
        )
        self.async_client = AsyncClient()

    @patch('apps.bot.telegram_bot.Application.process_update', new_callable=AsyncMock)
    async def test_webhook_post_success(self, mock_process_update):
        payload = {
            "update_id": 123456789,
            "message": {
                "message_id": 1,
                "date": 1600000000,
                "chat": {
                    "id": 987654321,
                    "type": "supergroup",
                    "username": "test_channel_user"
                },
                "text": "Hello bot"
            }
        }

        response = await self.async_client.post(
            '/bot/webhook/',
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "ok")
        self.assertTrue(mock_process_update.called)
