from rest_framework import status, viewsets, permissions
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.db import transaction
from django.contrib.auth import authenticate
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token 

from .serializers import AgentSerializer
from .models import Agent, UserProfile

from users.serializers import (
    AuthTokenCustomSerializer,
    UserSerializer,
    RegisterSerializer,
    UpdateUserSerializer
)

class ObtainAuthTokenCustom(ObtainAuthToken):
    serializer_class = AuthTokenCustomSerializer


class LoginView(ObtainAuthTokenCustom):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_data = UserSerializer(instance=user).data

        return Response({
            'token': token.key,
            'user': user_data
        })

# class LoginView(APIView):
    # permission_classes = ()

    # def post(self, request, *args, **kwargs):
    #     email = request.data.get('email')
    #     password = request.data.get('password')
    #     print("_______________________________")
    #     print(f"Email: {email}, Password: {password}")

    #     user = authenticate(request, email=email, password=password)
    #     print(f"Authenticated User: {user}")

    #     if user is not None:
    #         token, created = Token.objects.get_or_create(user=user)
    #         user_data = UserSerializer(instance=user).data

    #         return Response({
    #             'token': token.key,
    #             'user': user_data
    #         })
    #     else:
    #         print("Authentication failed")
    #         return Response({'detail': 'Authentication failed'}, status=400)


class RegisterView(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            user_data = UserSerializer(instance=user).data
            return Response({
                'token': token.key,
                'user': user_data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = self.queryset
        # queryset = queryset.filter(id=self.request.user.id)
        return queryset

    @action(detail=False, url_path='update_user_details', methods=['POST'])
    def update_user_details(self, request):
        serializer = UpdateUserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            data = UserSerializer(instance=user).data
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = []

    def get_queryset(self):
        return Agent.objects.all().order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save()
    
    @action(detail=True, methods=['GET'])
    def detail_agent(self, request, pk=None):
        agent = self.get_object()
        agent.views_count += 1  # Increment view count by 1
        agent.save() 
        serializer = AgentSerializer(agent)
        return Response(serializer.data)
