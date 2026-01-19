## This code is for calculating the ear pressure, which we may experince when we go for dives
"""
Ear Pressure Equalisation Utilities for Scuba-Doo

This module provides functions to calculate ear pressure risk levels,
recommend equalisation techniques, and provide depth-specific safety tips
for scuba divers.
"""

from typing import Dict, List, Any


def calculate_ear_pressure_risk(
    depth: float,
    descent_rate: float = 5.0,
    water_temp: float = 25.0
) -> Dict[str, Any]:
    """
    Calculate ear pressure risk level based on dive conditions.
    """

    ## Base risk increases with depth (1 ATM per 10m)
    depth_risk = depth * 0.1

    ## Faster descent increases risk
    descent_factor = (descent_rate / 5.0) * 2.0

    ## Cold water increases risk
    temp_factor = max(0, (25 - water_temp) * 0.2)

    ## Total risk score
    total_score = depth_risk + descent_factor + temp_factor

    ## Determine risk level
    if total_score < 3:
        risk_level = "LOW"
        risk_color = "🟢"
        message = "Standard equalisation should be sufficient"
    elif total_score < 6:
        risk_level = "MODERATE"
        risk_color = "🟡"
        message = "Equalise more frequently, stay relaxed"
    elif total_score < 10:
        risk_level = "HIGH"
        risk_color = "🟠"
        message = "Use advanced techniques, descend slowly"
    else:
        risk_level = "VERY HIGH"
        risk_color = "🔴"
        message = "Extra caution required, consider shallower dive"

    return {
        "risk_level": risk_level,
        "risk_color": risk_color,
        "risk_score": round(total_score, 1),
        "message": message,
        "depth": depth,
        "descent_rate": descent_rate,
        "water_temp": water_temp
    }


def get_equalisation_technique(
    depth: float,
    diver_experience: str = "intermediate"
) -> Dict[str, Any]:
    """
    Recommend appropriate equalisation technique based on depth and experience.
    """

    techniques = {
        "valsalva": {
            "name": "Valsalva Maneuver",
            "description": "Pinch nose and gently blow with mouth closed",
            "difficulty": "Easy",
            "best_for": "Shallow depths, beginners",
            "warning": "Do not blow too hard. Can damage ear drums."
        },
        "frensel": {
            "name": "Frensel Technique",
            "description": "Use throat muscles to push air without using lungs",
            "difficulty": "Moderate",
            "best_for": "Deeper dives, experienced divers",
            "warning": "Requires practice to master"
        },
        "toyne": {
            "name": "Toyne Method",
            "description": "Try to say 'koo-koo' while pinching nose",
            "difficulty": "Moderate",
            "best_for": "Medium depths, controlled descents",
            "warning": "Useful alternative if Valsalva fails"
        },
        "edentulous": {
            "name": "Edentulous Technique",
            "description": "For divers without teeth, use tongue against soft palate",
            "difficulty": "Easy",
            "best_for": "Divers with dental issues",
            "warning": "Limited power but safer for ears"
        }
    }

    ## Depth-based recommendation
    if depth <= 10:
        recommended = ["valsalva", "edentulous"]
        frequency = "Every 1 to 2 meters"
    elif depth <= 20:
        recommended = ["valsalva", "toyne"]
        frequency = "Every meter during descent"
    else:
        recommended = ["frensel", "toyne"]
        frequency = "Every 0.5 to 1 meter. Pre-equalise before descent"

    ## Experience-based adjustment
    if diver_experience == "beginner":
        recommended = ["valsalva", "edentulous"]
    elif diver_experience == "advanced":
        recommended = ["frensel", "toyne"] + recommended

    return {
        "recommended_techniques": [techniques[t] for t in recommended],
        "frequency": frequency,
        "depth_category": (
            "shallow" if depth <= 10 else
            "medium" if depth <= 20 else
            "deep"
        ),
        "pre_descent_tip": "Practice equalisation on the surface before descending"
    }


def get_ear_safety_tips(
    depth: float,
    water_temp: float = 25.0
) -> List[str]:
    """
    Get depth-specific ear safety tips for scuba divers.
    """

    tips = [
        "Equalise early and often before discomfort begins",
        "Descend feet-first for better pressure control",
        "Never force equalisation. Pain is a warning sign",
        "If pain occurs, ascend slightly and retry",
        "Stay relaxed. Tension reduces equalisation efficiency"
    ]

    ## Depth-specific tips
    if depth > 10:
        tips.append("! Pressure increases rapidly beyond 10m. Equalise every meter")

    if depth > 15:
        tips.append("! Use a descent line for controlled descent")
        tips.append("! Monitor depth gauge closely")

    if depth > 20:
        tips.append("! Depths beyond 20m require advanced equalisation")
        tips.append("! Consider shallower dives if ear issues exist")

    ## Temperature-specific tips
    if water_temp < 20:
        tips.append("! Cold water tightens tissues. Equalise more frequently")
        tips.append("! A hooded wetsuit may help protect ears")

    if water_temp < 15:
        tips.append("! Very cold water greatly increases ear injury risk")
        tips.append("! Reduce depth in cold conditions")

    ## General tips
    tips.extend([
        "Practice equalisation techniques in shallow water",
        "Do not rush the descent",
        "Listen for the pop sound indicating tube opening",
        "Avoid diving with congestion or sinus infections"
    ])

    return tips


def get_ear_care_recommendations(
    depth: float,
    descent_rate: float = 5.0,
    water_temp: float = 25.0,
    diver_experience: str = "intermediate"
) -> Dict[str, Any]:
    """
    Get comprehensive ear care recommendations for a dive.
    """

    risk = calculate_ear_pressure_risk(depth, descent_rate, water_temp)
    techniques = get_equalisation_technique(depth, diver_experience)
    tips = get_ear_safety_tips(depth, water_temp)

    ## Recommended maximum depth
    if risk["risk_level"] in ["LOW", "MODERATE"]:
        max_recommended_depth = depth + 10
    else:
        max_recommended_depth = depth

    ## Summary message
    if risk["risk_level"] == "LOW":
        summary = "Dive conditions are favourable for ear equalisation."
    elif risk["risk_level"] == "MODERATE":
        summary = "Standard precautions should ensure safe equalisation."
    elif risk["risk_level"] == "HIGH":
        summary = "Extra care is required during descent."
    else:
        summary = "Shallower dives are advised to reduce ear stress."

    return {
        "summary": summary,
        "risk_assessment": risk,
        "equalisation": techniques,
        "safety_tips": tips,
        "max_recommended_depth": round(max_recommended_depth, 1),
        "warnings": [
            "Never dive with ear congestion or infection",
            "Abort the dive if pain persists",
            "Consult a diving medicine specialist for recurring issues"
        ]
    }


def quick_ear_risk_check(depth: float) -> str:
    """
    Quick check of ear risk level based only on depth.
    """

    if depth <= 10:
        return "🟢 LOW - Standard equalisation"
    elif depth <= 15:
        return "🟡 MODERATE - Equalise frequently"
    elif depth <= 20:
        return "🟠 HIGH - Use proper technique"
    elif depth <= 30:
        return "🔴 VERY HIGH - Advanced equalisation required"
    else:
        return "🔴 EXTREME - Consider shallower dive"