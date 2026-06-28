# dashboard/home.py
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

def load_data():
    conn = sqlite3.connect("database/urbaniq.db")
    df = pd.read_sql("SELECT * FROM locations_processed", conn)
    conn.close()
    return df

def show_home():
    df = load_data()

    st.markdown("""
    <style>
    .stApp { background-color: #050816 !important; }
    @keyframes fade-up {
        from { opacity:0; transform:translateY(16px); }
        to   { opacity:1; transform:translateY(0); }
    }
    .home-header {
        background: linear-gradient(135deg, #0a0f1e, #0d1a2e);
        border: 1px solid #1e293b;
        border-radius: 20px;
        padding: 40px 48px;
        margin-bottom: 32px;
        position: relative;
        overflow: hidden;
        animation: fade-up 0.6s ease both;
    }
    .home-header::before {
        content: '';
        position: absolute;
        top: -50%; right: -10%;
        width: 400px; height: 400px;
        background: radial-gradient(circle, #7c3aed11, transparent 70%);
        pointer-events: none;
    }
    .home-title {
        font-size: 36px;
        font-weight: 800;
        color: #fff;
        margin: 0 0 8px 0;
    }
    .home-sub {
        font-size: 15px;
        color: #475569;
        margin: 0;
    }
    .kpi-card {
        background: #0a0f1e;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 24px;
        transition: all 0.3s;
        text-align: center;
    }
    .kpi-card:hover {
        border-color: rgba(14,165,233,0.3);
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(14,165,233,0.08);
    }
    .kpi-icon { font-size: 28px; margin-bottom: 8px; }
    .kpi-value {
        font-size: 28px; font-weight: 800;
        background: linear-gradient(135deg, #0ea5e9, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }
    .kpi-label { font-size: 12px; color: #475569; letter-spacing: 1px; }
    .top-area-card {
        background: #0a0f1e;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s;
        height: 100%;
    }
    .top-area-card:hover {
        border-color: rgba(124,58,237,0.3);
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(124,58,237,0.1);
    }
    .medal { font-size: 40px; margin-bottom: 12px; }
    .area-name {
        font-size: 20px; font-weight: 700;
        color: #fff; margin-bottom: 4px;
    }
    .area-city { font-size: 13px; color: #475569; margin-bottom: 16px; }
    .score-badge {
        background: linear-gradient(135deg, #0ea5e9, #7c3aed);
        border-radius: 10px; padding: 10px;
        font-size: 24px; font-weight: 800;
        color: white; margin-bottom: 16px;
    }
    .area-stat {
        font-size: 12px; color: #475569;
        margin: 4px 0; text-align: left;
    }
    .biz-type-card {
        background: #0a0f1e;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 16px 8px;
        text-align: center;
        transition: all 0.3s;
        cursor: pointer;
    }
    .biz-type-card:hover {
        border-color: rgba(14,165,233,0.4);
        background: rgba(14,165,233,0.05);
        transform: translateY(-4px);
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Header ─────────────────────────────────────────────────
    user = st.session_state.get("user_name", "User")
    st.markdown(f"""
    <div class="home-header">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div class="home-title">Welcome back, {user}! 👋</div>
                <div class="home-sub">
                    Here's your NCR business intelligence dashboard
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:12px; color:#475569;">Last updated</div>
                <div style="font-size:14px; color:#0ea5e9; font-weight:600;">
                    Live Data · 60 Areas
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Cards ──────────────────────────────────────────────
    best_area  = df.loc[df["opportunity_score"].idxmax()]
    avg_rent   = int(df["avg_rent"].mean())
    top_growth = df.loc[df["growth_rate"].idxmax()]
    low_comp   = df.loc[df["competition_score"].idxmin()]
    avg_score  = df["opportunity_score"].mean()

    kpis = [
        ("📍", str(len(df)), "AREAS ANALYZED"),
        ("🏆", best_area["area"], "BEST AREA"),
        ("💰", f"₹{avg_rent:,}", "AVG RENT"),
        ("📈", top_growth["area"], "HIGHEST GROWTH"),
        ("⚔️", low_comp["area"], "LOW COMPETITION"),
        ("⭐", f"{avg_score:.1f}", "AVG SCORE"),
    ]

    cols = st.columns(6)
    for i, (icon, value, label) in enumerate(kpis):
        with cols[i]:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">{icon}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Top 3 Areas ────────────────────────────────────────────
    st.markdown("""
    <div style="font-size:22px; font-weight:800; color:#fff;
                margin-bottom:4px;">🏆 Top Opportunity Areas</div>
    <div style="font-size:14px; color:#475569; margin-bottom:20px;">
        Ranked by overall opportunity score across all business types
    </div>
    """, unsafe_allow_html=True)

    top3   = df.nlargest(3, "opportunity_score").reset_index(drop=True)
    medals = ["🥇", "🥈", "🥉"]
    cols   = st.columns(3)

    for i, row in top3.iterrows():
        with cols[i]:
            st.markdown(f"""
            <div class="top-area-card">
                <div class="medal">{medals[i]}</div>
                <div class="area-name">{row['area']}</div>
                <div class="area-city">{row['city']}</div>
                <div class="score-badge">{row['opportunity_score']}</div>
                <div style="font-size:11px; color:#475569;
                            margin-bottom:8px;">OPPORTUNITY SCORE</div>
                <div class="area-stat">🚇 Metro: {row['metro_distance_km']} km</div>
                <div class="area-stat">💰 Income: ₹{int(row['avg_income']):,}</div>
                <div class="area-stat">📈 Growth: {row['growth_rate']}%</div>
                <div class="area-stat">⚔️ Competition: {row['competition_score']}/10</div>
                <div class="area-stat">🏠 Rent: ₹{int(row['avg_rent']):,}/mo</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Quick Chart ────────────────────────────────────────────
    st.markdown("""
    <div style="font-size:22px; font-weight:800; color:#fff;
                margin-bottom:4px;">📊 Quick Insights</div>
    <div style="font-size:14px; color:#475569; margin-bottom:20px;">
        Top 10 areas by opportunity score
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        top10 = df.nlargest(10, "opportunity_score")
        fig = px.bar(
            top10,
            x="opportunity_score",
            y="area",
            orientation="h",
            color="opportunity_score",
            color_continuous_scale=["#1e293b", "#0ea5e9", "#7c3aed"],
            template="plotly_dark",
        )
        fig.update_layout(
            plot_bgcolor="#0a0f1e",
            paper_bgcolor="#0a0f1e",
            font_color="#e2e8f0",
            showlegend=False,
            height=380,
            margin=dict(l=10, r=10, t=10, b=10),
            coloraxis_showscale=False,
            xaxis=dict(gridcolor="#1e293b"),
            yaxis=dict(gridcolor="#1e293b"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        city_avg = df.groupby("city")["opportunity_score"].mean().reset_index()
        fig2 = px.bar(
            city_avg,
            x="city",
            y="opportunity_score",
            color="opportunity_score",
            color_continuous_scale=["#1e293b", "#7c3aed", "#0ea5e9"],
            template="plotly_dark",
            labels={"opportunity_score": "Avg Score", "city": "City"}
        )
        fig2.update_layout(
            plot_bgcolor="#0a0f1e",
            paper_bgcolor="#0a0f1e",
            font_color="#e2e8f0",
            showlegend=False,
            height=380,
            margin=dict(l=10, r=10, t=10, b=10),
            coloraxis_showscale=False,
            xaxis=dict(gridcolor="#1e293b"),
            yaxis=dict(gridcolor="#1e293b"),
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Business Types ─────────────────────────────────────────
    st.markdown("""
    <div style="font-size:22px; font-weight:800; color:#fff;
                margin-bottom:4px;">🏢 Supported Business Types</div>
    <div style="font-size:14px; color:#475569; margin-bottom:20px;">
        Each business type has unique AI-powered scoring weights
    </div>
    """, unsafe_allow_html=True)

    businesses = [
        ("☕", "Cafe",          "Office zones, metro hubs"),
        ("🍕", "Restaurant",    "Residential, markets"),
        ("🏋", "Gym",           "Working professionals"),
        ("💊", "Pharmacy",      "Hospital zones"),
        ("🛒", "Grocery Store", "Residential colonies"),
        ("💻", "Co-working",    "IT corridors"),
        ("👕", "Clothing",      "Market areas, malls"),
        ("📚", "Bookstore",     "Educational zones"),
    ]

    cols = st.columns(8)
    for i, (icon, name, desc) in enumerate(businesses):
        with cols[i]:
            st.markdown(f"""
            <div class="biz-type-card">
                <div style="font-size:28px;">{icon}</div>
                <div style="font-size:12px; color:#e2e8f0;
                            font-weight:600; margin-top:8px;">{name}</div>
                <div style="font-size:10px; color:#475569;
                            margin-top:4px;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)