## Not required for now, was using when doing the groq api calls for beautifying the answers and also getting the values and giving the verdict!

import requests
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

def get_llm_analysis(location, date, time, coords, weather, animals):
    # Trim animal text if too long
    animals_short = animals[:700] + "..." if len(animals) > 800 else animals

    prompt = f"""
DIVE SITE REPORT

Location: {location}
Date: {date}
Time: {time}
Coordinates: {coords['latitude']}, {coords['longitude']}

SEA CONDITIONS:
- Temp: {weather.get("sea_temp")} °C
- Waves: {weather.get("wave_height")} m
- Currents: {weather.get("current_speed")} m/s
- UV Index: {weather.get("uv_index")}

POTENTIAL MARINE LIFE:
{animals_short}

TASK:
Give:
1. Safety verdict (Safe / Unsafe)
2. Recommended wetsuit
3. SPF level
4. One risk alert

Limit response to 150 words.
"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 400
        }
    )

    try:
        result = response.json()
        if "choices" not in result:
            return "LLM error. Response trimmed due to token limits."
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"LLM exception: {str(e)}"