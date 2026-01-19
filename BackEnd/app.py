## Here we come to the most important, working
from fastapi import FastAPI, Request
## CORSMiddleware:- Allows backend to accept requests from other domains (like your frontend running on a different port), preventing CORS errors in the browser.
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import joblib
import os

from .supabase_client import get_coordinates, get_marine_animal_data
from .meteo_utils import get_weather_and_marine_data
from .ear_utils import get_ear_care_recommendations

## Load environment variables from .env file
load_dotenv()

## Initialise FastAPI app
app = FastAPI()

## Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         # Allow requests from any domain (frontend running on a different port or domain)
    allow_credentials=True,      # Allow cookies and credentials in cross-origin requests
    allow_methods=["*"],         # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],         # Allow all custom headers (like Content-Type, Authorization, etc.)
)

## Load trained Random Forest model once when server starts
MODEL_PATH = "Data/scuba_dive_model.pkl"
model = joblib.load(MODEL_PATH)

## Recommend wetsuit type based on temperature
def recommend_suit(temp):
    if temp >= 28: return "light wetsuit"
    if temp >= 24: return "3mm wetsuit"
    if temp >= 20: return "5mm wetsuit"
    if temp >= 16: return "semi-dry suit"
    return "dry suit"

## Recommend SPF level based on UV index
def recommend_spf(uv):
    if uv <= 2: return "SPF 15"
    if uv <= 5: return "SPF 30"
    if uv <= 7: return "SPF 50"
    return "SPF 50+"

## Route to analyse dive based on location, date, and time
@app.post("/analyse-dive")
async def analyse_dive(request: Request):
    data = await request.json()
    location = data.get("location")
    date = data.get("date")
    time = data.get("time")

    ## Get latitude and longitude for selected dive location
    coordinates = get_coordinates(location)
    if not coordinates:
        return {"error": f"Coordinates not found for {location}"}

    lat = coordinates["latitude"]
    lon = coordinates["longitude"]

    ## Fetch weather and marine data from Open-Meteo APIs
    api_data = get_weather_and_marine_data(lat, lon, date, time)
    marine = api_data["marine"]
    weather = api_data["weather"]

    ## Extract features required by the model
    try:
        feature_vector = [
            lat,
            lon,
            int(date.split("-")[1]),                     ## month
            int(time.split(":")[0]),                     ## hour_of_day
            marine["hourly"]["wave_height"][0],
            marine["hourly"]["sea_surface_temperature"][0],
            marine["hourly"]["ocean_current_velocity"][0],
            weather["daily"]["uv_index_max"][0],
            weather["hourly"]["pressure_msl"][0],
            coordinates.get("typical_depth", 20)         ## fallback in case missing
        ]
    except Exception:
        return {"error": "Error preparing input features from weather APIs"}

    ## Predict safe or unsafe using trained Random Forest model
    prediction = model.predict([feature_vector])[0]
    verdict = "🟢 Safe" if prediction == 1 else "🔴 Unsafe"

    ## Suggest wetsuit and SPF based on conditions
    suit = recommend_suit(feature_vector[5])      ## temperature
    spf = recommend_spf(feature_vector[7])        ## UV index

    ## Get top 3 marine animals likely visible at that site
    marine_life_data = get_marine_animal_data(lat, lon)
    top_animals = []
    if isinstance(marine_life_data, list):
        for a in marine_life_data[:3]:
            top_animals.append({
                "name": a.get("marine_animal"),
                "depth": a.get("typical_depth"),
                "probability": a.get("probability")
            })
    elif isinstance(marine_life_data, dict) and marine_life_data:
        top_animals.append({
            "name": marine_life_data.get("marine_animal"),
            "depth": marine_life_data.get("typical_depth"),
            "probability": marine_life_data.get("probability")
        })

    ## Generate ear safety recommendations
    ear_care = get_ear_care_recommendations(
        depth=feature_vector[9],
        descent_rate=5.0,
        water_temp=feature_vector[5],
        diver_experience="intermediate"
    )

    ## Extract risk data for emoji display
    risk = ear_care["risk_assessment"]

    ## Format result message
    result_text = f"""
     Verdict: {verdict}
     Recommended Suit: {suit}
     Recommended SPF: {spf}

     Likely Marine Life:
    """
    for a in top_animals:
        result_text += f"\n- {a['name']} at {a['depth']}m (prob: {a['probability']})"

    result_text += f"""

     Ear Safety Summary:
     {ear_care['summary']}

     Max Recommended Depth: {ear_care['max_recommended_depth']}m
     Ear Risk Level: {risk['risk_color']} {risk['risk_level']} (Score: {risk['risk_score']})
     Tips:
    """
    for tip in ear_care["safety_tips"][:5]:
        result_text += f"\n- {tip}"

    ## Final response to frontend
    return {
        "llm_response": result_text.strip(),
        "verdict": verdict,
        "recommended_suit": suit,
        "recommended_spf": spf,
        "marine_life": top_animals,
        "ear_care": ear_care
    }