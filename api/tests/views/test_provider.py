from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ...models import Provider
from ...serializers import ProviderSerializer

client = Client()


class TestGetAllProviders(TestCase):
    """
    Test for GET all providers API
    """

    def setUp(self):
        """
        Method that runs before every test
        """
        Provider.objects.create(
            name='Provider 1', email='p1@gmail.com', phone='+91123456789', lang='EN', currency='INR')
        Provider.objects.create(
            name='Provider 2', email='p2@gmail.com', phone='+91123456799', lang='EN', currency='USD')

    def test_get_all_providers(self):
        """
        Test for GET all providers
        """
        response = client.get(reverse('get_post_providers'))
        providers = Provider.objects.all()
        serializer = ProviderSerializer(providers, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
