from django.urls import path

from orders import views

urlpatterns = [
    path("", views.CreateOrderAPIView.as_view()),
    path("orders/", views.ListOrderView.as_view()),
    path("tarifs/", views.GetAllTarifsAPIView.as_view()),
    path("plugins/", views.GetAllPluginsAPIView.as_view()),

]
