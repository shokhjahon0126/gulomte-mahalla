from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsViewSet,TelegramChannelViewsets

app_name = 'news'

urlpatterns = [
    path('', NewsViewSet.as_view({'get':'list','post':'create'}), name='news-list'),
    path('<int:pk>/', NewsViewSet.as_view({'get':'retrieve','delete':'destroy','put':'update','patch':'partial_update'}), name='news-detail'),
    path('channel/', TelegramChannelViewsets.as_view({'get':'list','post':'create'}), name='channel-list'),
    path('channel/<int:pk>/', TelegramChannelViewsets.as_view({'get':'retrieve','delete':'destroy','patch':'partial_update'}), name='channel-detail'),
]
