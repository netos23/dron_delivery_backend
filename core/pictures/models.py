from django.db import models
from django.utils.timezone import now


class SatellitePictureModel(models.Model):
    link = models.CharField(max_length=256, null=True, blank=True)
    lat_1 = models.FloatField(null=True)
    lon_1 = models.FloatField(null=True)
    lat_2 = models.FloatField(null=True)
    lon_2 = models.FloatField(null=True)
    created_at = models.DateTimeField(default=now)
    expiration_date = models.DateTimeField(null=True)

    def __str__(self):
        return f'{str(self.link)}'


class PictureModel(models.Model):
    url = models.ImageField(max_length=256, upload_to='pictures/', null=True, blank=True)
    link = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return f'{str(self.url)}'
