import pytz
from datetime import datetime, timedelta
from typing import List

from django.test import TestCase
from django.db.models import Q

from satellites.models import SatelliteModel, PositionModel
from satellites.tasks import _update_positions
from geozones.models import GeozoneModel


class CalcPositionsTest(TestCase):
    def setUp(self):
        sat = SatelliteModel()

        sat.object_name = "ISS"
        sat.resolution = 0

        sat.norad_id = 25544
        sat.classification_type = "U"
        sat.int_design = "98067A"
        sat.epoch = datetime(year=2008, day=20, month=9, hour=12,
                             minute=25, second=40, tzinfo=pytz.UTC)
        sat.element_number = 292
        sat.bstar = -0.11606e-4
        sat.mean_motion_dot = -0.00002182
        sat.mean_motion_ddot = 0
        sat.inclination = 51.6416
        sat.ra_of_asc_node = 247.4627
        sat.eccentricity = 0.006703
        sat.arg_of_pericenter = 130.536
        sat.mean_anomaly = 325.0288
        sat.mean_motion = 15.72125391
        sat.rev_at_epoch = 56353
        sat.save()

        _update_positions(0.1)

    def test_update_positions(self):
        self.assertGreater(PositionModel.objects.count(), 0)
        pos = PositionModel.objects.first()
        print("Longitude: {:.2f}\n"
              "Latitude: {:.2f}\n"
              "When: {}\n"
              "Sat name: {}".format(pos.lon, pos.lat,
                                    pos.created_at.strftime("%a %b %d %H:%M:%S %Y"),
                                    pos.satellite.object_name))

    def test_find_satellite_by_geozone(self):
        pos = PositionModel.objects.first()
        last_date = pos.created_at - timedelta(days=1)
        future_date = pos.created_at + timedelta(days=1)

        geozone = GeozoneModel()
        geozone.wkt = f"POLYGON (({pos.lat - 1} {pos.lon - 1}, {pos.lat + 1} " \
                      f"{pos.lon - 1}, {pos.lat + 1} {pos.lon + 1}, " \
                      f"{pos.lat - 1} {pos.lon + 1}, {pos.lat - 1} {pos.lon - 1}))"
        geozone.name = "test"
        geozone.save()
        self.assertTrue(geozone.geom.contains(pos.point))
        self.assertGreater(len(self.get_positions(geozone.geom, last_date)), 0)
        self.assertEqual(len(self.get_positions(geozone.geom, future_date)), 0)

    @staticmethod
    def get_positions(polygon, date) -> List[PositionModel]:
        return PositionModel.objects.filter(Q(point__within=polygon) & Q(created_at__gte=date)).all()
