import json
import logging
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from decouple import config

from .telegram_bot import get_bot_app

logger = logging.getLogger(__name__)

WEBHOOK_SECRET = config("WEBHOOK_SECRET", default=None)


@csrf_exempt
async def telegram_webhook_view(request):
    """
    Async Django view to receive updates from Telegram Webhook.
    """
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    # Validate secret token if WEBHOOK_SECRET is set in environment
    if WEBHOOK_SECRET:
        received_secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if received_secret != WEBHOOK_SECRET:
            logger.warning("Unauthorized webhook request with invalid secret token.")
            return JsonResponse({"error": "Invalid secret token"}, status=403)

    try:
        raw_body = request.body.decode("utf-8")
        if not raw_body:
            return JsonResponse({"error": "Empty body"}, status=400)

        data = json.loads(raw_body)
        app = await get_bot_app()
        
        # Deserialize JSON data into a Telegram Update object
        update = Update.de_json(data=data, bot=app.bot)
        
        # Process update asynchronously using Application
        await app.process_update(update)
        
        return JsonResponse({"status": "ok"})
    except json.JSONDecodeError:
        logger.error("Failed to decode JSON from Telegram update payload.")
        return HttpResponseBadRequest("Invalid JSON")
    except Exception as e:
        logger.error(f"Error processing Telegram webhook update: {e}", exc_info=True)
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
