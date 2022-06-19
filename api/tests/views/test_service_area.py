import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ...models import Provider, ServiceArea
from ...serializers import ServiceAreaSerializer
from django.contrib.gis.geos import Polygon


# initialize the APIClient app
client = Client()


class TestGetAllServiceAreasByProvider(TestCase):
    """
    Test for GET all service areas by provider id
    """

    def setUp(self):
        """
        Method that runs before every test
        """
        self.provider_1 = Provider.objects.create(
            name='Provider 1', email='p1@gmail.com', phone='+91123456789', lang='EN', currency='INR')
        self.provider_2 = Provider.objects.create(
            name='Provider 2', email='p2@gmail.com', phone='+91123456799', lang='EN', currency='USD')

        ServiceArea.objects.create(name="Area 1", price=1.2, polygon=Polygon(
            ((0.0, 0.0), (0.0, 50.0), (50.0, 50.0), (50.0, 0.0), (0.0, 0.0))), provider=self.provider_1)

        ServiceArea.objects.create(name="Area 2", price=3.3, polygon=Polygon(
            ((0.0, 1.0), (0.0, 40.0), (50.0, 20.0), (50.0, 6.0), (0.0, 1.0))), provider=self.provider_1)

    def test_get_all_sevice_areas_by_provider(self):
        response = client.get(reverse('get_post_service_areas', kwargs={
                              'provider_id': self.provider_1.pk}))
        service_areas = ServiceArea.objects.filter(provider=self.provider_1)
        serializer = ServiceAreaSerializer(service_areas, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestCreateServiceArea(TestCase):
    """
    Test for adding a new service area for a provider
    """

    def setUp(self):
        self.provider = Provider.objects.create(
            name='Provider 1', email='p1@gmail.com', phone='+91123456789', lang='EN', currency='INR')

        self.valid_payload = {
            'name': 'Area 1',
            'price': 3.5,
            'polygon': [[0, 0], [0, 50], [50, 50], [50, 0], [0, 0]],
            'provider_id': self.provider.pk,
        }

    def test_valid_create_service_area(self):
        response = client.post(
            reverse('get_post_service_areas', kwargs={
                'provider_id': self.provider.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
