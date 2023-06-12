from rest_framework import viewsets
from rest_framework.response import Response
from .models import Country, City, Property
from .serializers import CountrySerializer, CitySerializer, PropertySerializer

class CountryViewSet(viewsets.ViewSet):
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

class PropertyViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Property.objects.all()
        serializer = PropertySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PropertySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def retrieve(self, request, pk=None):
        queryset = Property.objects.all()
        property_obj = get_object_or_404(queryset, pk=pk)
        serializer = PropertySerializer(property_obj)
        return Response(serializer.data)

    def update(self, request, pk=None):
        property_obj = get_object_or_404(Property.objects.all(), pk=pk)
        serializer = PropertySerializer(property_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        property_obj = get_object_or_404(Property.objects.all(), pk=pk)
        property_obj.delete()
        return Response(status=204)

