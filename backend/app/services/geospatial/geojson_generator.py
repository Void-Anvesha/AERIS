"""GeoJSON Generator module for creating compliant GeoJSON FeatureCollections."""

from typing import Dict, Any, List
from app.core.logging import logger


class GeoJSONGenerator:
    """Generator for standard RFC 7946 GeoJSON FeatureCollections."""

    def generate_feature_collection(
        self,
        latitude: float,
        longitude: float,
        aqi: float,
        date_str: str,
        admin_info: Dict[str, Any],
        nearby_objects: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate GeoJSON FeatureCollection containing target location and nearby objects.

        Args:
            latitude: Target latitude coordinate.
            longitude: Target longitude coordinate.
            aqi: Air Quality Index value.
            date_str: Analysis date string (YYYY-MM-DD).
            admin_info: Administrative metadata (ward, district, zone, etc.).
            nearby_objects: List of nearby infrastructure objects.

        Returns:
            Dict conforming to GeoJSON FeatureCollection format.
        """
        logger.info("Generating GeoJSON FeatureCollection.")

        features = []

        # Target monitoring point feature
        target_feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [longitude, latitude]  # GeoJSON specifies [longitude, latitude]
            },
            "properties": {
                "name": "Target Air Quality Station",
                "aqi": aqi,
                "date": date_str,
                "ward": admin_info.get("ward"),
                "district": admin_info.get("district"),
                "zone": admin_info.get("zone"),
                "population_density": admin_info.get("population_density"),
                "is_target": True
            }
        }
        features.append(target_feature)

        # Nearby infrastructure features
        node_coords = []
        for obj in nearby_objects:
            obj_loc = obj.get("location", {})
            o_lat = obj_loc.get("latitude", 0.0)
            o_lon = obj_loc.get("longitude", 0.0)
            node_coords.append([o_lon, o_lat])

            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [o_lon, o_lat]
                },
                "properties": {
                    "name": obj.get("name"),
                    "category": obj.get("category"),
                    "distance_km": obj.get("distance_km"),
                    "details": obj.get("details"),
                    "is_target": False
                }
            }
            features.append(feature)

        # Spatial Grid Net Network Feature (MultiLineString edges)
        if node_coords:
            star_lines = [[[longitude, latitude], n_coord] for n_coord in node_coords]
            ring_line = node_coords + [node_coords[0]] if len(node_coords) >= 2 else []
            all_mesh_lines = star_lines + ([ring_line] if ring_line else [])

            net_feature = {
                "type": "Feature",
                "geometry": {
                    "type": "MultiLineString",
                    "coordinates": all_mesh_lines
                },
                "properties": {
                    "name": "Spatial Pollution Monitoring Mesh Grid Network",
                    "type": "spatial_mesh_grid",
                    "edge_count": len(all_mesh_lines)
                }
            }
            features.append(net_feature)

        feature_collection = {
            "type": "FeatureCollection",
            "features": features
        }

        logger.debug(f"GeoJSON generated with {len(features)} total features.")
        return feature_collection
