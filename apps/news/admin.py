from django.contrib import admin
from .models import News, TelegramChannel

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'send_date', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('send_date', 'created_at')

@admin.register(TelegramChannel)
class TelegramChannelAdmin(admin.ModelAdmin):
    list_display = ('title', 'username', 'get_status')
    readonly_fields = ('chat_id',)
    
    def get_status(self, obj):
        return obj.status
    get_status.short_description = "Status"

