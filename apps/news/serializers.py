from apps.news.models import TelegramChannel
from rest_framework import serializers
from .models import News
import os

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'description', 'file', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


    def validate_file(self, value):

        ext = os.path.splitext(value.name)[1].lower()
        valid_extensions = [
            '.pdf',
            '.jpg',
            '.jpeg',
            '.png',
            '.mp3',
            '.mp4',
        ]
        
        if ext not in valid_extensions:
            raise serializers.ValidationError(
                f"Ruxsat berilmagan fayl formati. Faqat {', '.join(valid_extensions)} formatlariga ruxsat berilgan."
            )
        
        max_size = 5 * 1024 * 1024 
        
        if value.size > max_size:
            raise serializers.ValidationError("Fayl hajmi 5 MB dan oshmasligi kerak.")
            
        return value


class TelegramChannelSerializers(serializers.ModelSerializer):
    class Meta:
        model = TelegramChannel
        exclude = ('chat_id',)
        read_only_fields = ['id']
    

    
            

