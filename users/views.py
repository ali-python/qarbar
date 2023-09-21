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
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Q

from .serializers import AgentSerializer
from .models import Agent, UserProfile
from property.models import Property
from property.serializers import PropertySerializer
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
    

class AgentPropertyPagination(PageNumberPagination):
    page_size = 10 # Set the number of properties per page
    page_size_query_param = 'page_size'
    max_page_size = 100

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

        # Filter properties based on the agent's ID
        properties = Property.objects.filter(agent=agent)

        # Annotate property counts
        property_counts = Property.objects.filter(agent=agent).values(
            'property_type__home_types',
            'property_type__plot_types',
            'property_type__commercial_types'
        ).annotate(
            home_type_count=Count('property_type__home_types'),
            plot_type_count=Count('property_type__plot_types'),
            commercial_types_count=Count('property_type__commercial_types'),
            house_count_rent=Count('pk', filter=Q(property_type__home_types='house', rent_sale_type='rent')),
            house_count_sale=Count('pk', filter=Q(property_type__home_types='house', rent_sale_type='sale')),
            office_count_rent=Count('pk', filter=Q(property_type__commercial_types='office', rent_sale_type='rent')),
            office_count_sale=Count('pk', filter=Q(property_type__commercial_types='office', rent_sale_type='sale'))
        )

        # Apply pagination to the properties
        paginator = AgentPropertyPagination()
        properties = paginator.paginate_queryset(properties, request)

        serializer = AgentSerializer(instance=agent, context={'request': request})
        data = serializer.data
        data['properties'] = PropertySerializer(instance=properties, many=True).data
        data['property_counts'] = property_counts[0] if property_counts else {}

        return paginator.get_paginated_response(data)


