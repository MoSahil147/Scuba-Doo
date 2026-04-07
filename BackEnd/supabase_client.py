## Here we are fetching the Coordinates and Marine Animal data for the final Verdict
from supabase import create_client
from dotenv import load_dotenv
import os
import pandas as pd
from pathlib import Path
import logging

## Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

## Paths for local fallback
BASE_DIR = Path(__file__).parent.parent
COORDINATES_CSV = BASE_DIR / "Data" / "Coordinates.csv"
MARINE_ANIMAL_CSV = BASE_DIR / "Data" / "All Good copy.csv"

## Initialise Supabase client
supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        logger.error(f"Failed to initialise Supabase client: {e}")

## Getting the coordinates
def get_coordinates(location_name: str):
    ## Try Supabase first
    if supabase:
        try:
            response = supabase.table("Coordinates Info").select("*").eq("name", location_name).execute()
            if response.data:
                return response.data[0]
        except Exception as e:
            logger.warning(f"Supabase query failed for coordinates, falling back to CSV: {e}")

    ## Local Fallback
    if COORDINATES_CSV.exists():
        try:
            df = pd.read_csv(COORDINATES_CSV)
            
            ## First try exact match (case-insensitive)
            match = df[df["name"].str.lower() == location_name.lower()]
            if not match.empty:
                return match.iloc[0].to_dict()
            
            ## If not found, check if the CSV name is contained within the full location string
            ## The frontend sends "Name, Region, Country"
            for _, row in df.iterrows():
                if row["name"].lower() in location_name.lower():
                    return row.to_dict()
                    
        except Exception as e:
            logger.error(f"Failed to read local coordinates CSV: {e}")

    return None

## Fetching the Marine Animal Datas
def get_marine_animal_data(lat: float, lon: float):
    ## Try Supabase first
    if supabase:
        try:
            response = supabase.table("All the values").select("*").eq("latitude", lat).eq("longitude", lon).execute()
            if response.data:
                ## Return list of matches or single dict based on usage? 
                ## app.py handles both, but Supabase usually returns a list of records.
                return response.data
        except Exception as e:
            logger.warning(f"Supabase query failed for marine animal data, falling back to CSV: {e}")

    ## Local Fallback
    if MARINE_ANIMAL_CSV.exists():
        try:
            df = pd.read_csv(MARINE_ANIMAL_CSV)
            ## Filter by approximate coordinates (to handle floating point precision)
            matches = df[(abs(df["latitude"] - lat) < 0.001) & (abs(df["longitude"] - lon) < 0.001)]
            if not matches.empty:
                return matches.to_dict("records")
        except Exception as e:
            logger.error(f"Failed to read local marine animal CSV: {e}")

    return []