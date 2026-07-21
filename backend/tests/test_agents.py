from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_geospatial_agent_endpoint():
    payload = {
        "latitude": 28.6139,
        "longitude": 77.2090,
        "aqi": 185.5,
        "date": "2026-07-21"
    }
    response = client.post("/api/geospatial/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "ward" in data
    assert "district" in data
    assert "geojson" in data
    assert "kml_path" in data

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
    response = client.post("/api/hotspot/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "hotspot" in data
    assert "severity" in data
    assert "cause" in data
