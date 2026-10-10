from apps.news.models import TelegramChannel
from rest_framework import serializers
from .models import News
import os

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'description', 'send_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class TelegramChannelSerializers(serializers.ModelSerializer):
    status = serializers.ReadOnlyField()

    class Meta:
        model = TelegramChannel
        fields = ['id', 'title', 'username', 'status']
        read_only_fields = ['id', 'status']

    

    
            

