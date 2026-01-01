from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .supabase_client import get_coordinates, get_marine_animal_data
from .meteo_utils import get_weather_and_marine_data
from .groq_utils import get_llm_analysis
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-dive")
async def analyze_dive(request: Request):
    data = await request.json()

    location = data.get("location")
    date = data.get("date")
    time = data.get("time")

    coordinates = get_coordinates(location)
    if not coordinates:
        return {"error": f"Coordinates not found for {location}"}

    lat = coordinates["latitude"]
    lon = coordinates["longitude"]

    raw_weather = get_weather_and_marine_data(lat, lon, date, time)
    raw_animals = get_marine_animal_data(lat, lon)

    compact_weather = {
        "sea_temp": raw_weather["marine"]["hourly"]["sea_surface_temperature"][0],
        "wave_height": raw_weather["marine"]["hourly"]["wave_height"][0],
        "current_speed": raw_weather["marine"]["hourly"]["ocean_current_velocity"][0],
        "uv_index": raw_weather["weather"]["daily"]["uv_index_max"][0],
    }

    compact_animals = []
    if isinstance(raw_animals, list):
        for a in raw_animals[:3]:
            compact_animals.append({
                "name": a.get("marine_animal"),
                "depth": a.get("typical_depth"),
                "probability": a.get("probability")
            })
    elif isinstance(raw_animals, dict) and raw_animals:
        compact_animals.append({
            "name": raw_animals.get("marine_animal"),
            "depth": raw_animals.get("typical_depth"),
            "probability": raw_animals.get("probability")
        })

    llm_response = get_llm_analysis(
        location,
        date,
        time,
        coordinates,
        compact_weather,
        compact_animals
    )

    return {
        "llm_response": llm_response,
        "coordinates": coordinates,
        "weather": compact_weather,
        "marine_life": compact_animals
    }