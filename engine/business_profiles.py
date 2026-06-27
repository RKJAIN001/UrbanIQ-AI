# engine/business_profiles.py
BUSINESS_PROFILES = {
    "cafe": {
        "display_name": "☕ Cafe",
        "weights": {
            "office_norm":      0.30,
            "metro_norm":       0.25,
            "sentiment_norm":   0.20,
            "competition_norm": 0.15,
            "rent_norm":        0.10,
        },
        "description": "Cafes thrive near offices and metro stations with high footfall.",
        "ideal_for": ["office areas", "metro hubs", "college zones"]
    },

    "restaurant": {
        "display_name": "🍕 Restaurant",
        "weights": {
            "pop_norm":         0.30,
            "sentiment_norm":   0.25,
            "income_norm":      0.20,
            "competition_norm": 0.15,
            "rent_norm":        0.10,
        },
        "description": "Restaurants need high population, good income and positive area sentiment.",
        "ideal_for": ["residential zones", "market areas", "entertainment hubs"]
    },

    "gym": {
        "display_name": "🏋 Gym",
        "weights": {
            "pop_norm":         0.30,
            "competition_norm": 0.30,
            "metro_norm":       0.20,
            "rent_norm":        0.10,
            "growth_norm":      0.10,
        },
        "description": "Gyms need working professionals, metro access and low competition.",
        "ideal_for": ["residential areas", "office zones", "metro corridors"]
    },

    "pharmacy": {
        "display_name": "💊 Pharmacy",
        "weights": {
            "hospitals_norm":   0.35,
            "pop_norm":         0.30,
            "competition_norm": 0.20,
            "rent_norm":        0.10,
            "metro_norm":       0.05,
        },
        "description": "Pharmacies need high population density and proximity to hospitals.",
        "ideal_for": ["hospital zones", "residential areas", "market areas"]
    },

    "grocery_store": {
        "display_name": "🛒 Grocery Store",
        "weights": {
            "pop_norm":         0.40,
            "competition_norm": 0.25,
            "rent_norm":        0.20,
            "growth_norm":      0.15,
        },
        "description": "Grocery stores need dense residential population and low competition.",
        "ideal_for": ["residential colonies", "new townships", "growing areas"]
    },

    "coworking": {
        "display_name": "💻 Co-working Space",
        "weights": {
            "office_norm":      0.35,
            "metro_norm":       0.30,
            "income_norm":      0.20,
            "competition_norm": 0.10,
            "rent_norm":        0.05,
        },
        "description": "Co-working spaces need corporate zones, metro access and high income areas.",
        "ideal_for": ["IT corridors", "business districts", "metro hubs"]
    },

    "clothing_store": {
        "display_name": "👕 Clothing Store",
        "weights": {
            "income_norm":      0.35,
            "sentiment_norm":   0.25,
            "pop_norm":         0.20,
            "competition_norm": 0.10,
            "metro_norm":       0.10,
        },
        "description": "Clothing stores need high income shoppers and good footfall areas.",
        "ideal_for": ["market areas", "malls", "high income zones"]
    },

    "bookstore": {
        "display_name": "📚 Bookstore",
        "weights": {
            "schools_norm":     0.35,
            "competition_norm": 0.25,
            "income_norm":      0.20,
            "rent_norm":        0.10,
            "sentiment_norm":   0.10,
        },
        "description": "Bookstores need educated population, schools nearby and low competition.",
        "ideal_for": ["educational zones", "residential areas", "college hubs"]
    }
}

def get_business_types():
    return list(BUSINESS_PROFILES.keys())

def get_display_names():
    return {k: v["display_name"] for k, v in BUSINESS_PROFILES.items()}