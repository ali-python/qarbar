# serializers.py
from rest_framework import serializers
from .models import News

class NewsSerializer(serializers.ModelSerializer):
    description = serializers.CharField(allow_blank=True, allow_null=True,)

    class Meta:
        model = News
        fields = '__all__'
