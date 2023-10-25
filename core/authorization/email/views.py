from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, serializers
from rest_framework import status
from rest_framework.response import Response

from .services import EmailPart1, EmailPart2
from ..serializers import AuthResponseSerializer


class EmailPart1View(generics.GenericAPIView):
    class EmailPart1RequestSerializer(serializers.Serializer):
        email = serializers.CharField(max_length=128)
        digits = serializers.IntegerField(min_value=3, max_value=9, default=3, required=False)

    serializer_class = serializers.Serializer

    @swagger_auto_schema(
        request_body=EmailPart1RequestSerializer, responses={200: serializer_class(), 451: serializer_class()}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.EmailPart1RequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = EmailPart1(**serializer.data)
        service.send_code()
        return Response({}, status=status.HTTP_200_OK)


class EmailPart2View(generics.GenericAPIView):
    class EmailPart2RequestSerializer(serializers.Serializer):
        email = serializers.CharField(max_length=128)
        code = serializers.CharField()

    serializer_class = AuthResponseSerializer

    @swagger_auto_schema(
        request_body=EmailPart2RequestSerializer, responses={"200": serializer_class()}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.EmailPart2RequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = EmailPart2(request.user, **serializer.data)
        user = service.auth()
        return Response(AuthResponseSerializer(user).data, status=status.HTTP_200_OK)
