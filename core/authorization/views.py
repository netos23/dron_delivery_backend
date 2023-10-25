from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import serializers
from .email.services import EmailPart1
from .models import Users
from .serializers import (
    JWTRefreshSerializer,
    ResponseUserSerializer, RequestUserSerializer, RequestFarmerSerializer,
)
from .services import (
    UserService
)

from utils.exceptions import BaseRestException
import logging

logger_bot = logging.getLogger(__name__)


class JWTRefreshView(TokenRefreshView):
    """Refresh token. Please send access JWT in header."""

    permission_classes = ()
    authentication_classes = ()
    serializer_class = JWTRefreshSerializer


class UserView(generics.GenericAPIView):
    """Work with users"""

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthentication,)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: ResponseUserSerializer,
            status.HTTP_401_UNAUTHORIZED: {},
        }
    )
    def get(self, request):
        """Get user. JWT required"""
        request.auth.verify()
        user_id = request.auth.get("user_id")
        service = UserService(user_id=user_id)
        user = service.get_user(user_id)
        return Response(ResponseUserSerializer(user).data, status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=RequestUserSerializer,
        responses={
            status.HTTP_200_OK: ResponseUserSerializer,
            status.HTTP_401_UNAUTHORIZED: {},
        },
    )
    def patch(self, request):
        """Update user info. JWT required"""
        serializer = RequestUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = request.auth.get("user_id")
        service = UserService(user_id)
        user = service.update_user(data=serializer.validated_data)
        data = ResponseUserSerializer(user).data
        return Response(data, status.HTTP_200_OK)

    def delete(self, request):
        user_id = request.auth.get("user_id")
        user = Users.objects.get(id=user_id)
        user.is_active = False
        user.first_name = "deleted"
        user.last_name = "deleted"
        user.email = "deleted"
        user.birthday = None
        user.gender = "-1"
        user.save()
        if user:
            return Response(data={}, status=status.HTTP_204_NO_CONTENT)


class RegisterUserView(generics.GenericAPIView):

    @swagger_auto_schema(
        request_body=RequestUserSerializer,
        responses={
            status.HTTP_200_OK: {},
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = RequestUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = EmailPart1(**serializer.validated_data)
        service.register_user()
        service.send_code()
        return Response({}, status=status.HTTP_200_OK)


class BotWebhookView(generics.GenericAPIView):
    @swagger_auto_schema(
        request_body=serializers.Serializer,
        responses={
            status.HTTP_200_OK: {},
        },
    )
    def post(self, request, *args, **kwargs):
        try:
            body = request.data
            text = body['message']['text']
            token = text.split(' ')[-1]
            user = self.associate_user_by_token(token)
            chat_id = int(body['message']['chat']['id'])
            user.tg_chat_id = chat_id
            user.save()

            text = "Привет!"
            BotSingleton().bot.send_message(chat_id, text)
        except:
            pass
        return Response({}, status=status.HTTP_200_OK)

    @staticmethod
    def associate_user_by_token(token):
        token_th = BotIdToken.objects.filter(id_token=token)
        if not token_th.exists():
            raise BaseRestException("Объект не найден", status_code=400)
        return token_th.first().user


class FarmRegisterUserView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthentication,)

    @swagger_auto_schema(
        request_body=RequestFarmerSerializer,
        responses={
            status.HTTP_200_OK: {},
        },
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_staff:
            raise APIException(f"Farmer already got brand")
        serializer = RequestFarmerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.brand = serializer.data['brand']
        user.address = serializer.data['address']
        user.save()
        return Response({}, status=status.HTTP_200_OK)
