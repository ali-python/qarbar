from rest_framework import status, viewsets, permissions, filters
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as django_filters
from django.contrib.auth import authenticate
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token 
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Q,  Case, When, IntegerField
from users.filter_set import AgentFilter
from .serializers import AgentSerializer, UserProfileSerializer
from .models import Agent, UserProfile
from property.models import Property
from property.serializers import PropertySerializer
from users.serializers import (
    AuthTokenCustomSerializer,
    UserSerializer,
    RegisterSerializer,
    UpdateUserSerializer, 
    AgentUserUpdateSerializer
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

# class AgentViewSet(viewsets.ModelViewSet):
#     queryset = Agent.objects.all().order_by('-created_at')
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
#     serializer_class = AgentSerializer
#     filterset_class = AgentFilter
#     permission_classes = []

#     def list(self, request, *args, **kwargs):
#         if request.query_params:
#             agents = self.filter_queryset(self.get_queryset())
#         else:
#             agents = self.get_queryset()
#         agent_data = []
        
#         for agent in agents:
#             # Count rental and sale properties for each agent
#             rent_count = agent.individual_properties.filter(rent_sale_type='rent').count()
#             sale_count = agent.individual_properties.filter(rent_sale_type='sale').count()

#             serializer = self.get_serializer(agent)
#             data = serializer.data
#             data['rent_property_count'] = rent_count
#             data['sale_property_count'] = sale_count
#             agent_data.append(data)

#         return Response(agent_data)
    
#     def perform_create(self, serializer):
#         serializer.save()
    
#     @action(detail=True, methods=['GET'])
#     def detail_agent(self, request, pk=None):
#         agent = self.get_object()
#         agent.views_count += 1  # Increment view count by 1
#         agent.save()

#         # Filter properties based on the agent's ID
#         properties = Property.objects.filter(agent=agent)

#         # Annotate property counts
#         property_counts = Property.objects.filter(agent=agent).values(
#             'property_type__home_types',
#             'property_type__plot_types',
#             'property_type__commercial_types'
#         ).annotate(
#             home_type_count=Count('property_type__home_types'),
#             plot_type_count=Count('property_type__plot_types'),
#             commercial_types_count=Count('property_type__commercial_types'),
#             house_count_rent=Count('pk', filter=Q(property_type__home_types='house', rent_sale_type='rent')),
#             house_count_sale=Count('pk', filter=Q(property_type__home_types='house', rent_sale_type='sale')),
#             office_count_rent=Count('pk', filter=Q(property_type__commercial_types='office', rent_sale_type='rent')),
#             office_count_sale=Count('pk', filter=Q(property_type__commercial_types='office', rent_sale_type='sale'))
#         )

#          # Count how many properties an agent has for sale and for rent
#         sale_count = properties.filter(rent_sale_type='sale').count()
#         rent_count = properties.filter(rent_sale_type='rent').count()

#         # Apply pagination to the properties
#         paginator = AgentPropertyPagination()
#         properties = paginator.paginate_queryset(properties, request)

#         serializer = AgentSerializer(instance=agent, context={'request': request})
#         data = serializer.data
#         data['properties'] = PropertySerializer(instance=properties, many=True).data
#         data['property_counts'] = property_counts[0] if property_counts else {}
#         data['sale_count'] = sale_count
#         data['rent_count'] = rent_count

#         return paginator.get_paginated_response(data)


class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all().order_by('-created_at')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    serializer_class = AgentSerializer
    filterset_class = AgentFilter
    permission_classes = []

    def list(self, request, *args, **kwargs):
        if request.query_params:
            agents = self.filter_queryset(self.get_queryset())
        else:
            agents = self.get_queryset()
        agent_data = []
        
        for agent in agents:
            # Count rental and sale properties for each agent
            rent_count = agent.individual_properties.filter(rent_sale_type='rent').count()
            sale_count = agent.individual_properties.filter(rent_sale_type='sale').count()

            serializer = self.get_serializer(agent)
            data = serializer.data
            data['rent_property_count'] = rent_count
            data['sale_property_count'] = sale_count
            agent_data.append(data)

        return Response(agent_data)
    
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

        # Count how many properties an agent has for sale and for rent
        sale_count = properties.filter(rent_sale_type='sale').count()
        rent_count = properties.filter(rent_sale_type='rent').count()

        # Apply pagination to the properties
        paginator = AgentPropertyPagination()
        properties = paginator.paginate_queryset(properties, request)

        serializer = AgentSerializer(instance=agent, context={'request': request})
        data = serializer.data
        data['properties'] = PropertySerializer(instance=properties, many=True).data
        data['property_counts'] = property_counts[0] if property_counts else {}
        data['sale_count'] = sale_count
        data['rent_count'] = rent_count

        return paginator.get_paginated_response(data)
    
    @action(detail=True, methods=['PUT'])
    def update_agent(self, request, pk=None):
        agent_id = pk
        agent = Agent.objects.get(pk=agent_id)
        agent_serializer = AgentSerializer(instance=agent, data=request.data.get('agent', {}), partial=True)

        if agent_serializer.is_valid():
            agent_serializer.save()

            # Assuming that userprofile data is part of the agent data
            # If not, you can update it in a similar manner.
            userprofile_data = request.data.get('userprofile', {})
            userprofile = agent.user.userprofile

            if userprofile_data:
                userprofile.phone_number = userprofile_data.get('phone_number', userprofile.phone_number)
                userprofile.dob = userprofile_data.get('dob', userprofile.dob)
                userprofile.city = userprofile_data.get('city', userprofile.city)
                userprofile.country = userprofile_data.get('country', userprofile.country)
                userprofile.save()

            return Response(agent_serializer.data, status=status.HTTP_200_OK)
        return Response(agent_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

