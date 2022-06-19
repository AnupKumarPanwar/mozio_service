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


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_provider(request, pk):
    return Response({})
