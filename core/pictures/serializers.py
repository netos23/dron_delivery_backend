from rest_framework import serializers


class PictureSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    url = serializers.URLField()
    link = serializers.URLField()


class SatPictureSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    url = serializers.URLField()
    link = serializers.URLField()
    created_at = serializers.DateTimeField()
    lat_1 = serializers.FloatField()
    lon_1 = serializers.FloatField()
    lat_2 = serializers.FloatField()
    lon_2 = serializers.FloatField()


class PictureByZoneRequestSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    geozone_id = serializers.IntegerField()
