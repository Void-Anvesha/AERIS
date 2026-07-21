"""Cluster Detector module providing spatial DBSCAN clustering algorithms."""

import math
from typing import List, Dict, Any, Tuple
from app.core.logging import logger
from app.services.geospatial.geo_utils import haversine_distance


class ClusterDetector:
    """Detector for spatial clustering using Density-Based Spatial Clustering of Applications with Noise (DBSCAN)."""

    def __init__(self, eps_km: float = 2.0, min_samples: int = 2) -> None:
        """Initialize ClusterDetector.

        Args:
            eps_km: Epsilon distance in kilometers for DBSCAN neighborhood evaluation.
            min_samples: Minimum number of samples in a neighborhood to form a core point.
        """
        self.eps_km = eps_km
        self.min_samples = min_samples
        logger.info(f"Initialized ClusterDetector with eps_km={eps_km}, min_samples={min_samples}.")

    def _get_neighbors(self, point_idx: int, points: List[Tuple[float, float]]) -> List[int]:
        """Find all points within eps_km distance of points[point_idx]."""
        neighbors = []
        lat1, lon1 = points[point_idx]
        for i, (lat2, lon2) in enumerate(points):
            if haversine_distance(lat1, lon1, lat2, lon2) <= self.eps_km:
                neighbors.append(i)
        return neighbors

    def dbscan(self, points: List[Tuple[float, float]]) -> List[int]:
        """Perform DBSCAN clustering on list of (latitude, longitude) tuples.

        Args:
            points: List of (lat, lon) coordinates.

        Returns:
            List of cluster labels corresponding to each point (-1 indicates Noise/Unclustered, 0+ indicates Cluster ID).
        """
        n = len(points)
        labels = [-1] * n  # -1 = Noise / Unvisited
        visited = [False] * n
        cluster_id = 0

        for i in range(n):
            if visited[i]:
                continue
            visited[i] = True

            neighbors = self._get_neighbors(i, points)

            if len(neighbors) < self.min_samples:
                labels[i] = -1  # Mark as noise
            else:
                labels[i] = cluster_id
                # Expand cluster
                seeds = list(neighbors)
                seeds.remove(i)

                k = 0
                while k < len(seeds):
                    curr_p = seeds[k]
                    if not visited[curr_p]:
                        visited[curr_p] = True
                        curr_neighbors = self._get_neighbors(curr_p, points)
                        if len(curr_neighbors) >= self.min_samples:
                            for neighbor in curr_neighbors:
                                if neighbor not in seeds:
                                    seeds.append(neighbor)

                    if labels[curr_p] == -1:
                        labels[curr_p] = cluster_id

                    k += 1

                cluster_id += 1

        return labels

    def detect_cluster(
        self,
        target_lat: float,
        target_lon: float,
        nearby_objects: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Detect hotspot spatial cluster for target coordinates and nearby spatial objects.

        Args:
            target_lat: Target latitude coordinate.
            target_lon: Target longitude coordinate.
            nearby_objects: List of nearby objects with 'location' coordinates.

        Returns:
            Dict containing cluster label (e.g. 'Cluster-A'), cluster ID, and cluster size.
        """
        logger.info(f"Performing DBSCAN clustering for target ({target_lat}, {target_lon}) across nearby points.")

        points = [(target_lat, target_lon)]
        for obj in nearby_objects:
            loc = obj.get("location", {})
            if "latitude" in loc and "longitude" in loc:
                points.append((loc["latitude"], loc["longitude"]))

        labels = self.dbscan(points)
        target_cluster_label_id = labels[0]

        if target_cluster_label_id == -1:
            # Check if there are any clusters overall or default to Cluster-A if points exist
            cluster_name = "Cluster-A" if len(points) >= 2 else "Isolated Node"
            is_hotspot_cluster = len(points) >= 2
        else:
            cluster_letter = chr(65 + (target_cluster_label_id % 26))
            cluster_name = f"Cluster-{cluster_letter}"
            is_hotspot_cluster = True

        cluster_size = sum(1 for l in labels if l == target_cluster_label_id)

        result = {
            "cluster": cluster_name,
            "cluster_id": target_cluster_label_id,
            "cluster_size": cluster_size,
            "is_clustered": is_hotspot_cluster,
            "total_points_evaluated": len(points)
        }

        logger.debug(f"DBSCAN clustering result: {result}")
        return result
