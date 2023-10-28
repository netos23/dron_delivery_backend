from django.db import models
import uuid

from orders.models import OrderModel


class OrderPayModel(models.Model):
    class PayStatus(models.IntegerChoices):
        REGISTER = 0
        HOLD = 1
        PAID = 2
        CANCEL = 3
        REFUND = 4
        AUTH = 5
        BAD_AUTH = 6

        WAIT_COMMIT = 10
        COMMITED = 11
        REJECTED = 20

    class Method(models.TextChoices):
        SBER = 'sber'
        ALPHA = 'alpha'
        DOLYAME = 'doly'
        UKASSA = 'ukassa'
        CLOUD = 'cloudPay'
        PAYPAL = 'payPal'
        TEST = 'test'

    order = models.ForeignKey(OrderModel, on_delete=models.DO_NOTHING, related_name='payments')
    created_at = models.DateTimeField(auto_now_add=True)
    pay_method = models.CharField(choices=Method.choices, max_length=255)
    amount = models.IntegerField()
    status = models.IntegerField(choices=PayStatus.choices)
    bank_order_uid = models.CharField(max_length=255)
    bank_order_id = models.CharField(max_length=255)
    status_changed_at = models.DateTimeField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['bank_order_uid']),
            models.Index(fields=['bank_order_id']),
            models.Index(fields=['order'])
        ]


