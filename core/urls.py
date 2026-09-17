from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from django.conf import settings
from django.conf.urls.static import static

# Source - https://stackoverflow.com/a/5518073
# Posted by Micah Carrick, modified by community. See post 'Timeline' for change history
# Retrieved 2026-09-17, License - CC BY-SA 4.0

urlpatterns = [
    path('admin/', admin.site.urls),

    # Existing Backend REST APIs (Do Not Touch)
    path('User/', include('apps.users.urls')),
    path('News/', include('apps.news.urls')),

    # drf-spectacular documentation URLs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Public Unauthenticated News Views (Read-Only Aholi Portali)
    path('public/news/', TemplateView.as_view(template_name='news/public_list.html'), name='web-public-news-list'),
    path('public/news/<int:pk>/', TemplateView.as_view(template_name='news/public_detail.html'), name='web-public-news-detail'),

    # Authenticated Presentation Views (Django Templates)
    path('', TemplateView.as_view(template_name='dashboard/index.html'), name='home'),
    path('login/', TemplateView.as_view(template_name='auth/login.html'), name='web-login'),
    path('dashboard/', TemplateView.as_view(template_name='dashboard/index.html'), name='web-dashboard'),
    path('news/', TemplateView.as_view(template_name='news/list.html'), name='web-news-list'),
    path('news/create/', TemplateView.as_view(template_name='news/form.html'), name='web-news-create'),
    path('news/<int:pk>/', TemplateView.as_view(template_name='news/detail.html'), name='web-news-detail'),
    path('news/<int:pk>/edit/', TemplateView.as_view(template_name='news/form.html'), name='web-news-edit'),
    path('profile/', TemplateView.as_view(template_name='profile/detail.html'), name='web-profile-detail'),
    path('profile/edit/', TemplateView.as_view(template_name='profile/edit.html'), name='web-profile-edit'),
    path('profile/change-password/', TemplateView.as_view(template_name='profile/change_password.html'), name='web-profile-change-password'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
