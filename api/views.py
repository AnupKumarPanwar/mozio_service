from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST'])
def get_post_providers(request):
    return Response({})


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_provider(request, pk):
    return Response({})


