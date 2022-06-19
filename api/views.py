from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Provider
from .serializers import ProviderSerializer
from rest_framework import status


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
    if request.method == 'GET':
        try:
            provider = Provider.objects.get(pk=pk)
        except Provider.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProviderSerializer(provider)
        return Response(serializer.data)
    else:
        return Response({})
