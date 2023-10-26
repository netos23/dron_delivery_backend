from django.db import models

from authorization.models import Users


class GeozoneModel(models.Model):
    wkt = models.TextField()
    name = models.CharField(max_length=50)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
