# Scuba-Doo

A real-time web app that helps scuba divers with dive safety using weather, marine life, and environmental data. It predicts safety verdicts, recommends suits, shows marine life visibility and gives ear pressure advice using ML model and live APIs. Built as a side quest to learn FastAPI backends, since being a marine and tech geek at the same time.

## Let's Understand What It Does

When we select a dive location, date and time, at the frontend the app:

- Pulls real-time weather and ocean data from **Open-Meteo APIs**
- Fetches marine life and depth data from **Supabase**
- Sends all collected information to a **Random Forest ML model** that:
  - Predicts if the dive is **Safe** or **Unsafe**
  - Recommends **wetsuit thickness** and **SPF level**
  - Highlights visible marine animals based on season and location
  - Calculates **ear pressure risk** and suggests:
    - Equalisation techniques based on depth and diver experience
    - Safety tips based on temperature and descent speed

The app responds instantly through a clean frontend, with real-time recommendations.

## Visual Overview

### Project Working Demo

![Project Working](Project%20Working.gif)

### System Architecture

![System Architecture](System%20Architecture.png)

## Tech Stack Used

### Backend

- **Python**, **FastAPI**: Core server and API
- **joblib**: For loading the pre-trained ML model
- **Open-Meteo APIs**: Weather, marine current, wave height, sea temperature
- **Supabase**: Stores geotagged dive sites and marine life metadata
- **Custom Ear Care Module**: Calculates depth/temp-based ear risks and mitigation tips

### Frontend

- **HTML**, **CSS**, **JavaScript**: Simple, responsive UI
- **Dropdowns**: Dynamic location selector from Supabase
- **Form-based interaction**: Inputs dive details and displays:
  - Dive safety verdict
  - Top 3 visible marine species
  - Suit and sunscreen suggestions
  - Ear safety score with actionable advice

## Why I Built This Project Scuba-Doo

I wanted to explore backend ML systems in a practical way, using real world data (for context, some of the data was synthetically generated). Scuba-Doo helped me understand API integration, ML inferences, data cleaning and most importantly decision logic, while making something personally meaningful as a diver.