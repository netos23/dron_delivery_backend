from django.urls import path

from orders import views

urlpatterns = [
    path("", views.CreateOrderAPIView.as_view())
]
