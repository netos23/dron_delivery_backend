from rest_framework import generics

from orders.models import OrderModel, TarifModel
from orders.serilizers import OrderSerializer, TarifSerializer


# Create your views here.
class CreateOrderAPIView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    queryset = OrderModel.objects.all()


class ListOrderView(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = OrderModel.objects.all()

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return OrderModel.objects.filter(user=user)


class GetAllTarifsAPIView(generics.ListAPIView):
    serializer_class = TarifSerializer
    queryset = TarifModel.objects.all()
