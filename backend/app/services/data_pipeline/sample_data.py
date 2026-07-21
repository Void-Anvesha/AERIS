import pandas as pd


def create_sample_datasets() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    aqi_df = pd.DataFrame([
        {"date": "2024-01-01", "city": "Bengaluru", "aqi": 120},
        {"date": "2024-01-02", "city": "Bengaluru", "aqi": 140},
    ])
    weather_df = pd.DataFrame([
        {"date": "2024-01-01", "city": "Bengaluru", "temperature": 28, "humidity": 65},
        {"date": "2024-01-02", "city": "bengaluru", "temperature": 30, "humidity": 70},
    ])
    traffic_df = pd.DataFrame([
        {"date": "2024-01-01", "city": "Bengaluru", "traffic_index": 0.8},
        {"date": "2024-01-02", "city": "Bengaluru", "traffic_index": 0.9},
    ])
    return aqi_df, weather_df, traffic_df
