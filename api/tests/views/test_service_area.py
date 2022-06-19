import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ...models import Provider, ServiceArea
from ...serializers import NestedServiceAreaSerializer, ServiceAreaSerializer
from django.contrib.gis.geos import Polygon


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
            ((0.0, 0.0), (0.0, 50.0), (50.0, 50.0), (50.0, 0.0), (0.0, 0.0))), provider=self.provider_1)

        ServiceArea.objects.create(name="Area 2", price=3.3, polygon=Polygon(
            ((0.0, 1.0), (0.0, 40.0), (50.0, 20.0), (50.0, 6.0), (0.0, 1.0))), provider=self.provider_1)

    def test_get_all_sevice_areas_by_provider(self):
        response = client.get(reverse('get_post_service_areas', kwargs={
                              'provider_id': self.provider_1.pk}))
        service_areas = ServiceArea.objects.filter(provider=self.provider_1)
        serializer = NestedServiceAreaSerializer(service_areas, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestCreateServiceArea(TestCase):
    """
    Test for adding a new service area for a provider
    """

    def setUp(self):
        self.provider = Provider.objects.create(
            name='Provider 1',
            email='p1@gmail.com',
            phone='+91123456789',
            lang='EN',
            currency='INR')

        self.valid_payload = {
            'name': 'Area 1',
            'price': 3.5,
            'polygon': [[0, 0], [0, 50], [50, 50], [50, 0], [0, 0]],
            'provider_id': self.provider.pk,
        }

        # first and last points in the polyon must be same
        self.invalid_payload = {
            'name': 'Area 1',
            'price': 3.5,
            'polygon': [[0, 0], [0, 50], [50, 50], [50, 0], [1, 0]],
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

    def test_invalid_create_service_area(self):
        response = client.post(
            reverse('get_post_service_areas', kwargs={
                'provider_id': self.provider.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestGetServiceArea(TestCase):
    """
    Test to get service area by id
    """

    def setUp(self):
        self.provider_1 = Provider.objects.create(
            name='Provider 1',
            email='p1@gmail.com',
            phone='+91123456789',
            lang='EN',
            currency='INR')

        self.provider_2 = Provider.objects.create(
            name='Provider 1',
            email='p2@gmail.com',
            phone='+91123456780',
            lang='EN',
            currency='INR')

        self.service_area = ServiceArea.objects.create(name="Area 1", price=1.2, polygon=Polygon(
            ((0.0, 0.0), (0.0, 50.0), (50.0, 50.0), (50.0, 0.0), (0.0, 0.0))), provider=self.provider_1)

    def test_get_sevice_area(self):
        """
        Valid test case
        """
        response = client.get(
            reverse(
                'get_delete_update_service_areas',
                kwargs={
                    'provider_id': self.provider_1.pk,
                    'pk': self.service_area.pk}))
        serializer = NestedServiceAreaSerializer(self.service_area)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_get_sevice_area(self):
        """
        Should return unauthorised because the service area does not belongs to the provider
        """
        response = client.get(
            reverse(
                'get_delete_update_service_areas',
                kwargs={
                    'provider_id': self.provider_2.pk,
                    'pk': self.service_area.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestUpdateServiceArea(TestCase):
    """
    Test to update service area
    """

    def setUp(self):
        self.provider = Provider.objects.create(
            name='Provider 1',
            email='p1@gmail.com',
            phone='+91123456789',
            lang='EN',
            currency='INR')

        self.service_area = ServiceArea.objects.create(name="Area 1", price=1.2, polygon=Polygon(
            ((0.0, 0.0), (0.0, 50.0), (50.0, 50.0), (50.0, 0.0), (0.0, 0.0))), provider=self.provider)

        self.valid_payload = {
            'name': 'Area 1',
            'price': 3.5,
            'polygon': [[1, 0], [0, 50], [50, 50], [50, 0], [1, 0]],
            'provider_id': self.provider.pk,
        }

        # first and last points in the polyon must be same
        self.invalid_payload = {
            'name': 'Area 1',
            'price': 3.5,
            'polygon': [[0, 0], [0, 50], [50, 50], [50, 0], [1, 0]],
            'provider_id': self.provider.pk,
        }

    def test_valid_update_sevice_area(self):
        """
        Valid test case
        """
        response = client.put(
            reverse(
                'get_delete_update_service_areas',
                kwargs={
                    'provider_id': self.provider.pk,
                    'pk': self.service_area.pk}),
            data=json.dumps(
                self.valid_payload),
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_sevice_area(self):
        """
        Fails because first and last element of the polygon are not same
        """
        response = client.put(
            reverse(
                'get_delete_update_service_areas',
                kwargs={
                    'provider_id': self.provider.pk,
                    'pk': self.service_area.pk}),
            data=json.dumps(
                self.invalid_payload),
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestDeleteServiceArea(TestCase):
    """
    Test to delete service area
    """

    def setUp(self):
        self.provider_1 = Provider.objects.create(
            name='Provider 1',
            email='p1@gmail.com',
            phone='+91123456789',
            lang='EN',
            currency='INR')

        self.service_area_1 = ServiceArea.objects.create(name="Area 1", price=1.2, polygon=Polygon(
            ((0.0, 0.0), (0.0, 50.0), (50.0, 50.0), (50.0, 0.0), (0.0, 0.0))), provider=self.provider_1)

        self.provider_2 = Provider.objects.create(
            name='Provider 2',
            email='p2@gmail.com',
            phone='+91123456788',
            lang='EN',
            currency='INR')

        self.service_area_2 = ServiceArea.objects.create(name="Area 2", price=4.2, polygon=Polygon(
            ((0.0, 0.0), (0.0, 50.0), (50.0, 50.0), (50.0, 0.0), (0.0, 0.0))), provider=self.provider_2)

    def test_valid_delete_sevice_area(self):
        """
        Successfully deletes the service area
        """
        response = client.delete(
            reverse(
                'get_delete_update_service_areas',
                kwargs={
                    'provider_id': self.provider_1.pk,
                    'pk': self.service_area_1.pk}),
            content_type='application/json')

        self.assertEqual(len(ServiceArea.objects.all()), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_delete_sevice_area(self):
        """
        Service area not found
        """
        response = client.delete(
            reverse('get_delete_update_service_areas', kwargs={
                    'provider_id': self.provider_1.pk, 'pk': 123}),
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_delete_sevice_area(self):
        """
        Fails beacuse service area does not belong to the prvider
        """
        response = client.delete(
            reverse(
                'get_delete_update_service_areas',
                kwargs={
                    'provider_id': self.provider_1.pk,
                    'pk': self.service_area_2.pk}),
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
