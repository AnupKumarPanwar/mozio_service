from django.contrib.gis.db import models

class Provider(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    lang = models.CharField(max_length=5)
    currency = models.CharField(max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ServiceArea(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    polygon = models.PolygonField()
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name