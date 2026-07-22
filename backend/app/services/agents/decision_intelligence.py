import os
import pandas as pd
from app.models.insight import Hotspot, IntelligenceSnapshot, SourceAttribution
from app.core.logging import logger

class DecisionIntelligenceAgent:
    def __init__(self) -> None:
        self.csv_path = "data/raw/aqi.csv"
        self.city = "India National Grid"

    def generate_snapshot(self) -> IntelligenceSnapshot:
        if not os.path.exists(self.csv_path):
            logger.warning("aqi.csv not found at %s. Falling back to default snapshot.", self.csv_path)
            return self._fallback_snapshot()
            
        try:
            df = pd.read_csv(self.csv_path)
            # Standardize date and values
            df["aqi_value"] = pd.to_numeric(df["aqi_value"], errors="coerce").fillna(100.0)
            
            # Calculate actual statistics from CSV
            current_aqi = int(df["aqi_value"].mean())
            worst_idx = df["aqi_value"].idxmax()
            worst_row = df.loc[worst_idx]
            worst_city = str(worst_row["area"])
            worst_city_aqi = int(worst_row["aqi_value"])
            
            # Group by area to find actual high-pollution hotspots
            hotspots_df = df[df["aqi_value"] > 150].drop_duplicates("area").head(5)
            
            # Hardcoded coordinates for mapping main Indian locations in the dataset
            coords_map = {
                "Delhi": (28.6139, 77.2090),
                "Mumbai": (19.0760, 72.8777),
                "Bengaluru": (12.9716, 77.5946),
                "Kolkata": (22.5726, 88.3639),
                "Chennai": (13.0827, 80.2707),
                "Hyderabad": (17.3850, 78.4867),
                "Ahmedabad": (23.0225, 72.5714),
                "Pune": (18.5204, 73.8567),
                "Maharashtra": (19.0760, 72.8777),
                "Bihar": (25.0961, 85.3131),
                "Madhya Pradesh": (22.9734, 78.6569),
                "Chhattisgarh": (21.2787, 81.8661),
                "Assam": (26.2006, 92.9376),
                "Rajasthan": (27.0238, 74.2179)
            }
            
            hotspots = []
            for _, row in hotspots_df.iterrows():
                area_name = str(row["area"])
                state_name = str(row["state"])
                aqi_val = float(row["aqi_value"])
                
                lat, lng = coords_map.get(area_name, coords_map.get(state_name, (28.61, 77.20)))
                hotspots.append(
                    Hotspot(
                        name=f"{area_name} ({state_name})",
                        lat=lat,
                        lng=lng,
                        risk_level="Very High" if aqi_val > 200 else "High",
                        source=str(row.get("prominent_pollutants", "PM2.5"))
                    )
                )
                
            if not hotspots:
                # Add at least one hotspot from the worst location
                lat, lng = coords_map.get(worst_city, (28.61, 77.20))
                hotspots.append(
                    Hotspot(
                        name=f"{worst_city} ({worst_row['state']})",
                        lat=lat,
                        lng=lng,
                        risk_level="Critical",
                        source=str(worst_row.get("prominent_pollutants", "PM2.5"))
                    )
                )

            return IntelligenceSnapshot(
                city=self.city,
                current_aqi=current_aqi,
                status="Unhealthy" if current_aqi > 150 else "Moderate",
                trend="Rising",
                forecast_next_24h=current_aqi + 14,
                forecast_next_72h=current_aqi + 22,
                hotspots=hotspots,
                source_attribution=SourceAttribution(
                    traffic=0.45,
                    industry=0.25,
                    biomass=0.18,
                    dust=0.12
                ),
                recommendation=f"Enforce active industrial restriction and dust sprinklers in {worst_city} due to critical AQI value of {worst_city_aqi}.",
                advisory=f"Air pollution has exceeded limits. Residents in {worst_city} should use N95 masks and restrict outdoor activities."
            )
            
        except Exception as e:
            logger.exception("Error parsing aqi.csv: %s. Using fallback snapshot.", str(e))
            return self._fallback_snapshot()

    def _fallback_snapshot(self) -> IntelligenceSnapshot:
        return IntelligenceSnapshot(
            city=self.city,
            current_aqi=168,
            status="Unhealthy",
            trend="Rising",
            forecast_next_24h=182,
            forecast_next_72h=190,
            hotspots=[
                Hotspot(name="Downtown Junction", lat=12.9716, lng=77.5946, risk_level="High", source="Traffic"),
                Hotspot(name="Industrial Corridor", lat=12.9600, lng=77.6200, risk_level="Very High", source="Industry"),
            ],
            source_attribution=SourceAttribution(
                traffic=0.42,
                industry=0.28,
                biomass=0.18,
                dust=0.12,
            ),
            recommendation="Deploy mobile monitoring units, restrict truck movement during peak hours, and activate roadside dust suppression.",
            advisory="Sensitive groups should avoid prolonged outdoor activity and keep windows closed. General citizens should use masks if outdoors.",
        )

