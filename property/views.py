from rest_framework import viewsets
from rest_framework.response import Response
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from .models import Country, City, Property, Area
from property.filter_set import PropertyFilter
from users.serializers import AgentSerializer
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

@extend_schema(
    summary="Get a list of all properties, and create , update and detail of property",
    description="This endpoint returns a list of all properties, also it have create property  detail of property and update property in the system.",
    tags=["Property"],
)

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
        if user.is_staff or (hasattr(user, 'users') and hasattr(user.users, 'agent')):
            # Filter properties based on the agent user
            if user.is_staff:
                # If the user is staff, show all properties
                properties = self.get_queryset()
            else:
                # If the user is an agent user, show only their properties
                properties = self.get_queryset().filter(agent__agent_user__user=user)
            serializer = self.get_serializer(properties, many=True)
            return Response(serializer.data)
        return HttpResponse("Unauthorized", status=401)

    def destroy(self, request, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user.is_staff or self.request.user.users.agent:
            return super().destroy(request, *args, **kwargs)
        return Response({'message': 'Page not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['GET'])
    def detail_property(self, request, pk=None):
        property = self.get_object()
        serializer = PropertySerializer(property)
        return Response(serializer.data)
    
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

