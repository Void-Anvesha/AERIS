"""Nearby Analyzer module to detect infrastructure within spatial radius."""

from typing import List, Dict, Any
from app.core.logging import logger
from app.services.geospatial.geo_utils import haversine_distance


class NearbyAnalyzer:
    """Analyzer for detecting nearby infrastructure and environmental objects around coordinates."""

    INFRASTRUCTURE_CATEGORIES = [
        "schools",
        "hospitals",
        "industries",
        "roads",
        "parks",
        "construction sites"
    ]

    def __init__(self, search_radius_km: float = 5.0) -> None:
        """Initialize the NearbyAnalyzer.

        Args:
            search_radius_km: Radius in kilometers within which to detect objects.
        """
        self.search_radius_km = search_radius_km
        logger.info(f"Initializing NearbyAnalyzer with search radius {search_radius_km} km.")

    def detect_nearby_objects(self, latitude: float, longitude: float) -> List[Dict[str, Any]]:
        """Detect infrastructure objects near given coordinates.

        Args:
            latitude: Target latitude coordinate.
            longitude: Target longitude coordinate.

        Returns:
            List of detected infrastructure dictionaries containing category, name, distance_km, and location.
        """
        logger.info(f"Detecting nearby infrastructure objects for coordinate: ({latitude}, {longitude})")

        # Realistic offset coordinates for generated mock infrastructure around target point
        mock_templates = [
            {
                "category": "schools",
                "name": "St. Jude Public Academy",
                "lat_offset": 0.004,
                "lon_offset": 0.003,
                "details": "Educational institute (Primary & Secondary)"
            },
            {
                "category": "hospitals",
                "name": "City General Multi-Specialty Hospital",
                "lat_offset": -0.005,
                "lon_offset": 0.006,
                "details": "Major regional healthcare center with ER"
            },
            {
                "category": "industries",
                "name": "Apex Chemical & Processing Plant",
                "lat_offset": 0.012,
                "lon_offset": -0.008,
                "details": "Industrial manufacturing facility (Potential AQI source)"
            },
            {
                "category": "roads",
                "name": "NH-48 Arterial Expressway Corridor",
                "lat_offset": -0.002,
                "lon_offset": -0.003,
                "details": "Heavy vehicular traffic highway"
            },
            {
                "category": "parks",
                "name": "Greenwood Botanical Eco Park",
                "lat_offset": -0.008,
                "lon_offset": -0.005,
                "details": "Urban green space and biodiversity reserve"
            },
            {
                "category": "construction sites",
                "name": "Metro Line Extension Construction Site",
                "lat_offset": 0.003,
                "lon_offset": -0.004,
                "details": "Active civil construction site (Dust source)"
            }
        ]

        results = []
        for tmpl in mock_templates:
            obj_lat = round(latitude + tmpl["lat_offset"], 6)
            obj_lon = round(longitude + tmpl["lon_offset"], 6)
            dist = haversine_distance(latitude, longitude, obj_lat, obj_lon)

            if dist <= self.search_radius_km:
                results.append({
                    "category": tmpl["category"],
                    "name": tmpl["name"],
                    "distance_km": dist,
                    "location": {
                        "latitude": obj_lat,
                        "longitude": obj_lon
                    },
                    "details": tmpl["details"]
                })

        logger.info(f"Detected {len(results)} nearby infrastructure objects.")
        return results
