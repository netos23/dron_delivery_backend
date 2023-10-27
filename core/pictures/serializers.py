from rest_framework import serializers


class SatPictureSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    url = serializers.URLField()
    link = serializers.URLField()
    created_at = serializers.DateTimeField()
    lat_1 = serializers.FloatField(null=True)
    lon_1 = serializers.FloatField(null=True)
    lat_2 = serializers.FloatField(null=True)
    lon_2 = serializers.FloatField(null=True)


class SatByZoneRequestSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    geozone_id = serializers.IntegerField()
