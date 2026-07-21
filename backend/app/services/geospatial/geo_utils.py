"""Geospatial utility functions for coordinate validation and spatial calculation."""

import math
from app.core.exceptions import ValidationError
from app.core.logging import logger


def validate_coordinates(latitude: float, longitude: float) -> None:
    """Validate latitude and longitude values.

    Args:
        latitude: Latitude in decimal degrees (-90.0 to 90.0).
        longitude: Longitude in decimal degrees (-180.0 to 180.0).

    Raises:
        ValidationError: If coordinates are out of valid range or invalid type.
    """
    if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
        logger.error(f"Invalid coordinate type: lat={type(latitude)}, lon={type(longitude)}")
        raise ValidationError("Latitude and longitude must be floating point numbers or integers.")

    if math.isnan(latitude) or math.isnan(longitude) or math.isinf(latitude) or math.isinf(longitude):
        logger.error(f"Infinite or NaN coordinates received: lat={latitude}, lon={longitude}")
        raise ValidationError("Coordinates cannot be NaN or infinite values.")

    if not (-90.0 <= latitude <= 90.0):
        logger.error(f"Latitude out of bounds: {latitude}")
        raise ValidationError(f"Latitude must be between -90.0 and 90.0 degrees. Got {latitude}")

    if not (-180.0 <= longitude <= 180.0):
        logger.error(f"Longitude out of bounds: {longitude}")
        raise ValidationError(f"Longitude must be between -180.0 and 180.0 degrees. Got {longitude}")

    logger.debug(f"Coordinates validated successfully: lat={latitude}, lon={longitude}")


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great-circle distance between two points on the Earth in kilometers.

    Args:
        lat1: Latitude of point 1.
        lon1: Longitude of point 1.
        lat2: Latitude of point 2.
        lon2: Longitude of point 2.

    Returns:
        Distance in kilometers.
    """
    r = 6371.0  # Earth's radius in kilometers

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    return round(r * c, 3)
