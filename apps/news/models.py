from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_future_date(value):
    if value and value < timezone.now():
        raise ValidationError("Yuborish vaqti kelajakda bo'lishi kerak! (The date and time must be in the future)")

class News(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    
    send_date = models.DateTimeField(
        verbose_name="Send Date", 
        validators=[validate_future_date], 
        null=True, blank=True,
        help_text="Qaysi vaqtda yuborilishini belgilang"
    )
 
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Schedule the task if send_date is set and it's a new news or send_date is updated
        # Here we just schedule it simply.
        if self.send_date:
            from .tasks import send_news_to_telegram
            send_news_to_telegram.apply_async(
                args=[self.id, self.title, self.description],
                eta=self.send_date
            )



class TelegramChannel(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    username = models.CharField(max_length=255, verbose_name="Username", unique=True)
    chat_id = models.CharField(max_length=255, verbose_name="Chat ID", unique=True,null=True,blank=True)
    
    class Meta:
        verbose_name = "Telegram Channel"
        verbose_name_plural = "Telegram Channel"
        unique_together = [["username", "chat_id"]]
        ordering = ['-pk']
        
    def __str__(self):
        return self.title

    @property
    def status(self):
        if self.chat_id:
            return "✅ Connected"
        return "❌ Not Connected"

