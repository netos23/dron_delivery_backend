from rest_framework import generics

from orders.models import OrderModel, TarifModel
from orders.serilizers import OrderSerializer, TarifSerializer


# Create your views here.
class CreateOrderAPIView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    queryset = OrderModel.objects.all()


class GetAllTarifsAPIView(generics.ListAPIView):
    serializer_class = TarifSerializer
    queryset = TarifModel.objects.all()