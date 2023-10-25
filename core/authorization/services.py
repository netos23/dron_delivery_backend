import secrets
from abc import ABC

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.tokens import RefreshToken

from .models import AuthCodeModel, Users


class RefreshTokenExt(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super(RefreshTokenExt, cls).for_user(user)
        token["user_id"] = user.pk
        token["is_verified"] = user.is_verified
        return token


def update_or_create_code(code, email=None):
    AuthCodeModel(email=email, code=code).clean()
    obj, create = AuthCodeModel.objects.update_or_create(email=email, defaults={"code": code})
    return obj.id


def generate_user_jwt(user: Users):
    return RefreshTokenExt.for_user(user)


def generate_no_auth_user_jwt(user: Users):
    return RefreshToken.for_user(user)


class AuthService(ABC):
    def __init__(self, user, **kwargs):
        self.old_user = user
        self.phone = kwargs.get("phone")
        self.email = kwargs.get("email")
        self.code = kwargs.get("code")
        self.user = None

    def _clean_auth_code(self) -> AuthCodeModel:
        raise NotImplementedError("Please Implement this method")

    def validate(self) -> bool:
        raise NotImplementedError("Please Implement this method")

    @transaction.atomic
    def auth(self):
        self.validate()
        self.user = self._get_or_create_user()
        self.gen_token()
        self._clean_auth_code()
        return self.user

    def _get_or_create_user(self) -> Users:
        user_params = {}
        if self.phone is not None:
            user_params["phone"] = self.phone
        if self.email is not None:
            user_params["email"] = self.email
        user = (
            Users.objects.filter(**user_params, is_active=True).order_by("-id").first()
        )
        self.new_user = user is None
        if user is None:
            user = Users(
                phone=self.phone,
                email=self.email,
                username=secrets.token_hex(16),
                is_verified=True,
            )
            user.set_password(secrets.token_hex(8))
        user.is_verified = True
        user.save()
        return user

    def gen_token(self):
        refresh = generate_user_jwt(self.user)
        self.user.refresh_token = refresh
        self.user.access_token = refresh.access_token
        self.user.last_login = timezone.now()
        self.user.save()


class UserService:

    def __init__(self, user_id: Users, **kwargs):
        self.user = self.get_user(user_id)
        self.kwargs = kwargs

    def get_user(self, user_id) -> Users:
        try:
            return Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            raise APIException(f"UserView {user_id} does not exists")

    def update_user(self, *, data: dict) -> Users:
        users = Users.objects.filter(id=self.user.id)
        first_name = data.get("first_name") or self.user.first_name or ""
        last_name = data.get("last_name") or self.user.last_name or ""
        if (first_name or last_name) and not data.get("name"):
            data["name"] = " ".join([first_name, last_name]).strip()
        users.update(**data)
        self.user = users.first()
        return self.user
