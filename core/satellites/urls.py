from django.urls import path

from satellites import views

urlpatterns = [
    path("", views.SatelliteView.as_view()),
    path("by_zone", views.SatelliteByZone.as_view())
]
