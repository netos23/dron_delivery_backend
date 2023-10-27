from datetime import datetime

from rest_framework import generics

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from django.db.models import Q
from django.shortcuts import get_object_or_404

from drf_yasg.utils import swagger_auto_schema

from pictures.serializers import PictureByZoneRequestSerializer, SatPictureSerializer
from pictures.models import SatellitePictureModel
from geozones.models import DeprecatedGeozoneModel, GeozoneModel


class ListPicturesView(generics.GenericAPIView):
    serializer_class = SatPictureSerializer
    request_serializer = PictureByZoneRequestSerializer
    renderer_classes = [JSONRenderer]

    @staticmethod
    def not_intersects_with_depr_zone(polygon) -> bool:
        return DeprecatedGeozoneModel.objects.filter(geom__intersects=polygon).count() == 0

    @staticmethod
    def get_pics_query_set(polygon, date):
        return SatellitePictureModel.objects.filter(Q(polygon_intersections=polygon) &
                                                    Q(created_at__gte=date) &
                                                    Q(expired_date__gt=datetime.now()))

    @swagger_auto_schema(query_serializer=request_serializer(),
                         responses={200: serializer_class(many=True), 404: {}, 403: {}})
    def get(self, request):
        req_ser = self.request_serializer(data=request.query_params)
        req_ser.is_valid(raise_exception=True)

        geozone_id = req_ser.data["geozone_id"]
        date = req_ser.data["date"]

        polygon = get_object_or_404(GeozoneModel, pk=geozone_id).geom
        if not self.not_intersects_with_depr_zone(polygon):
            return Response(status=403)

        pics_pos = self.get_pics_query_set(polygon, date)
        if pics_pos.count() == 0:
            return Response(status=404)

        resp_serializer = SatPictureSerializer(data=pics_pos.all(), many=True)
        resp_serializer.is_valid(raise_exception=True)
        return Response(data=resp_serializer.data, status=200)
