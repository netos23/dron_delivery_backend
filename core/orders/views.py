from django.shortcuts import render
from rest_framework import generics

from orders.models import OrderModel
from orders.serilizers import OrderSerializer


# Create your views here.
class CreateOrderAPIView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    queryset = OrderModel.objects.all()