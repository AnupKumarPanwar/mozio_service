from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ...models import Provider, ServiceArea
from django.contrib.gis.geos import Polygon


client = Client()


class TestCheckServiceArea(TestCase):
    """
    Test to check service areas containing a point
    """

    def setUp(self):
        """
        Method that runs before every test
        """
        self.provider_1 = Provider.objects.create(
            name='Provider 1',
            email='p1@gmail.com',
            phone='+91123456789',
            lang='EN',
            currency='INR')
        self.provider_2 = Provider.objects.create(
            name='Provider 2',
            email='p2@gmail.com',
            phone='+91123456799',
            lang='EN',
            currency='USD')

        ServiceArea.objects.create(name="Area 1", price=1.2, polygon=Polygon(
            ((0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0), (0.0, 0.0))), provider=self.provider_1)

        ServiceArea.objects.create(name="Area 2", price=3.3, polygon=Polygon(
            ((1.0, 0.0), (3.0, 0.0), (3.0, 2.0), (1.0, 2.0), (1.0, 0.0))), provider=self.provider_2)

        ServiceArea.objects.create(name="Area 3", price=5.1, polygon=Polygon(
            ((2.0, 0.0), (4.0, 0.0), (4.0, 2.0), (2.0, 2.0), (2.0, 0.0))), provider=self.provider_1)

        ServiceArea.objects.create(name="Area 4", price=2.0, polygon=Polygon(
            ((0.0, 1.0), (2.0, 1.0), (2.0, 4.0), (0.0, 4.0), (0.0, 1.0))), provider=self.provider_2)

    def test_check_service_area(self):
        """
        Valid test case
        """
        response = client.get(reverse('check_service_areas'), {
                              'lat': 1.5, 'lng': 1.5})
        self.assertEqual(len(response.data['features']), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
