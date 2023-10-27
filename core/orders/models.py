from django.db import models
from django.utils.timezone import now

from authorization.models import Users
from geozones.models import GeozoneModel
from satellites.models import SatelliteModel


# Create your models here.
class TarifModel(models.Model):
    name = models.CharField(max_length=50)
    base_price = models.FloatField()
    per_photo = models.FloatField()
    description = models.CharField(max_length=255)
    picture = models.URLField(null=True)


class OrderModel(models.Model):
    STATUS_TYPE_CHOICES = [
        (0, "Created"),
        (1, "Data collected"),
        (2, "Done")
    ]

    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    geozone = models.ForeignKey(GeozoneModel, on_delete=models.SET_NULL, null=True)
    satellites = models.ManyToManyField(SatelliteModel)
    date_begin = models.DateTimeField()
    date_end = models.DateTimeField()
    created_at = models.DateTimeField(default=now)
    tarif = models.ForeignKey(TarifModel, on_delete=models.SET_NULL, null=True)
    price = models.FloatField()
    status = models.IntegerField(default=0, choices=STATUS_TYPE_CHOICES)
