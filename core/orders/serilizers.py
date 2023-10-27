from typing import List

from rest_framework import serializers

from orders.models import OrderModel


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = '__all__'
