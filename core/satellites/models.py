from django.db import models


class SatelliteModel(models.Model):
    bject_name = models.CharField(max_length=50)
    object_id = models.CharField(max_length=20)
    epoch = models.DateTimeField()
    mean_motion = models.FloatField()
    eccentricity = models.FloatField()
    inclination = models.FloatField()
    ra_of_asc_node = models.FloatField()
    arg_of_pericenter = models.FloatField()
    mean_anomaly = models.FloatField()
    ephemeris_type = models.IntegerField()
    classification_type = models.CharField(max_length=1)
    norad_cat_id = models.IntegerField()
    element_set_no = models.IntegerField()
    rev_at_epoch = models.IntegerField()
    bstar = models.FloatField()
    mean_motion_dot = models.FloatField()
    mean_motion_ddot = models.FloatField()
    is_active = models.BooleanField(default=True)
    resolution = models.FloatField()


class PositionModel(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    createdAt = models.DateTimeField()
    satellite = models.ForeignKey(SatelliteModel, on_delete=models.CASCADE)
