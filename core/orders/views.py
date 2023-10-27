from rest_framework import generics, permissions, status
from rest_framework.response import Response

from orders.models import OrderModel, TarifModel, PluginModel
from orders.serilizers import OrderSerializer, TarifSerializer, RequestOrderSerializer, PluginSerializer
from rest_framework_simplejwt import authentication


# Create your views here.
class CreateOrderAPIView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthentication,)
    serializer_class = RequestOrderSerializer
    queryset = OrderModel.objects.all()


    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        data['user'] = request.user.id
        data['status'] = 0
        data['price'] = 0
        serializer = OrderSerializer(data=data)
        serializer.is_valid()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ListOrderView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthentication,)

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

class GetAllPluginsAPIView(generics.ListAPIView):
    serializer_class = PluginSerializer
    queryset = PluginModel.objects.all()
