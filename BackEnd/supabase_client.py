## Herewe are fetching the Coordinates and Marine Animal data for the final Verdict
from supabase import create_client
from dotenv import load_dotenv
import os
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

## Getting the coordinates
def get_coordinates(location_name: str):
    response = supabase.table("Coordinates Info").select("*").eq("name", location_name).execute()
    if response.data:
        return response.data[0]
    return None

## Fetching the Marine Animal Datas
def get_marine_animal_data(lat: float, lon: float):
    response = supabase.table("All the values").select("*").eq("latitude", lat).eq("longitude", lon).execute()
    if response.data:
        return response.data[0]
    return {}