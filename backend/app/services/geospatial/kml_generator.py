"""KML Generator module to generate KML XML exports for spatial visualization."""

import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Dict, Any, List
from app.core.logging import logger


class KMLGenerator:
    """Generator for KML (Keyhole Markup Language) XML files."""

    def __init__(self, output_dir: str = "exports/kml") -> None:
        """Initialize KML Generator with output directory.

        Args:
            output_dir: Directory path where generated KML files will be saved.
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info(f"Initialized KMLGenerator with output directory: {self.output_dir}")

    def generate_kml(
        self,
        latitude: float,
        longitude: float,
        aqi: float,
        date_str: str,
        admin_info: Dict[str, Any],
        nearby_objects: List[Dict[str, Any]]
    ) -> str:
        """Generate KML document and save to file path.

        Args:
            latitude: Target latitude coordinate.
            longitude: Target longitude coordinate.
            aqi: Air Quality Index value.
            date_str: Analysis date string (YYYY-MM-DD).
            admin_info: Administrative metadata dictionary.
            nearby_objects: List of nearby infrastructure objects.

        Returns:
            Absolute or relative path string to the generated KML file.
        """
        logger.info(f"Generating KML export for coordinates ({latitude}, {longitude})")

        kml_elem = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
        doc_elem = ET.SubElement(kml_elem, "Document")

        name_elem = ET.SubElement(doc_elem, "name")
        name_elem.text = f"AERIS Air Quality Intelligence - {date_str}"

        desc_elem = ET.SubElement(doc_elem, "description")
        desc_elem.text = (
            f"AQI Analysis Report for Ward: {admin_info.get('ward')}, "
            f"District: {admin_info.get('district')}, Zone: {admin_info.get('zone')}"
        )

        # Target Placemark
        target_pm = ET.SubElement(doc_elem, "Placemark")
        target_name = ET.SubElement(target_pm, "name")
        target_name.text = f"Target Station (AQI: {aqi})"

        target_desc = ET.SubElement(target_pm, "description")
        target_desc.text = (
            f"AQI: {aqi}\nDate: {date_str}\nWard: {admin_info.get('ward')}\n"
            f"District: {admin_info.get('district')}\nZone: {admin_info.get('zone')}\n"
            f"Population Density: {admin_info.get('population_density')}"
        )

        target_point = ET.SubElement(target_pm, "Point")
        target_coords = ET.SubElement(target_point, "coordinates")
        target_coords.text = f"{longitude},{latitude},0"

        # Nearby Objects Placemarks
        nearby_folder = ET.SubElement(doc_elem, "Folder")
        folder_name = ET.SubElement(nearby_folder, "name")
        folder_name.text = "Nearby Infrastructure"

        node_coords = []
        for obj in nearby_objects:
            pm = ET.SubElement(nearby_folder, "Placemark")
            pm_name = ET.SubElement(pm, "name")
            pm_name.text = f"[{obj.get('category').upper()}] {obj.get('name')}"

            pm_desc = ET.SubElement(pm, "description")
            pm_desc.text = (
                f"Category: {obj.get('category')}\n"
                f"Distance: {obj.get('distance_km')} km\n"
                f"Details: {obj.get('details')}"
            )

            obj_loc = obj.get("location", {})
            obj_lat = obj_loc.get("latitude", 0.0)
            obj_lon = obj_loc.get("longitude", 0.0)
            node_coords.append((obj_lon, obj_lat))

            pm_point = ET.SubElement(pm, "Point")
            pm_coords = ET.SubElement(pm_point, "coordinates")
            pm_coords.text = f"{obj_lon},{obj_lat},0"

        # Network Mesh / Net Structure Folder
        mesh_folder = ET.SubElement(doc_elem, "Folder")
        mesh_name = ET.SubElement(mesh_folder, "name")
        mesh_name.text = "Spatial Network Mesh"

        # 1. Star vectors connecting target station to each nearby node
        for i, (n_lon, n_lat) in enumerate(node_coords):
            line_pm = ET.SubElement(mesh_folder, "Placemark")
            line_name = ET.SubElement(line_pm, "name")
            line_name.text = f"Mesh Edge: Target -> Node #{i+1}"
            
            line_elem = ET.SubElement(line_pm, "LineString")
            tess_elem = ET.SubElement(line_elem, "tessellate")
            tess_elem.text = "1"
            
            line_coords = ET.SubElement(line_elem, "coordinates")
            line_coords.text = f"{longitude},{latitude},0 {n_lon},{n_lat},0"

        # 2. Outer ring net edges connecting adjacent nodes
        if len(node_coords) >= 2:
            ring_pm = ET.SubElement(mesh_folder, "Placemark")
            ring_name = ET.SubElement(ring_pm, "name")
            ring_name.text = "Spatial Perimeter Grid Network"
            
            ring_line = ET.SubElement(ring_pm, "LineString")
            ring_tess = ET.SubElement(ring_line, "tessellate")
            ring_tess.text = "1"
            
            ring_coords_str = " ".join([f"{n_lon},{n_lat},0" for n_lon, n_lat in node_coords])
            # Close ring
            ring_coords_str += f" {node_coords[0][0]},{node_coords[0][1]},0"
            
            ring_coords = ET.SubElement(ring_line, "coordinates")
            ring_coords.text = ring_coords_str

        # Format XML cleanly
        xml_str = minidom.parseString(ET.tostring(kml_elem)).toprettyxml(indent="  ")

        filename = f"aeris_geospatial_{latitude}_{longitude}_{date_str}.kml".replace("-", "_")
        file_path = os.path.join(self.output_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(xml_str)

        logger.info(f"KML file successfully exported to {file_path}")
        return file_path
