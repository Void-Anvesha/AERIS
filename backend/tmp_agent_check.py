from app.services.data_pipeline.agents.data_fusion_agent import DataFusionAgent
from app.services.data_pipeline.agents.feature_engineering_agent import FeatureEngineeringAgent
from app.services.data_pipeline.sample_data import create_sample_datasets

aqi_df, weather_df, traffic_df = create_sample_datasets()

fusion = DataFusionAgent()
merged = fusion.run(aqi_df, weather_df, traffic_df)
print("Fusion output rows:", len(merged))
print(merged)

feature = FeatureEngineeringAgent()
engineered = feature.run(merged)
print("Feature output rows:", len(engineered))
print(engineered[["date","city","aqi","season","weekend","lag_aqi","rolling_mean_aqi","health_risk"]])