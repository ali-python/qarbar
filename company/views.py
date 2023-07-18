# views.py
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Company, CustomUser, CompanyAgent
from .serializers import CompanySerializer, CustomUserSerializer, CompanyAgentSerializer

class CompanyViewSet(viewsets.ViewSet):
    permission_classes = []
    def list(self, request):
        queryset = Company.objects.all()
        serializer = CompanySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def retrieve(self, request, pk=None):
        queryset = Company.objects.get(pk=pk)
        serializer = CompanySerializer(queryset)
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = Company.objects.get(pk=pk)
        serializer = CompanySerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = Company.objects.get(pk=pk)
        instance.delete()
        return Response(status=204)

class CustomUserViewSet(viewsets.ViewSet):
    permission_classes = []
    def list(self, request):
        queryset = CustomUser.objects.all()
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def retrieve(self, request, pk=None):
        queryset = CustomUser.objects.get(pk=pk)
        serializer = CustomUserSerializer(queryset)
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = CustomUser.objects.get(pk=pk)
        serializer = CustomUserSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = CustomUser.objects.get(pk=pk)
        instance.delete()
        return Response(status=204)

class CompanyAgentViewSet(viewsets.ViewSet):
    permission_classes = []
    def list(self, request):
        queryset = CompanyAgent.objects.all()
        serializer = CompanyAgentSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CompanyAgentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def retrieve(self, request, pk=None):
        queryset = CompanyAgent.objects.get(pk=pk)
        serializer = CompanyAgentSerializer(queryset)
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = CompanyAgent.objects.get(pk=pk)
        serializer = CompanyAgentSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = CompanyAgent.objects.get(pk=pk)
        instance.delete()
        return Response(status=204)
