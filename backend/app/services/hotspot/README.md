# Hotspot & Event Detection Agent Service

The **Hotspot & Event Detection Agent** processes enriched air quality and spatial context data to identify pollution hotspots, cluster spatial nodes using DBSCAN, infer root environmental causes via deterministic rule engines, compute severity scores (0–100), and issue intervention recommendations.

---

## Directory Structure

```
app/services/hotspot/
├── README.md           # Service documentation
├── __init__.py         # Package exports (HotspotAgent, HotspotInput, HotspotOutput)
├── hotspot_agent.py    # Core agent orchestrator exposing analyze_hotspot(input)
├── cluster_detector.py # DBSCAN spatial clustering algorithm implementation
├── event_detector.py   # Rule-based pollution cause inference & confidence engine
├── severity.py         # Severity scoring (0-100) and recommendation generator
└── timeline.py         # Historical AQI trend tracking and spike detection
```

---

## How It Works

### Pipeline Execution Flow

When calling `HotspotAgent.analyze_hotspot(input)`:

1. **Schema & Coordinate Validation (`hotspot_agent.py`)**: Validates input metrics (AQI, PM2.5, PM10) using Pydantic `HotspotInput` models and verifies coordinate boundaries.
2. **Timeline Trend & Spike Detection (`timeline.py`)**: Analyzes historical readings (`history`) to calculate baseline averages, trend direction (`RISING`, `STABLE`, `FALLING`), and flags sudden AQI/PM spikes (`is_spike`).
3. **DBSCAN Spatial Clustering (`cluster_detector.py`)**: Runs density-based spatial clustering on spatial coordinates using Haversine distance. Identifies spatial cluster labels (e.g., `Cluster-A`).
4. **Rule-Based Cause Inference (`event_detector.py`)**: Evaluates deterministic environmental rule chains to classify the primary pollution source and compute a confidence score (0.0 to 1.0):
   - **Construction Dust**: High PM10/PM2.5 ratio, low wind speed, nearby construction site.
   - **Traffic Congestion**: Nearby roads, elevated PM2.5 concentrations.
   - **Industrial Emissions**: Nearby industrial facilities, sustained high AQI/PM levels.
   - **Crop Burning**: Severe PM2.5 spike, dry weather conditions.
   - **Fireworks**: Abrupt high magnitude short-term AQI spike.
   - **Diesel Generator**: Localized PM2.5 spike near commercial or mixed infrastructure.
   - **Unknown**: Fallback classification.
5. **Severity Scoring & Recommendation (`severity.py`)**: Computes a normalized 0–100 severity score weighting:
   - AQI baseline magnitude
   - Population density impact
   - Presence of sensitive receptors (schools & hospitals)
   - Weather & dispersion conditions
   - Historical spike trends
   And derives targeted recommendations (e.g., *"Immediate inspection"*, *"Issue health advisory"*).

---

## Usage Example

```python
from app.services.hotspot import HotspotAgent

agent = HotspotAgent()

input_data = {
    "latitude": 28.6139,
    "longitude": 77.2090,
    "aqi": 210.0,
    "pm25": 85.0,
    "pm10": 180.0,
    "weather": {
        "temperature": 32.0,
        "humidity": 40.0,
        "wind_speed": 3.5,
        "condition": "dusty"
    },
    "history": [
        {"aqi": 110.0, "pm25": 45.0, "pm10": 80.0},
        {"aqi": 115.0, "pm25": 48.0, "pm10": 85.0}
    ],
    "nearby_objects": [
        {"category": "construction sites", "name": "Metro Extension Site"}
    ]
}

response = agent.analyze_hotspot(input_data)
print(response)
```

### Output Schema

```json
{
  "hotspot": true,
  "cluster": "Cluster-A",
  "severity": 71,
  "cause": "Construction Dust",
  "confidence": 0.91,
  "recommendation": "Issue vulnerable group health advisory for nearby schools and hospitals."
}
```
