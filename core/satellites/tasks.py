import math
from datetime import datetime, timedelta
from typing import Tuple

from .models import SatelliteModel, PositionModel

from celery import shared_task
from celery.utils.log import get_task_logger

from orbit_predictor.sources import get_predictor_from_tle_lines


logger = get_task_logger(__name__)


def ecef_to_llh(x: float, y: float, z: float) -> Tuple[float, float]:
    """
    Converts ECEF coordinates to LLH

    :param x: ECEF x coord
    :param y: ECEF y coord
    :param z: ECEF z coord
    :return: (latitude, longitude)
    """

    # Constants
    a = 6378137.0
    b = 6356752.314245
    e_sq = 0.00669437999014

    # Calculation
    p = math.sqrt(x ** 2 + y ** 2)
    theta = math.atan2(z * a, p * b)
    lon = math.atan2(y, x)
    lat = math.atan2(z + e_sq*b*math.sin(theta)**3, p - e_sq*a*math.cos(theta)**3)
    return math.degrees(lat), math.degrees(lon)


@shared_task
def update_positions():
    minutes_in_month = 30 * 24 * 60

    logger.info("Start updating positions")

    positions_dates = [datetime.now() + timedelta(minutes=delta_minute)
                       for delta_minute in range(minutes_in_month + 1)]
    satellites = SatelliteModel.objects.filter(is_active=True).all()
    positions = []
    for satellite in satellites:
        logger.info(f"Calculating positions of satellite {satellite.object_id}")

        predictor = get_predictor_from_tle_lines(satellite.tle_lines)
        for date in positions_dates:
            ll_coords = ecef_to_llh(*predictor.get_only_position(date))

            position = PositionModel()
            position.lat, position.lon = ll_coords
            position.createdAt = date
            position.satellite = satellite
            positions.append(position)

    PositionModel.objects.bulk_create(positions)
    logger.info("Successfully calculated positions")
