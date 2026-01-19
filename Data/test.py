import joblib
import pandas as pd

## Load the model
model = joblib.load("Data/scuba_dive_model.pkl")

## Define feature names
features = [
    "latitude", "longitude", "month", "hour_of_day",
    "wave_height", "sea_surface_temperature", "ocean_current_velocity",
    "uv_index_max", "pressure_msl", "typical_depth"
]

## Create a DataFrame for one input sample
sample = pd.DataFrame([[
    19.07, 72.87, 6, 10, 0.4, 28.5, 0.8, 8.0, 1012, 18
]], columns=features)

## Prediction Timeee
prediction = model.predict(sample)[0]
print("Prediction (1=Safe, 0=Unsafe):", prediction)