import datetime

from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from satellites.models import SatelliteModel, PositionModel
from satellites.serializers import SatteliteSerializer, PositionSerializer, RequestPositionSerializer
from satellites.tasks import update_positions


class SatelliteView(generics.GenericAPIView):
    """Show all satellites."""

    serializer_class = SatteliteSerializer
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(responses={200: serializer_class()})
    def get(self, request):
        satellites = SatelliteModel.objects.filter(is_active=True)
        return Response(data=self.serializer_class(satellites, many=True).data, status=status.HTTP_200_OK)


class PositionView(APIView):
    serializer_class = PositionSerializer
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(query_serializer=RequestPositionSerializer(), responses={200: serializer_class()})
    def get(self, request):
        serializer = RequestPositionSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        satellite_id = serializer.data.get('satellite_id')
        positions = PositionModel.objects.filter(satellite_id=satellite_id).all()
        positions = positions[::max(1, positions.count()//3000)]
        return Response(data=self.serializer_class(positions, many=True).data, status=status.HTTP_200_OK)
