from rest_framework import serializers


class GeozoneSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    wkt = serializers.CharField()


class RequestGeozoneSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=False)
    show_public = serializers.BooleanField(default=True)
