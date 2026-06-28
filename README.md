# 🏙️ UrbanIQ AI — Business Location Intelligence Platform

> AI-powered platform that helps entrepreneurs find the perfect business location in NCR using data-driven scoring and intelligent recommendations.

![Python](https://img.shields.io/badge/Python-3.13-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.58-red?style=flat-square&logo=streamlit)
![SQLite](https://img.shields.io/badge/SQLite-Database-green?style=flat-square&logo=sqlite)
![Plotly](https://img.shields.io/badge/Plotly-Charts-purple?style=flat-square&logo=plotly)
![Folium](https://img.shields.io/badge/Folium-Maps-darkgreen?style=flat-square)

## 🌍 Live Demo
👉 **[urbaniq-ai.streamlit.app](https://urbaniq-ai.streamlit.app)**

---

## 🎯 Problem Statement

Choosing the right business location is difficult. A person has to manually check:
- Population & income data
- Commercial rent prices
- Metro connectivity
- Competition levels
- Growth trends
- Hospital & school proximity

**UrbanIQ AI solves this** by analyzing all these factors together and recommending the best locations using intelligent weighted scoring.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🗺️ **Interactive Map** | Dark NCR map with heatmaps, animated clusters and rich popups |
| 🧠 **AI Scoring Engine** | Business-specific weighted scoring for 8 business types |
| 📊 **Deep Analytics** | 6+ interactive Plotly charts across all metrics |
| 🏆 **Smart Rankings** | Ranked recommendations with AI-generated explanations |
| 🤖 **AI Business Advisor** | Natural language query → instant location recommendations |
| ⚖️ **Area Comparison** | Side-by-side comparison with radar charts |
| 🔐 **Authentication** | Secure login/signup with SQLite |
| 🎨 **Landing Page** | Professional SaaS-style landing page |

---

## 🏢 Supported Business Types

| Business | Key Factors |
|---|---|
| ☕ Cafe | Office density, metro, footfall, sentiment |
| 🍕 Restaurant | Population, footfall, income, parking |
| 🏋 Gym | Population, competition, metro, income |
| 💊 Pharmacy | Hospitals, population, competition |
| 🛒 Grocery Store | Population, competition, rent, growth |
| 💻 Co-working | Office density, metro, income |
| 👕 Clothing Store | Income, footfall, sentiment |
| 📚 Bookstore | Schools, competition, income |

---

## 📊 Data Coverage

- **60+ NCR Areas** across Noida, Delhi, Gurgaon, Ghaziabad, Greater Noida
- **12 metrics** per area — population, income, rent, metro, hospitals, schools, competition, office density, growth, sentiment, footfall, parking
- **900+ data points** powering the recommendation engine

---

## 🏗️ System Architecture
Raw Data (CSV)

↓

Data Cleaning (Pandas)

↓

SQLite Database

↓

Feature Engineering + Normalization

↓

Weighted Scoring Engine

↓

Recommendation Engine

↓

Streamlit Dashboard + AI Advisor
---

## 🧠 How the Scoring Works

Each business type has a unique weight profile. For example, a **Cafe**:

```python
weights = {
    "office_norm":      0.25,  # Near offices
    "metro_norm":       0.20,  # Metro access
    "footfall_norm":    0.20,  # High footfall
    "sentiment_norm":   0.15,  # Positive area
    "competition_norm": 0.10,  # Low competition
    "rent_norm":        0.10,  # Affordable rent
}
```

All values are normalized to 0-1, then multiplied by weights and scaled to 0-100.

---

## 💻 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.13 |
| Dashboard | Streamlit |
| Database | SQLite |
| Data Analysis | Pandas, NumPy |
| Visualization | Plotly |
| Maps | Folium, streamlit-folium |
| ML | Scikit-learn |
| Version Control | Git + GitHub |
| Deployment | Streamlit Community Cloud |

---

## 🚀 Run Locally

```bash
# Clone the repository
git clone https://github.com/RKJAIN001/UrbanIQ-AI.git
cd UrbanIQ-AI

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Initialize database
python setup.py

# Run the app
streamlit run main.py
```

---

## 📁 Project Structure
UrbanIQ-AI/

├── main.py                    # App entry point

├── setup.py                   # Database initializer

├── requirements.txt           # Dependencies

├── data/

│   ├── raw/

│   │   ├── locations.csv      # Main dataset (60 areas)

│   │   └── enhanced_dataset.py

│   └── processed/

│       ├── locations_processed.csv

│       └── feature_engineering.py

├── database/

│   └── db_setup.py

├── engine/

│   ├── recommender.py         # Core scoring engine

│   ├── business_profiles.py   # Business weight profiles

│   ├── map_engine.py          # Folium map builder

│   └── ai_advisor.py          # NLP recommendation engine

├── dashboard/

│   ├── landing.py             # Landing page

│   ├── auth.py                # Login/signup

│   ├── home.py                # Home dashboard

│   ├── map_page.py            # Interactive map

│   ├── rankings.py            # Location rankings

│   ├── analytics.py           # Analytics charts

│   ├── ai_advisor.py          # AI advisor page

│   └── compare.py             # Area comparison

└── .streamlit/

└── config.toml            # Streamlit config