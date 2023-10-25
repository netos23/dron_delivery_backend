from django.urls import path, include

from .views import (
    JWTRefreshView,
    UserView, RegisterUserView, FarmRegisterUserView, BotWebhookView,
)

urlpatterns = [
    path("email/", include("authorization.email.urls")),
    path("token/refresh", JWTRefreshView.as_view(), name="token_refresh"),
    path("user", UserView.as_view(), name="user"),
    path("register", RegisterUserView.as_view(), name="register"),
    path("farm_register", FarmRegisterUserView.as_view(), name="farm_register"),
    path("bot/webhook", BotWebhookView.as_view(), name="bot_webhook")
]
