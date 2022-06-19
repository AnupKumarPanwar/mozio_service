from django.test import TestCase
from ...models import Provider, ServiceArea
from django.contrib.gis.geos import Polygon


class TestServiceAreaModel(TestCase):
    """
    This class contains tests for ServiceArea model.
    """

    def test_create(self):
        """
        This method tests creation of ServiceArea.
        """

        provider = Provider.objects.create(
            name="Provider 1",
            email="p1@gmail.com",
            phone="+918968894728",
            lang="EN",
            currency="INR",
        )

        service_area = ServiceArea.objects.create(
            name="Service Area 1",
            price=12.5,
            polygon=Polygon(
                ((0.0, 0.0), (0.0, 50.0), (50.0, 50.0), (50.0, 0.0), (0.0, 0.0))),
            provider=provider
        )

        self.assertEqual(str(service_area), service_area.name)
