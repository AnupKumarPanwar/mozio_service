from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Provider, ServiceArea
from .serializers import ProviderSerializer, ServiceAreaSerializer
from rest_framework import status
from django.contrib.gis.geos import Polygon


@api_view(['GET', 'POST'])
def get_post_providers(request):
    if request.method == 'GET':
        providers = Provider.objects.all()
        serializer = ProviderSerializer(providers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        data = {
            'name': request.data.get('name'),
            'email': request.data.get('email'),
            'phone': request.data.get('phone'),
            'lang': request.data.get('lang'),
            'currency': request.data.get('currency')
        }
        serializer = ProviderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_provider(request, pk):
    try:
        provider = Provider.objects.get(pk=pk)
    except Provider.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ProviderSerializer(provider)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProviderSerializer(provider, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        provider.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def get_post_service_areas(request, provider_id):
    if request.method == 'GET':
        service_areas = ServiceArea.objects.filter(provider_id=provider_id)
        serializer = ServiceAreaSerializer(service_areas, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        try:
            data = {
                'name': request.data.get('name'),
                'price': request.data.get('price'),
                'polygon': Polygon(tuple(map(tuple, request.data.get('polygon')))),
                'provider': provider_id,
            }
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        serializer = ServiceAreaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def get_delete_update_service_areas(request, provider_id, pk):
    try:
        service_area = ServiceArea.objects.get(pk=pk)
        if service_area.provider_id != int(provider_id):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except ServiceArea.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ServiceAreaSerializer(service_area)
        return Response(serializer.data)
    elif request.method == 'PUT':
        try:
            data = {
                'name': request.data.get('name'),
                'price': request.data.get('price'),
                'polygon': Polygon(tuple(map(tuple, request.data.get('polygon')))),
                'provider': provider_id,
            }
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        serializer = ServiceAreaSerializer(service_area, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({})
