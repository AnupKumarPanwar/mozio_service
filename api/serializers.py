from rest_framework import serializers
from .models import Provider, ServiceArea
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'


class ServiceAreaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ServiceArea
        geo_field = "polygon"
        fields = '__all__'
