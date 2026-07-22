from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_data_fusion_agent_endpoint():
    payload = {
        "aqi_data": [{"date": "2026-07-21", "city": "Delhi", "aqi": 185.5}],
        "weather_data": [{"date": "2026-07-21", "city": "Delhi", "temperature": 32.0, "humidity": 40.0}],
        "traffic_data": [{"date": "2026-07-21", "city": "Delhi", "traffic_index": 0.5}]
    }
    response = client.post("/api/agents/data-fusion", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["rows"] == 1
    assert "confidence" in data


def test_feature_engineering_agent_endpoint():
    payload = [
        {"date": "2026-07-21", "city": "Delhi", "aqi": 185.5, "traffic_index": 0.5, "industrial_score": 0.2, "green_cover": 0.4}
    ]
    response = client.post("/api/agents/feature-engineering", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "features_generated" in data


def test_geospatial_agent_endpoint():
    payload = {
        "latitude": 28.6139,
        "longitude": 77.2090,
        "aqi": 185.5,
        "date": "2026-07-21"
    }
    response = client.post("/api/agents/geospatial", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "ward" in data
    assert "district" in data
    assert "geojson" in data
    assert "kml_path" in data


def test_forecast_agent_endpoint():
    payload = {
        "state": "Delhi",
        "area": "Anand Vihar",
        "history": [
            {"date": "2026-07-20", "aqi": 180.0},
            {"date": "2026-07-21", "aqi": 185.0}
        ]
    }
    response = client.post("/api/agents/forecast", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "aqi24" in data
    assert "aqi48" in data
    assert "aqi72" in data


def test_source_attribution_agent_endpoint():
    payload = {
        "aqi": 185.5,
        "pm25": 85.0,
        "pm10": 180.0,
        "weather": {"humidity": 40.0},
        "nearby_objects": [{"category": "roads", "name": "NH-24"}]
    }
    response = client.post("/api/agents/source-attribution", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "traffic" in data
    assert "construction" in data
    assert "industry" in data
    assert "biomass" in data
    assert "dust" in data


def test_hotspot_agent_endpoint():
    payload = {
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
    response = client.post("/api/agents/hotspot", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "hotspot" in data
    assert "severity" in data
    assert "cause" in data


def test_decision_agent_endpoint():
    payload = {
        "aqi": 210.0,
        "forecast": 240.0,
        "confidence": 0.85,
        "dominant_pollutant": "PM2.5",
        "source": "Construction",
        "hotspot": True,
        "nearby_schools": 3,
        "nearby_hospitals": 1,
        "population_density": "High",
        "zone_name": "Ward 14"
    }
    response = client.post("/api/agents/decision", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "priority" in data
    assert "inspection" in data
    assert "reason" in data


from unittest.mock import patch, AsyncMock

@patch("app.services.llm.groq_client.GroqClient.generate", new_callable=AsyncMock)
def test_advisory_agent_endpoint(mock_generate):
    mock_generate.return_value = "Mocked advisory text response."
    payload = {
        "risk_score": 85,
        "priority": "Critical",
        "authority": "Municipal Corporation",
        "response_time": "Within 2 Hours",
        "recommended_actions": [
            "Sprinkle water on roads",
            "Stop construction activities",
            "Wear N95 masks"
        ],
        "reason": [
            "Current AQI (210) falls in the Critical band"
        ],
        "manual_review_required": False,
        "aqi": 210.0,
        "forecast": 240.0,
        "dominant_pollutant": "PM2.5",
        "source": "Construction",
        "zone_name": "Ward 14"
    }
    response = client.post("/api/agents/advisory", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "authority_advisory" in data
    assert "citizen_advisory" in data
    assert "sms_advisory" in data
    assert "email_advisory" in data



