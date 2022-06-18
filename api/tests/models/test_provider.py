from django.test import TestCase
from ...models import Provider


class TestProvider(TestCase):
    """
    This class contains tests for Provider model.
    """

    def test_create(self):
        """
        This method tests the creation of Provider.
        """

        provider = Provider.objects.create(
            name="Provider 1",
            email="p1@gmail.com",
            phone="+918968894728",
            lang="EN",
            currency="INR",
        )

        self.assertEqual(str(provider), provider.name)
