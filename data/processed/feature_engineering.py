# data/processed/feature_engineering.py
import pandas as pd
import numpy as np
import sqlite3

def normalize(series):
    min_val = series.min()
    max_val = series.max()
    if max_val == min_val:
        return pd.Series([0.5] * len(series), index=series.index)
    return (series - min_val) / (max_val - min_val)

def feature_engineering():
    conn = sqlite3.connect("database/urbaniq.db")
    df = pd.read_sql("SELECT * FROM locations", conn)
    conn.close()

    print("✅ Data loaded from database")
    print(f"   Shape: {df.shape}")

    # ── Normalize all columns ──────────────────────────────────
    df["pop_norm"]         = normalize(df["population_density"])
    df["income_norm"]      = normalize(df["avg_income"])
    df["metro_norm"]       = normalize(1 / (df["metro_distance_km"] + 0.1))
    df["hospitals_norm"]   = normalize(df["hospitals_nearby"])
    df["schools_norm"]     = normalize(df["schools_nearby"])
    df["office_norm"]      = normalize(df["office_density"])
    df["growth_norm"]      = normalize(df["growth_rate"])
    df["sentiment_norm"]   = normalize(df["sentiment_score"])
    df["rent_norm"]        = normalize(1 / df["avg_rent"])
    df["competition_norm"] = normalize(1 / df["competition_score"])
    df["footfall_norm"]    = normalize(df["footfall_score"])
    df["parking_norm"]     = normalize(df["parking_score"])

    print("✅ Normalization complete")

    # ── General Opportunity Score ──────────────────────────────
    df["opportunity_score"] = (
        df["pop_norm"]         * 0.12 +
        df["income_norm"]      * 0.12 +
        df["metro_norm"]       * 0.12 +
        df["office_norm"]      * 0.10 +
        df["growth_norm"]      * 0.12 +
        df["sentiment_norm"]   * 0.10 +
        df["rent_norm"]        * 0.10 +
        df["competition_norm"] * 0.10 +
        df["footfall_norm"]    * 0.06 +
        df["parking_norm"]     * 0.06
    ) * 100

    df["opportunity_score"] = df["opportunity_score"].round(2)

    # ── Save ───────────────────────────────────────────────────
    df.to_csv("data/processed/locations_processed.csv", index=False)

    conn = sqlite3.connect("database/urbaniq.db")
    df.to_sql("locations_processed", conn, if_exists="replace", index=False)
    conn.close()

    print("✅ Opportunity scores calculated")
    print("✅ Processed data saved")
    print()

    top5 = df[["area", "city", "opportunity_score"]].sort_values(
        "opportunity_score", ascending=False
    ).head(5)

    print("🏆 Top 5 Areas by Opportunity Score:")
    print(top5.to_string(index=False))

if __name__ == "__main__":
    feature_engineering()