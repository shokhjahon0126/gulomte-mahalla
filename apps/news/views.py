from rest_framework import viewsets
from .models import News
from .serializers import NewsSerializer
from .permissions import IsAdminOrReadOnly


class NewsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for News CRUD operations.
    GET requests are open to anonymous and authenticated users.
    POST, PUT, PATCH, DELETE operations are restricted to Admin users only.
    """
    queryset = News.objects.all().order_by('-created_at')
    serializer_class = NewsSerializer
    permission_classes = [IsAdminOrReadOnly]
