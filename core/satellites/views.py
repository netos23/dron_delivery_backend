from typing import List

from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, mixins
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404

from satellites.models import SatelliteModel, PositionModel
from satellites.serializers import SatteliteSerializer, SatByZoneRequestSerializer, \
    SatByZoneResponseSerializer

from geozones.models import DeprecatedGeozoneModel, GeozoneModel


class SatelliteView(generics.GenericAPIView):
    """Show all satellites."""

    serializer_class = SatteliteSerializer
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(responses={200: serializer_class()})
    def get(self, request):
        satellites = SatelliteModel.objects.filter(is_active=True)
        return Response(data=self.serializer_class(satellites, many=True).data, status=status.HTTP_200_OK)


class SatelliteByZone(generics.GenericAPIView):
    serializer_class = SatByZoneResponseSerializer
    request_serializer = SatByZoneRequestSerializer
    renderer_classes = [JSONRenderer]

    @staticmethod
    def not_intersects_with_depr_zone(polygon) -> bool:
        return DeprecatedGeozoneModel.objects.filter(geom__intersects=polygon).count() == 0

    @staticmethod
    def get_positions_query_set(polygon, date):
        return PositionModel.objects.filter(Q(point__within=polygon) & Q(created_at__gte=date))

    @swagger_auto_schema(query_serializer=request_serializer(),
                         responses={200: serializer_class(many=True), 404: {}, 403: {}})
    def get(self, request):
        request_ser = self.request_serializer(data=request.query_params)
        request_ser.is_valid(raise_exception=True)
        date = request_ser.validated_data['date']
        geozone_id = request_ser.validated_data['geozone_id']

        polygon = get_object_or_404(GeozoneModel, pk=geozone_id).geom
        if not self.not_intersects_with_depr_zone(polygon):
            return Response(status=403)

        qs_pos = self.get_positions_query_set(polygon, date)
        if qs_pos.count() == 0:
            return Response(status=404)

        json_ = []
        sats = qs_pos.values("satellite").distinct()
        for sat in sats:
            sat_id = sat["satellite"]
            zones_ser = self.serializer_class.PositionSerializer(
                              data=qs_pos.filter(satellite=sat_id).all(), many=True)
            zones_ser.is_valid()
            json_.append({"sat_id": sat_id,
                          "positions": zones_ser.data})
        return Response(data=json_, status=200)
