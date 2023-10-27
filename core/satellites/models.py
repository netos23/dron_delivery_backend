from django.contrib.gis.db import models


class SatelliteModel(models.Model):
    CLASS_TYPE_CHOICES = [
        ("U", "Unclassified"),
        ("S", "Secret"),
        ("C", "Classified")
    ]

    object_name = models.CharField(max_length=50)
    object_id = models.CharField(max_length=20)

    # TLE params
    norad_id = models.IntegerField(verbose_name="Id in NORAD database")
    epoch = models.DateTimeField()
    mean_motion_dot = models.FloatField()
    mean_motion_ddot = models.FloatField()
    int_design = models.CharField(max_length=8, verbose_name="International Designator")
    classification_type = models.CharField(max_length=1, choices=CLASS_TYPE_CHOICES, default="U")
    bstar = models.FloatField(verbose_name="Bstar coefficient")
    ephemeris_type = models.IntegerField(default=0)
    element_number = models.IntegerField(default=999)
    inclination = models.FloatField()
    ra_of_asc_node = models.FloatField(verbose_name="Right Ascension of the Ascending Node")
    mean_motion = models.FloatField()
    eccentricity = models.FloatField()
    arg_of_pericenter = models.FloatField(verbose_name="Argument of Perigee")
    mean_anomaly = models.FloatField()
    rev_at_epoch = models.IntegerField()

    picture = models.URLField(null=True)
    is_active = models.BooleanField(default=True)
    resolution = models.FloatField()


class PositionModel(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    point = models.PointField(null=True, srid=4326)
    created_at = models.DateTimeField()
    satellite = models.ForeignKey(SatelliteModel, on_delete=models.CASCADE)
