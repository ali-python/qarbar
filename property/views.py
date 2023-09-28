from rest_framework import viewsets
from rest_framework.response import Response
from django.http import HttpResponse
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from django.db.models import Sum 
from .models import Country, City, Property, Area
from django.db.models import Count, Q
from calendar import month_name
from users.models import Agent
from datetime import datetime, timedelta
from property.filter_set import PropertyFilter
from users.serializers import AgentSerializer
from PIL import Image, ImageDraw, ImageFont
from .serializers import (
    CountrySerializer,
    CitySerializer,
    PropertySerializer, 
    MediaSerializer,
    CreatePropertySerializer, 
    AreaSerializer
    )


class CountryViewSet(viewsets.ViewSet):
    permission_classes = []
    def list(self, request):
        queryset = Country.objects.all()
        serializer = CountrySerializer(queryset, many=True)
        
        return Response(serializer.data)

    def create(self, request):
        serializer = CountrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Country.objects.all()
        country = get_object_or_404(queryset, pk=pk)
        serializer = CountrySerializer(country)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            country = Country.objects.get(pk=pk)
        except Country.DoesNotExist:
            return Response(status=404)

        serializer = CountrySerializer(country, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            country = Country.objects.get(pk=pk)
        except Country.DoesNotExist:
            return Response(status=404)

        country.delete()
        return Response(status=204)


class CityViewSet(viewsets.ViewSet):
    permission_classes = []
    def list(self, request):
        queryset = City.objects.all()
        serializer = CitySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = City.objects.all()
        city = get_object_or_404(queryset, pk=pk)
        serializer = CitySerializer(city)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            city = City.objects.get(pk=pk)
        except City.DoesNotExist:
            return Response(status=404)

        serializer = CitySerializer(city, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            city = City.objects.get(pk=pk)
        except City.DoesNotExist:
            return Response(status=404)

        city.delete()
        return Response(status=204)
    

class AreaViewSet(viewsets.ViewSet):
    permission_classes = []
    def list(self, request):
        queryset = Area.objects.all()
        serializer = AreaSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = AreaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = Area.objects.all()
        area = get_object_or_404(queryset, pk=pk)
        serializer = AreaSerializer(area)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            area = Area.objects.get(pk=pk)
        except Area.DoesNotExist:
            return Response(status=404)

        serializer = AreaSerializer(area, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            area = Area.objects.get(pk=pk)
        except Area.DoesNotExist:
            return Response(status=404)

        area.delete()
        return Response(status=204)


class PropertyViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = PropertySerializer
    queryset = Property.objects.all().order_by('-id')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]

    search_fields = ['property_type__home_types', 'property_type__plot_types','property_type__commercial_types', 'property_type__unit_types', 'property_type__size', 'rent_sale_type']
    ordering_fields = ['created_at', 'updated_at', 'property_type']
    filterset_class = PropertyFilter
    permission_classes = []

    @action(detail=False, methods=['GET'])
    def agent_properties(self, request):
        user = self.request.user

        if user.is_staff or Agent.objects.filter(user=user).exists():
            # Filter properties based on the agent user
            if user.is_staff:
                # If the user is staff, show all properties
                properties = self.get_queryset()
            else:
                # If the user is an agent user, show only their properties
                properties = self.get_queryset().filter(agent__user=user)

            # Count properties by property types (home types and plot types)
            property_counts = properties.values('property_type__home_types', 'property_type__plot_types', 'property_type__commercial_types') \
                .annotate(home_type_count=Count('property_type__home_types'),
                        plot_type_count=Count('property_type__plot_types'),
                        commercial_types_count=Count('property_type__commercial_types'))
            
               # Count properties with home_type='house'
            house_count_rent = properties.filter(property_type__home_types='house', rent_sale_type= 'rent').count()
            house_count_sale = properties.filter(property_type__home_types='house', rent_sale_type= 'sale').count()
            office_count_sale = properties.filter(property_type__commercial_types='office', rent_sale_type= 'sale').count()
            office_count_rent = properties.filter(property_type__commercial_types='office', rent_sale_type= 'rent').count()

            serializer = self.get_serializer(properties, many=True)

            # Include the property counts in the response
            response_data = {
                'properties': serializer.data,
                'property_counts': property_counts,
                'house_count_rent': house_count_rent,
                'house_count_sale':house_count_sale,
                'office_count_sale':office_count_sale,
                'office_count_rent':office_count_rent
            }

            return Response(response_data)
        return HttpResponse("Unauthorized", status=401)

    @action(detail=False, methods=['GET'], url_path='agent-dashboard')
    def agent_dashboard(self, request):
        user = self.request.user

        if user.is_staff or Agent.objects.filter(user=user).exists():
            # Calculate the total number of agent properties
            if user.is_staff:
                total_agent_properties = Property.objects.count()
            else:
                total_agent_properties = Property.objects.filter(agent__user=user).count()

            # Calculate the total number of properties sold based on 'available' field
            total_properties_sold = Property.objects.filter(agent__user=user, available=False).count()

            # Calculate the total number of rent and sale properties
            total_rent_properties = Property.objects.filter(agent__user=user, rent_sale_type='rent').count()
            total_sale_properties = Property.objects.filter(agent__user=user, rent_sale_type='sale').count()

            # Calculate the total views on agent properties
            total_views_on_agent_properties = Property.objects.filter(agent__user=user).aggregate(Sum('views_count'))['views_count__sum']
            # Calculate the total views on rent properties
            total_views_on_rent_properties = Property.objects.filter(agent__user=user, rent_sale_type='rent').aggregate(total_views=Sum('views_count'))['total_views']

            # Calculate the total views on sale properties
            total_views_on_sale_properties = Property.objects.filter(agent__user=user, rent_sale_type='sale').aggregate(total_views=Sum('views_count'))['total_views']
            response_data = {
                'total_agent_properties': total_agent_properties,
                'total_properties_sold': total_properties_sold,
                'total_rent_properties': total_rent_properties,
                'total_sale_properties': total_sale_properties,
                'total_views_on_agent_properties': total_views_on_agent_properties,
                'total_views_on_rent_properties': total_views_on_rent_properties,
                'total_views_on_sale_properties': total_views_on_sale_properties,
            }

            return Response(response_data)
        return HttpResponse("Unauthorized", status=401)
    
    @action(detail=False, methods=['GET'], url_path='agent-graph')
    def agent_graph(self, request):
        user = self.request.user

        if user.is_staff or Agent.objects.filter(user=user).exists():
            # Calculate the date 6 months ago
            six_months_ago = datetime.now() - timedelta(days=180)

            # Query properties sold in the last 6 months
            properties_sold_in_last_six_months = Property.objects.filter(
                Q(available=False) & Q(date__gte=six_months_ago)
            )

            # Create a dictionary to store counts by month
            month_counts = {}
            for month_num in range(1, 13):
                month_name_str = month_name[month_num]
                month_counts[month_name_str] = {
                    'total_properties_sold': 0,
                    'rent_properties_sold': 0,
                    'sale_properties_sold': 0,
                }

            # Populate the counts by month
            for property in properties_sold_in_last_six_months:
                month_name_str = month_name[property.date.month]
                month_counts[month_name_str]['total_properties_sold'] += 1
                if property.rent_sale_type == 'rent':
                    month_counts[month_name_str]['rent_properties_sold'] += 1
                elif property.rent_sale_type == 'sale':
                    month_counts[month_name_str]['sale_properties_sold'] += 1

            # Calculate the total number of properties
            total_properties = Property.objects.count()

            response_data = {
                'month_counts': month_counts,
                'total_properties': total_properties,
            }

            return Response(response_data)
        return HttpResponse("Unauthorized", status=401)
    
    def destroy(self, request, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user.is_staff or self.request.user.users.agent:
            return super().destroy(request, *args, **kwargs)
        return Response({'message': 'Page not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['GET'])
    def detail_property(self, request, pk=None):
        property = self.get_object()
        property.views_count += 1  # Increment view count by 1
        property.save()
        serializer = PropertySerializer(property)
        return Response(serializer.data)
    
    @action(detail=True, methods=['POST'], url_path='toggle-available')
    def toggle_available(self, request, pk=None):
        property_instance = self.get_object()
        property_instance.available = not property_instance.available
        property_instance.save()
        return Response({'message': 'Available status toggled successfully'}, status=200)
    
    @action(detail=False, methods=['POST'])
    def create_property(self, request):
        if self.request.user:
            print("Request Data:", request.data)
            serializer = CreatePropertySerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                property = serializer.save()
                return Response(PropertySerializer(instance=property, context={'request': request}).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Page not found ohhh its error and some error'}, status=status.HTTP_404_NOT_FOUND)

