from rest_framework import serializers
from pictures.serializers import PictureSerializer
from satellites.models import PositionModel


class SatteliteSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField(source='object_name')
    picture = serializers.URLField()
    resolution = serializers.FloatField()


class RequestPositionSerializer(serializers.Serializer):
    satellite_id = serializers.CharField(required=True)


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PositionModel
        fields = '__all__'
