from rest_framework import viewsets
from rest_framework.response import Response
from django.http import HttpResponse
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from django.db.models import Sum 
from .models import Country, City, Property, Area, Media
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
    AreaSerializer,
    PropertyTypesSerializer,
    InstallmentSerializer,
    AmentiesSerializer,
    PropertyLocationSerializer,
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
            if user.is_staff:
                properties = self.get_queryset()
            else:
                properties = self.get_queryset().filter(agent__user=user)
        else:
            properties = self.get_queryset().filter(user=request.user)


        property_counts = properties.values('property_type__home_types', 'property_type__plot_types', 'property_type__commercial_types') \
            .annotate(home_type_count=Count('property_type__home_types'),
                    plot_type_count=Count('property_type__plot_types'),
                    commercial_types_count=Count('property_type__commercial_types'))

        house_count_rent = properties.filter(property_type__home_types='house', rent_sale_type='rent').count()
        house_count_sale = properties.filter(property_type__home_types='house', rent_sale_type='sale').count()
        office_count_sale = properties.filter(property_type__commercial_types='office', rent_sale_type='sale').count()
        office_count_rent = properties.filter(property_type__commercial_types='office', rent_sale_type='rent').count()

        serializer = self.get_serializer(properties, many=True)

        response_data = {
            'properties': serializer.data,
            'property_counts': property_counts,
            'house_count_rent': house_count_rent,
            'house_count_sale': house_count_sale,
            'office_count_sale': office_count_sale,
            'office_count_rent': office_count_rent
        }

        return Response(response_data)

    @action(detail=False, methods=['GET'], url_path='agent-dashboard')
    def agent_dashboard(self, request):
        user = self.request.user

        if user.is_staff or Agent.objects.filter(user=user).exists():
            if user.is_staff:
                total_agent_properties = Property.objects.count()
            else:
                total_agent_properties = Property.objects.filter(agent__user=user).count()

            total_properties_sold = Property.objects.filter(agent__user=user, available=False).count()

            total_rent_properties = Property.objects.filter(agent__user=user, rent_sale_type='rent').count()
            total_sale_properties = Property.objects.filter(agent__user=user, rent_sale_type='sale').count()

            total_views_on_agent_properties = Property.objects.filter(agent__user=user).aggregate(Sum('views_count'))['views_count__sum']
            total_views_on_rent_properties = Property.objects.filter(agent__user=user, rent_sale_type='rent').aggregate(total_views=Sum('views_count'))['total_views']

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
            six_months_ago = datetime.now() - timedelta(days=180)

            properties_sold_in_last_six_months = Property.objects.filter(
                Q(available=False) & Q(date__gte=six_months_ago)
            )

            month_counts = {}
            for month_num in range(1, 13):
                month_name_str = month_name[month_num]
                month_counts[month_name_str] = {
                    'total_properties_sold': 0,
                    'rent_properties_sold': 0,
                    'sale_properties_sold': 0,
                }

            for property in properties_sold_in_last_six_months:
                month_name_str = month_name[property.date.month]
                month_counts[month_name_str]['total_properties_sold'] += 1
                if property.rent_sale_type == 'rent':
                    month_counts[month_name_str]['rent_properties_sold'] += 1
                elif property.rent_sale_type == 'sale':
                    month_counts[month_name_str]['sale_properties_sold'] += 1
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
        property.views_count += 1
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

    @action(detail=True, methods=['PUT', 'PATCH'])
    def update_property(self, request, pk=None):
        try:
            property_instance = self.get_object()
        except Property.DoesNotExist:
            return Response({'detail': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PropertySerializer(property_instance, data=request.data, partial=True)

        if serializer.is_valid():
            amenties_data = request.data.get('amenties')
            property_location_data = request.data.get('property_location')
            property_type_data = request.data.get('property_type')
            installment_data = request.data.get('installment')
            area_data = request.data.get('area')

            if amenties_data:
                amenties_serializer = AmentiesSerializer(property_instance.amenties, data=amenties_data, partial=True)
                if amenties_serializer.is_valid():
                    amenties_serializer.save()

            if property_location_data:
                property_location_instance = property_instance.property_location
                property_location_instance.latitude = property_location_data.get('latitude', property_location_instance.latitude)
                property_location_instance.longitude = property_location_data.get('longitude', property_location_instance.longitude)
                property_location_instance.save()

            if area_data:
                area_serializer = AreaSerializer(property_instance.area, data=area_data, partial=True)
                if area_serializer.is_valid():
                    area_serializer.save()

            if property_type_data:
                property_type_serializer = PropertyTypesSerializer(property_instance.property_type, data=property_type_data, partial=True)
                if property_type_serializer.is_valid():
                    property_type_serializer.save()

            if installment_data:
                installment_serializer = InstallmentSerializer(property_instance.installment, data=installment_data, partial=True)
                if installment_serializer.is_valid():
                    installment_serializer.save()

            media_data = request.data.get('media')
            if media_data:
                for media_item_data in media_data:
                    media_item_id = media_item_data.get('id', None) 
                    if media_item_id:
                        try:
                            media_item = Media.objects.get(id=media_item_id, property=property_instance)
                            media_item.media_type = media_item_data.get('media_type', media_item.media_type)
                            media_item.image_url = media_item_data.get('image_url', media_item.image_url)
                            media_item.save()
                        except Media.DoesNotExist:
                            pass
                    else:
                        Media.objects.create(property=property_instance, **media_item_data)
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






