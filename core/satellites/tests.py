import pytz
from datetime import datetime

from django.test import TestCase

from satellites.models import SatelliteModel, PositionModel
from satellites.tasks import _update_positions


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

    def test_update_positions(self):
        _update_positions()
        self.assertGreater(PositionModel.objects.count(), 0)
        pos = PositionModel.objects.first()
        print("Longitude: {:.2f}\n"
              "Latitude: {:.2f}\n"
              "When: {}\n"
              "Sat name: {}".format(pos.lon, pos.lat,
                                    pos.createdAt.strftime("%a %b %d %H:%M:%S %Y"),
                                    pos.satellite.object_name))