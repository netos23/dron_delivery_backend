import math
import time
from datetime import datetime, timedelta
from typing import Tuple, Literal

from django.utils import timezone
from django.contrib.gis.geos import Point

from .models import SatelliteModel, PositionModel

from celery import shared_task
from celery.utils.log import get_task_logger

from orbit_predictor.sources import get_predictor_from_tle_lines


logger = get_task_logger(__name__)


class TLESatelliteRepr:
    """
    Representation SatelliteModel TLE params as TLE fields
    """
    _satellite: SatelliteModel

    # Constants
    SECONDS_IN_DAY = 24 * 60 * 60
    _STR1_TEMPLATE = "1 {}{} {} {}{} {} {} {} {} {}"
    _STR2_TEMPLATE = "2 {} {} {} {} {} {} {}{}"

    def __init__(self, satellite: SatelliteModel):
        self._satellite = satellite

    @property
    def norad_id(self) -> str:
        norad_s = str(self._satellite.norad_id)
        return " " * (5 - len(norad_s)) + norad_s

    @property
    def epoch_day(self) -> str:
        epoch_day = self._satellite.epoch.timetuple().tm_yday + \
                    (self._satellite.epoch.hour * 60 * 60 +
                     self._satellite.epoch.minute * 60 + self._satellite.epoch.second) / self.SECONDS_IN_DAY
        str_epoch_day = f"{epoch_day:3.8f}"
        return "0" * (12 - len(str_epoch_day)) + str_epoch_day

    @property
    def epoch_year(self) -> str:
        return str(self._satellite.epoch.year)[-2:]

    @property
    def international_designator(self) -> str:
        int_design = self._satellite.int_design
        return int_design + " " * (8 - len(int_design))

    @property
    def classification(self) -> Literal["U", "S", "C"]:
        return self._satellite.classification_type

    @property
    def mean_motion_dot(self) -> str:
        sign = " " if self._satellite.mean_motion_dot >= 0 else "-"
        float_repr = f"{abs(self._satellite.mean_motion_dot):.8f}"
        return f"{sign}{float_repr[1:]}"

    @property
    def mean_motion_ddot(self) -> str:
        return self._get_as_exponential_str(self._satellite.mean_motion_ddot)

    @property
    def bstar(self) -> str:
        return self._get_as_exponential_str(self._satellite.bstar)

    @property
    def ephemeris_type(self) -> str:
        return str(self._satellite.ephemeris_type)

    @property
    def element_number(self) -> str:
        str_number = str(self._satellite.element_number)
        return " " * (4 - len(str_number)) + str_number

    @property
    def inc(self) -> str:
        s = format(self._satellite.inclination, "3.4f")
        return " " * (8 - len(s)) + s

    @property
    def ra_of_an(self) -> str:
        s = format(self._satellite.ra_of_asc_node, "3.4f")
        return " " * (8 - len(s)) + s

    @property
    def eccentricity(self) -> str:
        s = format(self._satellite.eccentricity, ".7f")
        return s[2:]

    @property
    def arg_of_perigee(self) -> str:
        s = format(self._satellite.arg_of_pericenter, "3.4f")
        return " " * (8 - len(s)) + s

    @property
    def mean_anomaly(self) -> str:
        s = format(self._satellite.mean_anomaly, "3.4f")
        return " " * (8 - len(s)) + s

    @property
    def mean_motion(self) -> str:
        s = format(self._satellite.mean_motion, "2.8f")
        return " " * (11 - len(s)) + s

    @property
    def rev_num(self) -> str:
        s = str(self._satellite.rev_at_epoch)
        return "0" * (5 - len(s)) + s

    @staticmethod
    def _get_as_exponential_str(num: float) -> str:
        scientific_format = format(abs(num), "e")
        scientific_format = scientific_format.replace("e", "").replace(".", "")
        pow_ = int(scientific_format[-2:])
        if pow_ > 0:
            scientific_format = scientific_format[:-2] + str(pow_ - 1)
        sign = " " if num >= 0 else "-"
        return sign + scientific_format[:5] + "-" + scientific_format[-1:]

    @staticmethod
    def _get_control_sum(tle_str: str) -> int:
        control_sum = 0
        for ch in tle_str:
            if ch.isdigit():
                control_sum += int(ch)
            elif ch == "-":
                control_sum += 1
        return control_sum % 10

    @property
    def tle_string1(self) -> str:
        s = self._STR1_TEMPLATE.format(
            self.norad_id,
            self.classification,
            self.international_designator,
            self.epoch_year,
            self.epoch_day,
            self.mean_motion_dot,
            self.mean_motion_ddot,
            self.bstar,
            self.ephemeris_type,
            self.element_number
        )
        return s + str(self._get_control_sum(s))

    @property
    def tle_string2(self) -> str:
        s = self._STR2_TEMPLATE.format(
            self.norad_id,
            self.inc,
            self.ra_of_an,
            self.eccentricity,
            self.arg_of_perigee,
            self.mean_anomaly,
            self.mean_motion,
            self.rev_num
        )
        return s + str(self._get_control_sum(s))

    @property
    def tle(self) -> Tuple[str, str]:
        return self.tle_string1, self.tle_string2


def _update_positions(days=30):
    seconds_in_month = int(days * 24 * 60 * 60)

    logger.info("Start updating positions")
    start_time = time.time()

    positions_dates = [timezone.now() + timedelta(seconds=delta_second)
                       for delta_second in range(seconds_in_month + 1)]
    satellites = SatelliteModel.objects.filter(is_active=True).all()

    for satellite in satellites:
        positions = []
        logger.info(f"Calculating positions of satellite {satellite.object_id}")

        tle_repr = TLESatelliteRepr(satellite)
        predictor = get_predictor_from_tle_lines(tle_repr.tle)
        begin_datetime = positions_dates[0]
        for date in positions_dates:
            if date - begin_datetime >= timedelta(hours=1):
                PositionModel.objects.bulk_create(positions)
                positions = []
                begin_datetime = date

            ll_coords = predictor.get_position(date).position_llh[:2]
            position = PositionModel()
            position.lat, position.lon = ll_coords
            position.point = Point(*ll_coords)
            position.created_at = date
            position.satellite = satellite
            positions.append(position)

        if positions:
            PositionModel.objects.bulk_create(positions)

    logger.info(f"Successfully calculated positions. Time: {time.time() - start_time:.2f}")


@shared_task
def update_positions():
    _update_positions()
