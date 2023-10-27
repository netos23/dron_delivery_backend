from django.urls import path

from geozones import views

urlpatterns = [
    path("deprecated/", views.DeprecatedGeozoneView.as_view()),
    path("zones/", views.GeozoneView.as_view()),
]
