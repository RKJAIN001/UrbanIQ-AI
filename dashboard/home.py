# dashboard/home.py
import streamlit as st
import pandas as pd
import sqlite3

def load_data():
    conn = sqlite3.connect("database/urbaniq.db")
    df = pd.read_sql("SELECT * FROM locations_processed", conn)
    conn.close()
    return df

def show_home():
    df = load_data()

    # ── Hero Section ───────────────────────────────────────────
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1e1e2e 0%, #2d1b69 50%, #1e1e2e 100%);
        border: 1px solid #2d2d44;
        border-radius: 16px;
        padding: 48px 40px;
        text-align: center;
        margin-bottom: 32px;
    ">
        <div style="font-size:56px; margin-bottom:16px;">🏙️</div>
        <h1 style="
            font-size: 42px;
            font-weight: 800;
            color: #fff;
            margin: 0 0 12px 0;
        ">UrbanIQ AI</h1>
        <p style="font-size:18px; color:#94a3b8; margin:0 0 8px 0;">
            AI-Powered Business Location Intelligence
        </p>
        <p style="font-size:14px; color:#64748b;">
            Analyze 30+ NCR locations across 8 business types using data-driven scoring
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Cards ──────────────────────────────────────────────
    best_area  = df.loc[df["opportunity_score"].idxmax()]
    avg_rent   = int(df["avg_rent"].mean())
    top_growth = df.loc[df["growth_rate"].idxmax()]
    low_comp   = df.loc[df["competition_score"].idxmin()]

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("📍 Areas Analyzed", f"{len(df)}")
    col2.metric("🏆 Best Area",       best_area["area"])
    col3.metric("💰 Avg Rent",        f"₹{avg_rent:,}")
    col4.metric("📈 Highest Growth",  top_growth["area"])
    col5.metric("⚔️ Lowest Competition", low_comp["area"])

    st.divider()

    # ── Top 3 Areas ────────────────────────────────────────────
    st.markdown("## 🏆 Top Opportunity Areas")
    st.caption("Ranked by overall opportunity score across all business types")

    top3   = df.nlargest(3, "opportunity_score").reset_index(drop=True)
    medals = ["🥇", "🥈", "🥉"]
    cols   = st.columns(3)

    for i, row in top3.iterrows():
        with cols[i]:
            with st.container(border=True):
                st.markdown(f"### {medals[i]} {row['area']}")
                st.caption(row['city'])
                st.metric("Opportunity Score", row['opportunity_score'])
                st.divider()
                st.caption(f"🚇 Metro: {row['metro_distance_km']} km")
                st.caption(f"💰 Income: ₹{int(row['avg_income']):,}")
                st.caption(f"📈 Growth: {row['growth_rate']}%")
                st.caption(f"⚔️ Competition: {row['competition_score']}/10")

    st.divider()

    # ── Business Types ─────────────────────────────────────────
    st.markdown("## 🏢 Supported Business Types")
    st.caption("Select any business type for tailored location recommendations")

    businesses = [
        ("☕", "Cafe",           "Office zones, metro hubs"),
        ("🍕", "Restaurant",     "Residential, markets"),
        ("🏋", "Gym",            "Working professionals"),
        ("💊", "Pharmacy",       "Hospital zones"),
        ("🛒", "Grocery Store",  "Residential colonies"),
        ("💻", "Co-working",     "IT corridors"),
        ("👕", "Clothing Store", "Market areas, malls"),
        ("📚", "Bookstore",      "Educational zones"),
    ]

    cols = st.columns(4)
    for i, (icon, name, desc) in enumerate(businesses):
        with cols[i % 4]:
            with st.container(border=True):
                st.markdown(f"### {icon} {name}")
                st.caption(desc)