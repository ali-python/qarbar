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
    company = CompanySerializer(read_only=True)
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = CompanyAgent
        fields = '__all__'
