import requests

def get_weather_and_marine_data(lat: float, lon: float, date: str, time: str):
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&daily=sunrise,sunset,uv_index_max"
        f"&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,"
        f"precipitation,temperature_120m,wind_speed_120m,pressure_msl,wind_direction_120m"
        f"&current=pressure_msl,surface_pressure,is_day&timezone=Asia%2FDubai"
    )

    marine_url = (
        f"https://marine-api.open-meteo.com/v1/marine?"
        f"latitude={lat}&longitude={lon}"
        f"&hourly=wave_height,wave_direction,sea_surface_temperature,"
        f"ocean_current_velocity,ocean_current_direction,sea_level_height_msl"
        f"&timezone=Asia%2FDubai"
    )

    weather_data = requests.get(weather_url).json()
    marine_data = requests.get(marine_url).json()

    return {
        "weather": weather_data,
        "marine": marine_data
    }