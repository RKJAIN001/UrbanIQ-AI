# data/raw/locations.py
# UrbanIQ AI - NCR Location Dataset
# We are creating realistic data for 30 areas across NCR

import pandas as pd
import os

def create_locations_dataset():
    data = {
        "area": [
            "Sector 18", "Sector 62", "Sector 63", "Sector 15",
            "Rajnagar Extension", "Sector 50", "Sector 137", "Sector 76",
            "Cyber City", "Sohna Road", "MG Road", "Sector 56",
            "Connaught Place", "Lajpat Nagar", "Rajouri Garden",
            "Dwarka Sector 10", "Saket", "Nehru Place", "Karol Bagh",
            "Janakpuri", "Rohini Sector 3", "Pitampura", "Preet Vihar",
            "Vaishali", "Indirapuram", "Crossings Republik",
            "Greater Noida West", "Knowledge Park", "Raj Nagar",
            "Vasundhara"
        ],
        "city": [
            "Noida", "Noida", "Noida", "Noida",
            "Ghaziabad", "Noida", "Noida", "Noida",
            "Gurgaon", "Gurgaon", "Gurgaon", "Gurgaon",
            "Delhi", "Delhi", "Delhi",
            "Delhi", "Delhi", "Delhi", "Delhi",
            "Delhi", "Delhi", "Delhi", "Delhi",
            "Ghaziabad", "Ghaziabad", "Ghaziabad",
            "Greater Noida", "Greater Noida", "Ghaziabad",
            "Ghaziabad"
        ],
        "latitude": [
            28.5700, 28.6270, 28.6210, 28.5830,
            28.6820, 28.5680, 28.5080, 28.5740,
            28.4950, 28.4230, 28.4800, 28.4230,
            28.6330, 28.5650, 28.6490,
            28.5921, 28.5245, 28.5491, 28.6510,
            28.6280, 28.7330, 28.7010, 28.6430,
            28.6450, 28.6430, 28.6580,
            28.6139, 28.4744, 28.6630,
            28.6480
        ],
        "longitude": [
            77.3260, 77.3680, 77.3810, 77.3160,
            77.4490, 77.3540, 77.3570, 77.3830,
            77.0870, 77.0420, 77.0800, 77.0800,
            77.2197, 77.2440, 77.1220,
            77.0590, 77.2167, 77.2510, 77.1900,
            77.0870, 77.1100, 77.1300, 77.2960,
            77.3380, 77.3700, 77.4120,
            77.4290, 77.4840, 77.4150,
            77.3560
        ],
        "population_density": [
            85, 72, 68, 78,
            65, 70, 55, 60,
            90, 62, 88, 65,
            95, 88, 82,
            75, 85, 80, 90,
            78, 72, 76, 74,
            70, 73, 60,
            52, 45, 68,
            66
        ],
        "avg_income": [
            75000, 82000, 78000, 70000,
            55000, 80000, 65000, 68000,
            95000, 85000, 90000, 80000,
            88000, 72000, 68000,
            65000, 85000, 78000, 70000,
            62000, 58000, 65000, 60000,
            68000, 70000, 52000,
            48000, 55000, 58000,
            62000
        ],
        "avg_rent": [
            85000, 55000, 50000, 60000,
            35000, 65000, 40000, 45000,
            120000, 75000, 95000, 70000,
            150000, 90000, 75000,
            55000, 100000, 85000, 80000,
            60000, 45000, 55000, 50000,
            42000, 45000, 32000,
            28000, 30000, 38000,
            40000
        ],
        "metro_distance_km": [
            0.3, 0.5, 1.2, 0.8,
            3.5, 1.0, 2.5, 1.8,
            0.2, 2.0, 0.4, 2.5,
            0.1, 0.3, 0.2,
            0.4, 0.5, 0.3, 0.4,
            0.6, 0.5, 0.4, 0.8,
            0.6, 1.2, 3.0,
            4.0, 5.0, 2.8,
            2.2
        ],
        "hospitals_nearby": [
            8, 5, 4, 6,
            3, 5, 3, 4,
            10, 6, 9, 5,
            12, 9, 7,
            6, 10, 8, 9,
            7, 6, 7, 6,
            5, 6, 4,
            3, 3, 5,
            5
        ],
        "schools_nearby": [
            12, 15, 12, 14,
            10, 13, 9, 11,
            8, 10, 9, 11,
            6, 10, 12,
            14, 11, 8, 13,
            15, 14, 13, 12,
            13, 14, 11,
            9, 8, 12,
            13
        ],
        "competition_score": [
            8.5, 6.0, 5.5, 7.0,
            4.0, 6.5, 4.5, 5.0,
            9.0, 6.0, 8.5, 5.5,
            9.5, 8.0, 7.5,
            6.0, 8.5, 8.0, 8.5,
            6.5, 5.5, 6.0, 6.5,
            5.5, 6.0, 4.0,
            3.5, 3.0, 5.0,
            5.5
        ],
        "office_density": [
            9.0, 8.5, 8.0, 7.5,
            4.5, 8.0, 6.0, 6.5,
            9.5, 7.0, 9.0, 7.0,
            8.5, 6.0, 5.5,
            5.0, 7.5, 8.5, 6.5,
            5.5, 4.5, 5.0, 5.5,
            6.0, 6.5, 4.0,
            3.5, 4.0, 5.0,
            5.5
        ],
        "growth_rate": [
            5.5, 8.0, 8.5, 6.0,
            9.0, 7.0, 10.0, 9.5,
            6.0, 9.0, 5.5, 8.0,
            3.0, 4.0, 4.5,
            5.5, 4.0, 3.5, 4.0,
            5.0, 5.5, 5.0, 5.5,
            7.0, 7.5, 10.0,
            11.0, 10.5, 8.5,
            8.0
        ],
        "sentiment_score": [
            8.5, 7.5, 7.0, 7.5,
            6.5, 8.0, 7.0, 7.5,
            9.0, 8.0, 8.5, 7.5,
            8.0, 7.5, 7.5,
            7.0, 8.5, 7.5, 7.5,
            7.0, 6.5, 7.0, 7.0,
            7.5, 7.5, 6.5,
            6.5, 6.0, 7.0,
            7.0
        ]
    }

    df = pd.DataFrame(data)

    # Save to CSV
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/locations.csv", index=False)
    print(f"✅ Dataset created: {len(df)} areas")
    print(df.head())
    return df

if __name__ == "__main__":
    create_locations_dataset()