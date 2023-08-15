from rest_framework import status, viewsets, permissions
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import AgentSerializer
from .models import Agent

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
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_data = UserSerializer(instance=user).data

        return Response({
            'token': token.key,
            'user': user_data
        })


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
    

# class AgentView(APIView):
#     authentication_classes = []
#     permission_classes = []

#     def post(self, request, *args, **kwargs):
#         serializer = AgentSerializer(data=request.data)
#         if serializer.is_valid():
#             agent = serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, *args, **kwargs):
#         try:
#             agent = Agent.objects.get(pk=kwargs['pk'])
#         except Agent.DoesNotExist:
#             return Response({'detail': 'Agent not found.'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = AgentSerializer(agent, data=request.data)
#         if serializer.is_valid():
#             agent = serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request, *args, **kwargs):
#         agents = Agent.objects.all()
#         serializer = AgentSerializer(agents, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

class AgentViewSet(viewsets.mixins.ListModelMixin,
                   viewsets.mixins.RetrieveModelMixin,
                   viewsets.mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    authentication_classes = []
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        agent = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

