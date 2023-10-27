from typing import List

from rest_framework import serializers

from orders.models import OrderModel, TarifModel


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = '__all__'


class TarifSerializer(serializers.ModelSerializer):
    class Meta:
        model = TarifModel
        fields = '__all__'