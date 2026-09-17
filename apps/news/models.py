import os

from django.db import models
from uuid import uuid4


def upload_file_name(self, filename):
    file_type = os.path.splitext(filename)[1][1:] 

    new_filename = f"{uuid4().hex}.{file_type}"
    return os.path.join(
        'uploads/',
        new_filename
    )


class News(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    
    file = models.FileField(
        null=True,
        blank=True,
        upload_to=upload_file_name
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


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

