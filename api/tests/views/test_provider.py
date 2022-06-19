import json
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


class TestCreateProvider(TestCase):
    """ Test module for creating a new provider """

    def setUp(self):
        self.valid_payload = {
            'name': 'Provider 1',
            'email': 'p1@gmail.com',
            'phone': '+911234567890',
            'lang': 'EN',
            'currency': 'INR'
        }
        self.invalid_payload = {
            'name': 'Provider 2',
            'email': '',
            'phone': '+911234567891',
            'lang': 'EN',
            'currency': 'USD'
        }

    def test_valid_create_provider(self):
        response = client.post(
            reverse('get_post_providers'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_provider(self):
        response = client.post(
            reverse('get_post_providers'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestGetProiver(TestCase):
    """ Test for GET provider by id API """

    def setUp(self):
        self.provider_1 = Provider.objects.create(
            name='Provider 1', email='p1@gmail.com', phone='+91123456789', lang='EN', currency='INR')
        self.provider_2 = Provider.objects.create(
            name='Provider 2', email='p2@gmail.com', phone='+91123456799', lang='EN', currency='USD')

    def test_valid_get_provider(self):
        response = client.get(
            reverse('get_delete_update_provider', kwargs={'pk': self.provider_1.pk}))
        provider = Provider.objects.get(pk=self.provider_1.pk)
        serializer = ProviderSerializer(provider)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_get_provider(self):
        response = client.get(
            reverse('get_delete_update_provider', kwargs={'pk': 23}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
