from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsViewSet,TelegramChannelViewsets

urlpatterns = [
    path('',NewsViewSet.as_view({'get':'list','post':'create'})),
    path('<int:pk>/',NewsViewSet.as_view({'get':'retrieve','delete':'destroy','patch':'partial_update'})),
    path('channel/',TelegramChannelViewsets.as_view({'get':'list','post':'create'})),
    path('channel/<int:pk>/',TelegramChannelViewsets.as_view({'get':'retrieve','delete':'destroy','patch':'partial_update'})),
]
