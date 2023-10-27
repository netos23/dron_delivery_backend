from typing import List

from rest_framework import serializers
from geozones.models import GeozoneModel, DeprecatedGeozoneModel


def tuple_validation(value):
    print(value)
    if len(value) != 2:
        raise serializers.ValidationError("Waited 2 floats")


def wkt_validation(value):
    if len(value) <= 0:
        raise serializers.ValidationError("Waited Polygons")


def polygon_validation(value):
    if len(value) < 3:
        raise serializers.ValidationError("Expected 3 or more points")


class WktField(serializers.ListField):
    default_validators = [wkt_validation]
    child = serializers.ListField(
                                    child=serializers.ListField(child=serializers.FloatField(),
                                                                validators=[tuple_validation]),
                                    validators=[polygon_validation]
                                )

    @staticmethod
    def _polygon_to_wkt(polygon: List[List[float]]) -> str:
        return "(" + ", ".join(map(lambda points: f"{points[0]} {points[1]}", polygon)) + ")"

    @staticmethod
    def _wkt_polygon_to_list(wkt: str) -> List[List[float]]:
        wkt = wkt.rstrip(")").lstrip("(")
        return list(map(lambda x: list(map(float, x.split(" "))), wkt.split(", ")))

    def to_representation(self, data: str):
        polygons = []
        data = data.lstrip("MULTIPOLYGON ").lstrip("POLYGON ").lstrip("(").rstrip(")")
        for polygon_s in data.split("), "):
            polygon_s = polygon_s.lstrip("(")
            polygons.append(self._wkt_polygon_to_list(polygon_s))
        return polygons

    def to_internal_value(self, data):
        if len(data) > 1:
            s = "MULTIPOLYGON ("
            for polygon in data:
                s += "(" + self._polygon_to_wkt(polygon) + "), "
            return s.rstrip(", ") + ")"
        else:
            return "POLYGON (" + self._polygon_to_wkt(data[0]) + ")"


class DeprecatedGeozoneSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    wkt = WktField()

    def create(self, validated_data):
        return DeprecatedGeozoneModel.objects.create(name=validated_data['name'], wkt=validated_data['wkt'])


class GeozoneSerializer(DeprecatedGeozoneSerializer):
    user_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        return GeozoneModel.objects.create(**validated_data)


class RequestGeozoneSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=False)
    show_public = serializers.BooleanField(default=True)
