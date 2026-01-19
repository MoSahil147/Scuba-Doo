## Needed to rely on generating the datasets, as couldn't collect many, so relied on some datasets and made all the permuation combinations using that!
import pandas as pd
import numpy as np
import random

## Main settingss
SAMPLES_PER_PAIR = 100 ## will generate 100 datas
OUTPUT_FILE = "Data/final_synthetic_dive_dataset.csv"  ## Will save inside the Data folder

## Load cleaned location and marine data
## Encoding tells how Python will read from a file by mapping bytes to characters, utf-8 is most common, since it failed, used latin1 (which is crazy, and read everything well)
coords = pd.read_csv("Data/Coordinates.csv", encoding="latin1")
marine = pd.read_csv("Data/All Good copy.csv", encoding="latin1")

## Merge both datasets on latitude and longitude to link marine animals to dive sites
## inner: helps in keeping rows where there is  a match in both coords and marine. If a dive site has no associated marine animal at that exact coordinate, it is excluded.
merged = pd.merge(coords, marine, on=["latitude", "longitude"], how="inner")

## Wave height between 0.2m and 3.2m
## Less than 0.2m is nearly flat and uncommon in open water. Above 3.2m is unsafe for diving due to strong surface turbulence. Most safe dive sites have mild to moderate wave heights within this range.
def random_wave_height(): return round(np.random.uniform(0.2, 3.2), 2)

## Ocean current between 0.05 and 1.4 m/s
## Below 0.05 m/s is negligible flow, often seen in sheltered areas. Above 1.4 m/s currents become risky for divers, especially for entry/exit and maintaining position. Most safe dives occur between 0.2 to 1.2 m/s.
def random_current_speed(): return round(np.random.uniform(0.05, 1.4), 2)

## Sea temperature based on month

## December, January, February (winter months), Sea temperatures are colder, so values are sampled between 16°C and 24°C, which matches winter diving conditions in many regions.
## June, July, August (summer months), Sea temperatures are warmer, so values are sampled between 25°C and 31°C, typical of tropical and summer dive sites.
## 	All other months (spring and autumn), Temperatures fall in a moderate range between 20°C and 28°C, representing transitional seasons.
def random_sea_temp(month):
    if month in [12, 1, 2]: return round(np.random.uniform(16, 24), 1)
    if month in [6, 7, 8]: return round(np.random.uniform(25, 31), 1)
    return round(np.random.uniform(20, 28), 1)

## UV index varies by month and time
## Morning and late evening hours have lower UV.
## Midday hours increase the UV due to direct sun exposure.
## Summer months add more intensity.
## Values are capped at 11 to stay within realistic limits based on global UV index standards.

def random_uv(month, hour):
    base = np.random.uniform(2, 6)
    if 10 <= hour <= 15: base += np.random.uniform(1, 4)
    if month in [5, 6, 7, 8]: base += 1
    return round(min(base, 11), 1)

## Suit recommendation based on sea temperature
def suit_from_temp(temp):
    if temp >= 28: return "light wetsuit"
    if temp >= 24: return "3mm wetsuit"
    if temp >= 20: return "5mm wetsuit"
    if temp >= 16: return "semi-dry suit"
    return "dry suit"

## SPF suggestion based on UV index
def spf_from_uv(uv):
    if uv <= 2: return "SPF 15"
    if uv <= 5: return "SPF 30"
    if uv <= 7: return "SPF 50"
    return "SPF 50+"

## Compute safety score using weather conditions
def safety_score(wave, current, temp, uv):
    score = 100  ## Starting with the full safety score

    score -= wave * 15  ## Reducing the score based on wave height severity
    score -= current * 20  ## Stronger the currents the more the safety reduces

    if temp < 20:
        score -= (20 - temp) * 2  ## Will penalise for cold water temperatures

    if uv > 8:
        score -= 10  ## High UV index, risk to health

    return max(0, min(100, round(score)))  # Final score between 0 and 100

## These are the output columns
columns = [
    "latitude", "longitude", "site_name",
    "marine_animal", "scientific_name",
    "month", "hour_of_day", "is_day", "is_peak_sun_hours",
    "wave_height", "wave_direction", "sea_surface_temperature",
    "ocean_current_velocity", "ocean_current_direction", "sea_level_height_msl",
    "uv_index_max", "temperature_2m", "relative_humidity_2m",
    "precipitation_probability", "precipitation",
    "wind_speed_120m", "wind_direction_120m",
    "pressure_msl", "surface_pressure",
    "typical_depth", "animal_probability", "best_months", "weather_condition", "notes",
    "safety_score", "verdict", "recommended_suit", "recommended_spf"
]

## A new CSV with headers
pd.DataFrame(columns=columns).to_csv(OUTPUT_FILE, index=False)

## Generating synthetic samples
for _, r in merged.iterrows():
    rows = []
    for _ in range(SAMPLES_PER_PAIR):
        ## Randomised time and light settings
        month = random.randint(1, 12)
        hour = random.randint(6, 18)
        is_day = 1
        is_peak = 1 if 10 <= hour <= 15 else 0

        ## Generate realistic weather features
        wave = random_wave_height()
        current = random_current_speed()
        sea_temp = random_sea_temp(month)
        uv = random_uv(month, hour)
        score = safety_score(wave, current, sea_temp, uv)
        verdict = "Safe" if score >= 60 else "Unsafe"

        ## Row creation for one sample
        row = [
            r["latitude"], r["longitude"], r["name"],
            r["marine_animal"], r["scientific_name"],
            month, hour, is_day, is_peak,
            wave, random.randint(0, 360), sea_temp,
            current, random.randint(0, 360), round(np.random.uniform(-0.5, 0.5), 2),
            uv, round(sea_temp + np.random.uniform(0, 3), 1), random.randint(40, 90),
            random.randint(0, 80), round(np.random.uniform(0, 8), 1),
            round(np.random.uniform(1, 14), 1), random.randint(0, 360),
            round(np.random.uniform(1005, 1024), 1), round(np.random.uniform(1000, 1019), 1),
            r["typical_depth"], r["probability"], r["best_months"], r["weather_condition"], r["notes"],
            score, verdict,
            suit_from_temp(sea_temp), spf_from_uv(uv)
        ]
        rows.append(row)

    ## Appending the samples for this pair to the CSV
    pd.DataFrame(rows, columns=columns).to_csv(
        OUTPUT_FILE, mode="a", index=False, header=False
    )

print("Dataset generated:", OUTPUT_FILE)