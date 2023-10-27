from django.test import TestCase

from geozones.models import GeozoneModel, DeprecatedGeozoneModel
from django.contrib.gis.geos.point import Point


class GeozoneTest(TestCase):
    geozone: GeozoneModel
    depr_geo: DeprecatedGeozoneModel
    point1 = Point(0.75, 0.75)
    point2 = Point(2, 2)

    def setUp(self):
        geozone = GeozoneModel()
        geozone.wkt = "POLYGON ((0 0, 1.5 0, 1.5 1, 0 1.5, 0 0))"
        geozone.name = "test"
        geozone.save()
        self.geozone = geozone

        depr_geo = DeprecatedGeozoneModel()
        depr_geo.wkt = "POLYGON ((0 0, 1.5 0, 1.5 1, 0 1.5, 0 0))"
        depr_geo.name = "test"
        depr_geo.save()
        self.depr_geo = depr_geo

    def test_field(self):
        geo = self.geozone
        self.assertTrue(geo.geom.contains(self.point1))
        self.assertFalse(geo.geom.contains(self.point2))

    def test_query(self):
        geo_original = self.geozone
        geo1 = GeozoneModel.objects.filter(geom__contains=self.point1).first()
        self.assertEqual(geo_original, geo1)
        geo2 = GeozoneModel.objects.exclude(geom__contains=self.point2).first()
        self.assertEqual(geo_original, geo2)

        dgeo_original = self.depr_geo
        dgeo1 = DeprecatedGeozoneModel.objects.filter(geom__contains=self.point1).first()
        self.assertEqual(dgeo_original, dgeo1)
        dgeo2 = DeprecatedGeozoneModel.objects.exclude(geom__contains=self.point2).first()
        self.assertEqual(dgeo_original, dgeo2)
