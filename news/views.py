from rest_framework import viewsets
from .models import News
from .serializers import NewsSerializer
from rest_framework import viewsets, filters, permissions 

class NewsViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = News.objects.all()
    serializer_class = NewsSerializer
