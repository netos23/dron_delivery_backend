from rest_framework import serializers
from pictures.serializers import PictureSerializer

from satellites.models import PositionModel


class SatteliteSerializer(serializers.Serializer):
    id = serializers.CharField(source='object_id')
    name = serializers.CharField(source='object_name')
    picture = serializers.URLField()


class SatByZoneRequestSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    geozone_id = serializers.IntegerField()


class SatByZoneResponseSerializer(serializers.Serializer):
    class PositionSerializer(serializers.ModelSerializer):
        class Meta:
            model = PositionModel
            fields = ["lat", "lon", "created_at"]

    sat_id = serializers.IntegerField()
    positions = serializers.ListField(child=PositionSerializer())
