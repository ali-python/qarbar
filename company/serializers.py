from rest_framework import serializers
from .models import Company, CustomUser, CompanyAgent

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class CompanyAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAgent
        fields = '__all__'
