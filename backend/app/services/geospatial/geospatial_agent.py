"""Geospatial Intelligence Agent module for urban air quality spatial analysis."""

from datetime import date
from typing import Dict, Any, Union, List
from pydantic import BaseModel, Field, field_validator

from app.core.exceptions import ValidationError, AERISException
from app.core.logging import logger
from app.services.geospatial.geo_utils import validate_coordinates
from app.services.geospatial.reverse_geocoder import ReverseGeocoder
from app.services.geospatial.nearby_analyzer import NearbyAnalyzer
from app.services.geospatial.geojson_generator import GeoJSONGenerator
from app.services.geospatial.kml_generator import KMLGenerator


class GeospatialInput(BaseModel):
    """Pydantic model for input data to the Geospatial Agent."""
    latitude: float = Field(..., description="Latitude coordinate (-90 to 90)")
    longitude: float = Field(..., description="Longitude coordinate (-180 to 180)")
    aqi: float = Field(..., ge=0.0, description="Air Quality Index value")
    date: str = Field(..., description="Date of observation in YYYY-MM-DD format")

    @field_validator("date")
    @classmethod
    def validate_date_format(cls, value: str) -> str:
        """Validate YYYY-MM-DD date string format."""
        try:
            date.fromisoformat(value)
        except ValueError:
            raise ValueError("date must be a valid date string in YYYY-MM-DD format")
        return value


from typing import Dict, Any, Union, List, Optional
import os


class GeospatialOutput(BaseModel):
    """Pydantic model for output response from the Geospatial Agent."""
    ward: str = Field(..., description="Ward boundary identifier")
    district: str = Field(..., description="District administrative area")
    zone: str = Field(..., description="Zone identifier")
    population_density: str = Field(..., description="Estimated population density")
    nearby_objects: List[Dict[str, Any]] = Field(..., description="Detected nearby infrastructure objects")
    geojson: Dict[str, Any] = Field(..., description="GeoJSON FeatureCollection payload")
    kml_path: str = Field(..., description="Path to generated KML export file")
    kml_url: Optional[str] = Field(default=None, description="Public URL route for Google Maps KML Layer rendering")
    confidence: float = Field(default=0.95, ge=0.0, le=1.0, description="Confidence score of spatial analysis")


class GeospatialAgent:
    """Geospatial Intelligence Agent for analyzing spatial urban contexts for air quality monitoring."""

    def __init__(self) -> None:
        """Initialize the Geospatial Agent and its processing services."""
        logger.info("Initializing GeospatialAgent instance.")
        self.reverse_geocoder = ReverseGeocoder()
        self.nearby_analyzer = NearbyAnalyzer()
        self.geojson_generator = GeoJSONGenerator()
        self.kml_generator = KMLGenerator()

    def analyze_location(self, input_data: Union[Dict[str, Any], GeospatialInput]) -> Dict[str, Any]:
        """Perform end-to-end geospatial analysis on a target location.

        The analysis pipeline executes the following steps:
        1. Validate coordinates.
        2. Reverse geocode coordinates.
        3. Generate Ward / District / Zone & density mapping.
        4. Detect nearby infrastructure (schools, hospitals, industries, roads, parks, construction sites).
        5. Generate GeoJSON FeatureCollection.
        6. Generate KML export.
        7. Return structured response.

        Args:
            input_data: Dictionary or GeospatialInput instance containing latitude, longitude, aqi, and date.

        Returns:
            Structured dictionary matching the required Geospatial analysis response.

        Raises:
            ValidationError: If input validation fails.
            AERISException: If processing error occurs during spatial pipeline execution.
        """
        logger.info(f"Starting analyze_location execution for input: {input_data}")

        try:
            # Step 0: Input schema validation
            if isinstance(input_data, dict):
                try:
                    parsed_input = GeospatialInput(**input_data)
                except Exception as ve:
                    logger.error(f"Input schema validation error: {str(ve)}")
                    raise ValidationError(f"Invalid input schema: {str(ve)}")
            elif isinstance(input_data, GeospatialInput):
                parsed_input = input_data
            else:
                raise ValidationError("Input must be a dictionary or GeospatialInput instance.")

            # Step 1: Validate coordinates
            validate_coordinates(parsed_input.latitude, parsed_input.longitude)

            # Step 2 & 3: Reverse geocode & Administrative boundary lookup
            admin_info = self.reverse_geocoder.reverse_geocode(
                parsed_input.latitude,
                parsed_input.longitude
            )

            # Step 4: Detect nearby infrastructure
            nearby_objects = self.nearby_analyzer.detect_nearby_objects(
                parsed_input.latitude,
                parsed_input.longitude
            )

            # Step 5: Generate GeoJSON FeatureCollection
            geojson_payload = self.geojson_generator.generate_feature_collection(
                latitude=parsed_input.latitude,
                longitude=parsed_input.longitude,
                aqi=parsed_input.aqi,
                date_str=parsed_input.date,
                admin_info=admin_info,
                nearby_objects=nearby_objects
            )

            # Step 6: Generate KML export
            kml_filepath = self.kml_generator.generate_kml(
                latitude=parsed_input.latitude,
                longitude=parsed_input.longitude,
                aqi=parsed_input.aqi,
                date_str=parsed_input.date,
                admin_info=admin_info,
                nearby_objects=nearby_objects
            )

            # Derive public web URL for Google Maps KML Layer integration
            kml_filename = os.path.basename(kml_filepath)
            kml_web_url = f"/exports/kml/{kml_filename}"

            # Step 7: Construct & return structured response
            output_model = GeospatialOutput(
                ward=admin_info["ward"],
                district=admin_info["district"],
                zone=admin_info["zone"],
                population_density=admin_info["population_density"],
                nearby_objects=nearby_objects,
                geojson=geojson_payload,
                kml_path=kml_filepath,
                kml_url=kml_web_url,
                confidence=0.95
            )

            logger.info(f"Geospatial location analysis completed successfully for ({parsed_input.latitude}, {parsed_input.longitude}).")
            return output_model.model_dump()

        except ValidationError:
            raise
        except Exception as e:
            logger.exception(f"Unexpected error during geospatial location analysis: {str(e)}")
            raise AERISException(f"Geospatial analysis failed: {str(e)}")
