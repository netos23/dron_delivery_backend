from django.db import models
from django.contrib.gis.geos import GEOSGeometry, Point, MultiPolygon
from django.contrib.gis.db import models
from authorization.models import Users


class GeozoneModel(models.Model):
    geom = models.MultiPolygonField(srid=4326)
    wkt = models.TextField()
    name = models.CharField(max_length=50)
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if getattr(self, 'wkt'):
            self.geom = MultiPolygon(self.wkt)
        super(GeozoneModel, self).save(*args, **kwargs)


class DeprecatedGeozoneModel(models.Model):
    geom = models.MultiPolygonField(srid=4326)
    wkt = models.TextField()
    name = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if getattr(self, 'wkt'):
            self.geom = MultiPolygon(self.wkt)
        super(DeprecatedGeozoneModel, self).save(*args, **kwargs)
