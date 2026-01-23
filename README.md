# Scuba-Doo: Predictive Dive Safety Analysis

This project is a real-time web application designed to enhance scuba dive safety by integrating machine learning with environmental and marine data. It provides divers with predictive safety verdicts, equipment recommendations, marine life visibility forecasts, and essential ear pressure advice.

## Key Features

- **Dive Safety Prediction:** Predicts whether a dive is "Safe" or "Unsafe" based on comprehensive data analysis.
- **Wetsuit & SPF Recommendation:** Suggests appropriate wetsuit thickness and SPF levels tailored to environmental conditions.
- **Marine Life Visibility:** Informs divers about visible marine species based on location and season.
- **Ear Pressure Advice:** Offers personalized advice on ear equalization techniques and risk mitigation based on depth and temperature.
- **Web-Based Interface:** An intuitive and responsive interface for easy interaction and real-time insights.

## How It Works

The application gathers real-time weather and oceanographic data, combines it with marine life and dive site information, and processes it through a machine learning model to provide crucial safety predictions and recommendations.

### Data Flow & Models

- **Real-time Data Acquisition:** The app pulls weather and ocean data from Open-Meteo APIs and fetches marine life and depth data from Supabase.
- **Machine Learning Core:** All collected information is fed into a pre-trained **Random Forest ML model**. This model performs:
    -   **Dive Safety Prediction (Classification):** Determines if the dive is Safe or Unsafe.
    -   **Equipment Recommendations (Regression/Classification):** Recommends wetsuit thickness and SPF level.
    -   **Ear Pressure Risk Assessment:** Calculates ear pressure risks and suggests equalization techniques and safety tips.

The application delivers instant responses through its frontend, ensuring divers have critical information at their fingertips.

## Visual Overview

### Project Working Demo

![Project Working](Project%20Working.gif)

### System Architecture

![System Architecture](System%20Architecture.png)

## Tech Stack

-   **Backend:** Python, FastAPI, Uvicorn, joblib, Open-Meteo APIs, Supabase
-   **Frontend:** HTML, CSS, JavaScript
-   **ML Environment:** `uv` for package and environment management

---

## Getting Started

Follow these instructions to get the Scuba-Doo project up and running on your local machine.

### Prerequisites

-   [Python 3.8+](https://www.python.org/downloads/)
-   [uv](https://github.com/astral-sh/uv) (a fast Python package installer and resolver)

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/MoSahil147/Scuba-Doo.git
    cd Scuba-Doo
    ```

2.  **Set up the Python environment using `uv`:**
    
    First, create a virtual environment:
    ```bash
    uv venv
    ```
    
    Then, activate the environment:
    - On macOS/Linux:
      ```bash
      source .venv/bin/activate
      ```
    - On Windows:
      ```bash
      .venv\Scripts\activate
      ```
    
    Finally, install the required packages:
    ```bash
    uv sync
    ```

### Running the Application

1.  **Start the backend server:**
    ```bash
    uvicorn BackEnd.app:app --reload
    ```
    The backend will be running at `http://127.0.0.1:8000`.

2.  **Open the frontend:**
    Navigate to the `FrontEnd` directory and open the `index.html` file in your web browser.

---

## Why I Built This Project

Scuba-Doo was developed as a personal project to explore backend machine learning systems using real-world and synthetically generated data. As a marine and tech enthusiast, this project allowed me to deepen my understanding of API integration, ML inference, data cleaning, and decision logic, all while creating a tool personally meaningful for divers.