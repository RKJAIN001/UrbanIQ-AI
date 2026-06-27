# engine/ai_advisor.py
# UrbanIQ AI Business Advisor — Pure Python NLP Engine

import re
import pandas as pd
from engine.recommender import get_recommendations, explain_recommendation
from engine.business_profiles import BUSINESS_PROFILES, get_display_names

# ── Keyword Maps ───────────────────────────────────────────────
BUSINESS_KEYWORDS = {
    "cafe":           ["cafe", "coffee", "coffee shop", "cafeteria", "tea shop"],
    "restaurant":     ["restaurant", "food", "dining", "eatery", "dhaba", "bistro"],
    "gym":            ["gym", "fitness", "workout", "exercise", "health club"],
    "pharmacy":       ["pharmacy", "medical", "medicine", "chemist", "drugstore"],
    "grocery_store":  ["grocery", "supermarket", "kirana", "general store", "provisions"],
    "coworking":      ["coworking", "co-working", "office space", "workspace", "cowork"],
    "clothing_store": ["clothing", "clothes", "fashion", "apparel", "garments", "boutique"],
    "bookstore":      ["bookstore", "book shop", "books", "stationery", "library"]
}

CITY_KEYWORDS = {
    "Noida":         ["noida", "sector"],
    "Delhi":         ["delhi", "new delhi", "ndmc"],
    "Gurgaon":       ["gurgaon", "gurugram", "cyber city"],
    "Ghaziabad":     ["ghaziabad", "gzb", "indirapuram", "vaishali"],
    "Greater Noida": ["greater noida", "knowledge park", "greater"]
}

def extract_business_type(text):
    """Extract business type from user query"""
    text_lower = text.lower()
    for business, keywords in BUSINESS_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                return business
    return None

def extract_city(text):
    """Extract city from user query"""
    text_lower = text.lower()
    for city, keywords in CITY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                return city
    return "All"

def extract_budget(text):
    """Extract budget from user query"""
    # Match patterns like 50000, 50,000, 50k, ₹50000
    patterns = [
        r'₹\s*(\d+[\d,]*)',
        r'rs\.?\s*(\d+[\d,]*)',
        r'budget\s*(?:of|is|=)?\s*(\d+[\d,]*)',
        r'(\d+)k\b',
        r'(\d{4,})'
    ]

    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            value = match.group(1).replace(",", "")
            # Handle 'k' suffix
            if 'k' in text.lower()[match.start():match.end()]:
                return int(value) * 1000
            return int(value)
    return None

def generate_response(query):
    """
    Main AI advisor function
    Takes user query, returns structured response
    """
    response = {
        "understood": {},
        "recommendations": [],
        "message": "",
        "error": None
    }

    # ── Step 1: Extract intent ─────────────────────────────────
    business_type = extract_business_type(query)
    city          = extract_city(query)
    budget        = extract_budget(query)

    response["understood"] = {
        "business": business_type,
        "city":     city,
        "budget":   budget
    }

    # ── Step 2: Validate ───────────────────────────────────────
    if not business_type:
        response["error"] = (
            "I couldn't identify the business type. "
            "Try mentioning: cafe, gym, restaurant, pharmacy, "
            "grocery store, coworking, clothing store, or bookstore."
        )
        return response

    # ── Step 3: Get recommendations ───────────────────────────
    results = get_recommendations(business_type, city, top_n=5)

    if results.empty:
        response["error"] = (
            f"No locations found for {business_type} in {city}. "
            "Try selecting 'All' cities."
        )
        return response

    # ── Step 4: Filter by budget ───────────────────────────────
    if budget:
        budget_filtered = results[results["avg_rent"] <= budget]
        if not budget_filtered.empty:
            results = budget_filtered
        else:
            response["message"] = (
                f"No areas found within ₹{budget:,} budget. "
                f"Showing closest options above budget."
            )

    # ── Step 5: Build recommendation objects ──────────────────
    profile = BUSINESS_PROFILES[business_type]
    recs    = []

    for _, row in results.head(3).iterrows():
        explanations = explain_recommendation(row, business_type)
        recs.append({
            "rank":         int(row["rank"]),
            "area":         row["area"],
            "city":         row["city"],
            "score":        row["business_score"],
            "rent":         int(row["avg_rent"]),
            "metro":        row["metro_distance_km"],
            "competition":  row["competition_score"],
            "growth":       row["growth_rate"],
            "income":       int(row["avg_income"]),
            "hospitals":    int(row["hospitals_nearby"]),
            "explanations": explanations
        })

    response["recommendations"] = recs
    response["profile"]         = profile
    response["business_type"]   = business_type

    return response