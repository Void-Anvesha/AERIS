# Geospatial Intelligence Agent Service

The **Geospatial Intelligence Agent** provides urban spatial analysis for air quality monitoring within the AERIS platform. It validates target geographical coordinates, reverse-geocodes administrative boundaries, detects nearby sensitive infrastructure, and generates visualization exports in standard GeoJSON and KML formats.

---

## Directory Structure

```
app/services/geospatial/
├── README.md               # Service documentation
├── __init__.py             # Package exports (GeospatialAgent, GeospatialInput, GeospatialOutput)
├── geospatial_agent.py     # Core agent orchestrator exposing analyze_location(input)
├── geo_utils.py            # Coordinate validation and Haversine distance calculations
├── reverse_geocoder.py     # Reverse geocoding & administrative boundary lookup (Ward, District, Zone)
├── nearby_analyzer.py      # Spatial infrastructure detection (schools, hospitals, industries, etc.)
├── geojson_generator.py    # Standard RFC 7946 GeoJSON FeatureCollection generator
└── kml_generator.py        # KML XML document generator and file exporter
```

---

## How It Works

### Pipeline Execution Flow

When calling `GeospatialAgent.analyze_location(input)`:

1. **Validation (`geo_utils.py`)**: Checks latitude (-90° to 90°) and longitude (-180° to 180°), ensuring coordinates are valid non-NaN numeric values.
2. **Reverse Geocoding (`reverse_geocoder.py`)**: Maps coordinates to administrative boundaries (`ward`, `district`, `zone`) and estimates `population_density`.
3. **Nearby Infrastructure Detection (`nearby_analyzer.py`)**: Scans spatial radius for environmental objects across 6 categories:
   - Schools
   - Hospitals
   - Industries
   - Roads
   - Parks
   - Construction Sites
4. **GeoJSON Generation (`geojson_generator.py`)**: Formats target monitoring point and detected infrastructure into an RFC 7946 compliant GeoJSON `FeatureCollection`.
5. **KML Export (`kml_generator.py`)**: Builds KML XML representations and saves `.kml` files to `exports/kml/` for visualization in GIS software or Google Earth.
6. **Response Assembly**: Returns structured Python dictionary validated against Pydantic models.

---

## Usage Example

```python
from app.services.geospatial import GeospatialAgent

agent = GeospatialAgent()

input_data = {
    "latitude": 28.6139,
    "longitude": 77.2090,
    "aqi": 185.5,
    "date": "2026-07-21"
}

response = agent.analyze_location(input_data)
print(response)
```

### Output Schema

```json
{
  "ward": "Ward 2A - Metro Sector 2",
  "district": "District 6 (Central Urban)",
  "zone": "Zone E",
  "population_density": "12,300 residents/km² (Dense Commercial & Residential)",
  "nearby_objects": [
    {
      "category": "schools",
      "name": "St. Jude Public Academy",
      "distance_km": 0.58,
      "location": { "latitude": 28.6179, "longitude": 77.2120 },
      "details": "Educational institute (Primary & Secondary)"
    }
  ],
  "geojson": {
    "type": "FeatureCollection",
    "features": [...]
  },
---

## Google Maps API KML Pipeline Integration

The FastAPI backend automatically serves exported `.kml` files via static route at `/exports/kml/<filename>.kml`.

### Pipeline Execution Workflow:

1. **Agent Execution**: `GeospatialAgent.analyze_location()` writes KML file to disk and outputs `kml_url`: `/exports/kml/aeris_geospatial_28.6139_77.209_2026_07_21.kml`.
2. **FastAPI Static Route**: `app.mount("/exports", StaticFiles(...))` serves public KML files.
3. **Google Maps `KmlLayer`**: Loads the KML overlay directly onto Google Maps JS client.

```javascript
// Front-end Google Maps JS Integration
function renderAerisKmlLayer(map, kmlWebUrl) {
    const publicUrl = `https://your-domain.com${kmlWebUrl}`;
    
    const kmlLayer = new google.maps.KmlLayer({
        url: publicUrl,
        map: map,
        preserveViewport: false
    });

    console.log("AERIS Spatial Net KML Layer loaded onto Google Maps:", publicUrl);
}
```

