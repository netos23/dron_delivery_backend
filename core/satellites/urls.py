from django.urls import path

from satellites import views

urlpatterns = [
    path("", views.SatelliteView.as_view()),
    path("points/", views.PositionView.as_view())
]
