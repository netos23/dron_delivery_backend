from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from satellites.models import SatelliteModel
from satellites.serializers import SatteliteSerializer


class SatelliteView(generics.GenericAPIView):
    """Show all satellites."""

    serializer_class = SatteliteSerializer
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(responses={200: serializer_class()})
    def get(self, request):
        satellites = SatelliteModel.objects.filter(is_active=True)
        return Response(data=self.serializer_class(satellites, many=True).data, status=status.HTTP_200_OK)