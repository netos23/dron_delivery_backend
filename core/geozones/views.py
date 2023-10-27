from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from geozones.models import GeozoneModel
from geozones.serializers import GeozoneSerializer, RequestGeozoneSerializer


class GeozoneView(generics.GenericAPIView):
    """Show all geozones."""

    request_serializer = RequestGeozoneSerializer
    serializer_class = GeozoneSerializer
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(query_serializer=request_serializer(), responses={200: serializer_class()})
    def get(self, request):
        serializer = self.request_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.data.get('user_id')
        show_public = serializer.data.get('show_public')
        if user_id:
            geozones = GeozoneModel.objects.filter(Q(user_id=user_id) | Q(user_id__isnull=show_public))
        else:
            geozones = GeozoneModel.objects.filter(Q(user_id__isnull=show_public))
        return Response(data=self.serializer_class(geozones, many=True).data, status=status.HTTP_200_OK)


class DeprecatedGeozoneView(generics.GenericAPIView):
    """Show all geozones."""

    request_serializer = RequestGeozoneSerializer
    serializer_class = GeozoneSerializer
    renderer_classes = [JSONRenderer]

    @swagger_auto_schema(responses={200: serializer_class()})
    def get(self, request):
        return Response(data=self.serializer_class(GeozoneModel.objects.all(), many=True).data,
                        status=status.HTTP_200_OK)
