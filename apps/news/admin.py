from django.contrib import admin
from .models import News,TelegramChannel

admin.site.register([News,TelegramChannel])


# @admin.register(News)
# class NewsAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'created_at', 'updated_at')
#     search_fields = ('title', 'description')
#     list_filter = ('created_at',)
