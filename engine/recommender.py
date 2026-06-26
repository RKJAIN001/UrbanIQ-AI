# engine/recommender.py
# Core scoring and recommendation logic

import pandas as pd
import sqlite3
from engine.business_profiles import BUSINESS_PROFILES

def load_processed_data():
    """Load processed location data from database"""
    conn = sqlite3.connect("database/urbaniq.db")
    df = pd.read_sql("SELECT * FROM locations_processed", conn)
    conn.close()
    return df

def calculate_score(df, business_type):
    """Apply business-specific weights and calculate scores"""
    
    if business_type not in BUSINESS_PROFILES:
        raise ValueError(f"Unknown business type: {business_type}")
    
    profile = BUSINESS_PROFILES[business_type]
    weights = profile["weights"]
    
    # Start with zero score
    score = pd.Series([0.0] * len(df), index=df.index)
    
    # Apply each weight
    for column, weight in weights.items():
        if column in df.columns:
            score += df[column] * weight
    
    # Scale to 0-100
    score = score * 100
    
    return score.round(2)

def get_recommendations(business_type, city_filter=None, top_n=5):
    """
    Main recommendation function
    Returns top N areas for a given business type
    """
    df = load_processed_data()
    
    # Filter by city if specified
    if city_filter and city_filter != "All":
        df = df[df["city"] == city_filter].copy()
    
    # Calculate business-specific scores
    df["business_score"] = calculate_score(df, business_type)
    
    # Sort by score
    df = df.sort_values("business_score", ascending=False).reset_index(drop=True)
    
    # Add rank
    df["rank"] = range(1, len(df) + 1)
    
    # Select output columns
    result = df[[
        "rank", "area", "city", "latitude", "longitude",
        "avg_rent", "metro_distance_km", "competition_score",
        "office_density", "growth_rate", "sentiment_score",
        "population_density", "avg_income", "hospitals_nearby",
        "business_score"
    ]].head(top_n)
    
    return result

def explain_recommendation(area_row, business_type):
    """
    Generate a human-readable explanation for why an area was recommended
    """
    profile = BUSINESS_PROFILES[business_type]
    weights = profile["weights"]
    
    explanations = []
    
    # Metro check
    if "metro_norm" in weights and weights["metro_norm"] >= 0.15:
        dist = area_row["metro_distance_km"]
        if dist <= 0.5:
            explanations.append(f"✓ Metro station very close ({dist} km)")
        elif dist <= 1.5:
            explanations.append(f"✓ Metro station nearby ({dist} km)")

    # Competition check
    if "competition_norm" in weights and weights["competition_norm"] >= 0.10:
        comp = area_row["competition_score"]
        if comp <= 5.0:
            explanations.append(f"✓ Low competition in area (score: {comp}/10)")
        elif comp <= 7.0:
            explanations.append(f"✓ Moderate competition (score: {comp}/10)")

    # Rent check
    rent = area_row["avg_rent"]
    if rent <= 45000:
        explanations.append(f"✓ Affordable rent (₹{rent:,}/month)")
    elif rent <= 70000:
        explanations.append(f"✓ Moderate rent (₹{rent:,}/month)")

    # Office density
    if "office_norm" in weights and weights["office_norm"] >= 0.15:
        if area_row["office_density"] >= 7.0:
            explanations.append(f"✓ High office density — strong footfall")

    # Growth
    if area_row["growth_rate"] >= 8.0:
        explanations.append(f"✓ Fast growing area ({area_row['growth_rate']}% growth)")

    # Sentiment
    if area_row["sentiment_score"] >= 8.0:
        explanations.append(f"✓ Very positive area sentiment")

    # Hospitals for pharmacy
    if "hospitals_norm" in weights:
        explanations.append(f"✓ {area_row['hospitals_nearby']} hospitals nearby")

    return explanations

if __name__ == "__main__":
    # Test the engine
    print("🧠 Testing Recommendation Engine\n")
    
    for business in ["cafe", "gym", "pharmacy", "coworking"]:
        print(f"Top 3 areas for {BUSINESS_PROFILES[business]['display_name']}:")
        results = get_recommendations(business, top_n=3)
        for _, row in results.iterrows():
            print(f"  {row['rank']}. {row['area']} ({row['city']}) — Score: {row['business_score']}")
        print()