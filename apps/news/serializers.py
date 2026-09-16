from apps.news.models import TelegramChannel
from rest_framework import serializers
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'description', 'file', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class TelegramChannelSerializers(serializers.ModelSerializer):
    class Meta:
        model = TelegramChannel
        exclude = ('chat_id',)
        read_only_fields = ['id']
    

    
            

