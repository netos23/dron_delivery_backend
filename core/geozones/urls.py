from django.urls import path

from geozones import views

urlpatterns = [
    path("", views.GeozoneView.as_view()),
]
