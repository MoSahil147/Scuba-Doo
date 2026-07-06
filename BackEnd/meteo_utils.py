## From the input we are giving in the frontend, after getting the lats, longi, time and date! Its sent here for fetching the marine and weather data.
import requests
import logging

logger = logging.getLogger(__name__)

## Finds the hourly array index matching the diver's chosen date/time.
## Falls back to the closest available hour if the exact stamp isn't present.
def _find_hour_index(hourly_times: list[str], date: str, time: str) -> int:
    target = f"{date}T{time}"
    if target in hourly_times:
        return hourly_times.index(target)

    target_hour_stamp = f"{date}T{time[:2]}:00"
    if target_hour_stamp in hourly_times:
        return hourly_times.index(target_hour_stamp)

    same_day = [i for i, t in enumerate(hourly_times) if t.startswith(date)]
    return same_day[0] if same_day else 0

## Fetching weather and Marine Data
def get_weather_and_marine_data(lat: float, lon: float, date: str, time: str):
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&daily=sunrise,sunset,uv_index_max"
        f"&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,"
        f"precipitation,temperature_120m,wind_speed_120m,pressure_msl,wind_direction_120m"
        f"&current=pressure_msl,surface_pressure,is_day&timezone=Asia%2FDubai"
        f"&start_date={date}&end_date={date}"
    )

    marine_url = (
        f"https://marine-api.open-meteo.com/v1/marine?"
        f"latitude={lat}&longitude={lon}"
        f"&hourly=wave_height,wave_direction,sea_surface_temperature,"
        f"ocean_current_velocity,ocean_current_direction,sea_level_height_msl"
        f"&timezone=Asia%2FDubai"
        f"&start_date={date}&end_date={date}"
    )

    ## Timeout guards against Render hanging on a slow/unreachable upstream host
    weather_response = requests.get(weather_url, timeout=10)
    marine_response = requests.get(marine_url, timeout=10)

    weather_data = weather_response.json()
    marine_data = marine_response.json()

    ## Open-Meteo returns HTTP 200 with an {"error": true, "reason": ...} body on bad params
    ## (e.g. a date outside its supported forecast/archive range), and non-200 statuses on
    ## rate limiting/outages. Surface this instead of failing silently with a KeyError further
    ## down the line when "hourly"/"daily" turn out to be missing.
    if not weather_response.ok or weather_data.get("error"):
        logger.error(f"Open-Meteo weather API failed: status={weather_response.status_code} body={weather_data}")
        raise RuntimeError(f"Weather API error: {weather_data.get('reason', weather_response.status_code)}")

    if not marine_response.ok or marine_data.get("error"):
        logger.error(f"Open-Meteo marine API failed: status={marine_response.status_code} body={marine_data}")
        raise RuntimeError(f"Marine API error: {marine_data.get('reason', marine_response.status_code)}")

    ## Pick out the hourly index matching the diver's chosen time, for both APIs,
    ## so the rest of the app doesn't need to know about Open-Meteo's response shape.
    weather_hour_index = _find_hour_index(weather_data["hourly"]["time"], date, time)
    marine_hour_index = _find_hour_index(marine_data["hourly"]["time"], date, time)

    return {
        "weather": weather_data,
        "marine": marine_data,
        "weather_hour_index": weather_hour_index,
        "marine_hour_index": marine_hour_index,
    }