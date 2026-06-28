# dashboard/home.py
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

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
        padding: 32px 40px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .home-header::before {
        content: '';
        position: absolute;
        top: -50%; right: -10%;
        width: 400px; height: 400px;
        background: radial-gradient(circle, #7c3aed11, transparent 70%);
        pointer-events: none;
    }
    .kpi-card {
        background: #0a0f1e;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 20px 16px;
        text-align: center;
        transition: all 0.3s;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .kpi-card:hover {
        border-color: rgba(14,165,233,0.3);
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(14,165,233,0.08);
    }
    .kpi-icon { font-size: 22px; margin-bottom: 6px; }
    .kpi-value {
        font-size: 22px; font-weight: 800;
        background: linear-gradient(135deg, #0ea5e9, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .kpi-label {
        font-size: 10px; color: #475569;
        letter-spacing: 0.5px;
        white-space: nowrap;
    }
    .top-area-card {
        background: #0a0f1e;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s;
    }
    .top-area-card:hover {
        border-color: rgba(124,58,237,0.3);
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(124,58,237,0.1);
    }
    .section-title {
        font-size: 20px; font-weight: 800;
        color: #fff; margin-bottom: 4px;
    }
    .section-sub {
        font-size: 13px; color: #475569;
        margin-bottom: 16px;
    }
    .insight-card {
        background: #0a0f1e;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 20px;
        transition: all 0.3s;
    }
    .insight-card:hover {
        border-color: rgba(14,165,233,0.2);
        transform: translateY(-2px);
    }
    .city-card {
        background: #0a0f1e;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        transition: all 0.3s;
    }
    .city-card:hover {
        border-color: rgba(14,165,233,0.3);
        transform: translateY(-3px);
    }
    .biz-card {
        background: #0a0f1e;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 14px 8px;
        text-align: center;
        transition: all 0.3s;
        cursor: pointer;
    }
    .biz-card:hover {
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
        <div style="display:flex; justify-content:space-between;
                    align-items:center;">
            <div>
                <div style="font-size:26px; font-weight:800;
                            color:#fff; margin-bottom:6px;">
                    Welcome back, {user}! 👋
                </div>
                <div style="font-size:13px; color:#475569;">
                    NCR Business Intelligence Dashboard ·
                    Real-time data across 60 areas
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:11px; color:#475569;">
                    Powered by
                </div>
                <div style="font-size:14px; color:#0ea5e9;
                            font-weight:700;">
                    UrbanIQ Engine v2.0
                </div>
                <div style="font-size:11px; color:#334155;
                            margin-top:2px;">
                    60 Areas · 5 Cities · 8 Business Types
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Row 1 ──────────────────────────────────────────────
    best_area  = df.loc[df["opportunity_score"].idxmax()]
    avg_rent   = int(df["avg_rent"].mean())
    top_growth = df.loc[df["growth_rate"].idxmax()]
    low_comp   = df.loc[df["competition_score"].idxmin()]
    avg_score  = round(df["opportunity_score"].mean(), 1)
    avg_income = int(df["avg_income"].mean())

    kpis1 = [
        ("📍", str(len(df)),         "Areas"),
        ("🏆", best_area["area"],    "Best Area"),
        ("💰", f"₹{avg_rent:,}",     "Avg Rent"),
        ("📈", f"{top_growth['growth_rate']}%", "Top Growth"),
        ("⚔️", f"{low_comp['competition_score']}", "Min Competition"),
        ("⭐", str(avg_score),        "Avg Score"),
    ]

    cols = st.columns(6)
    for i, (icon, value, label) in enumerate(kpis1):
        with cols[i]:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">{icon}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── KPI Row 2 ──────────────────────────────────────────────
    max_rent   = int(df["avg_rent"].max())
    min_rent   = int(df["avg_rent"].min())
    avg_metro  = round(df["metro_distance_km"].mean(), 1)
    max_growth = df["growth_rate"].max()
    avg_hosp   = round(df["hospitals_nearby"].mean(), 1)
    avg_school = round(df["schools_nearby"].mean(), 1)

    kpis2 = [
        ("🏠", f"₹{max_rent:,}", "Max Rent"),
        ("💸", f"₹{min_rent:,}", "Min Rent"),
        ("🚇", f"{avg_metro} km", "Avg Metro"),
        ("📊", f"{max_growth}%",  "Max Growth"),
        ("🏥", str(avg_hosp),    "Avg Hospitals"),
        ("🏫", str(avg_school),  "Avg Schools"),
    ]

    cols = st.columns(6)
    for i, (icon, value, label) in enumerate(kpis2):
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
    <div class="section-title">🏆 Top Opportunity Areas</div>
    <div class="section-sub">
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
                <div style="font-size:36px; margin-bottom:8px;">
                    {medals[i]}
                </div>
                <div style="font-size:18px; font-weight:800;
                            color:#fff; margin-bottom:2px;">
                    {row['area']}
                </div>
                <div style="font-size:12px; color:#475569;
                            margin-bottom:14px;">{row['city']}</div>
                <div style="
                    background:linear-gradient(135deg,#0ea5e9,#7c3aed);
                    border-radius:10px; padding:10px;
                    font-size:22px; font-weight:800;
                    color:white; margin-bottom:14px;">
                    {row['opportunity_score']}
                </div>
                <div style="font-size:10px; color:#475569;
                            margin-bottom:12px;
                            letter-spacing:1px;">OPPORTUNITY SCORE</div>
                <div style="display:grid; grid-template-columns:1fr 1fr;
                            gap:6px; text-align:left;">
                    <div style="background:#050816; border-radius:8px;
                                padding:8px;">
                        <div style="font-size:10px; color:#475569;">
                            🚇 Metro
                        </div>
                        <div style="font-size:13px; font-weight:600;
                                    color:#e2e8f0;">
                            {row['metro_distance_km']} km
                        </div>
                    </div>
                    <div style="background:#050816; border-radius:8px;
                                padding:8px;">
                        <div style="font-size:10px; color:#475569;">
                            🏠 Rent
                        </div>
                        <div style="font-size:13px; font-weight:600;
                                    color:#e2e8f0;">
                            ₹{int(row['avg_rent']):,}
                        </div>
                    </div>
                    <div style="background:#050816; border-radius:8px;
                                padding:8px;">
                        <div style="font-size:10px; color:#475569;">
                            📈 Growth
                        </div>
                        <div style="font-size:13px; font-weight:600;
                                    color:#22c55e;">
                            {row['growth_rate']}%
                        </div>
                    </div>
                    <div style="background:#050816; border-radius:8px;
                                padding:8px;">
                        <div style="font-size:10px; color:#475569;">
                            ⚔️ Competition
                        </div>
                        <div style="font-size:13px; font-weight:600;
                                    color:#f59e0b;">
                            {row['competition_score']}/10
                        </div>
                    </div>
                    <div style="background:#050816; border-radius:8px;
                                padding:8px;">
                        <div style="font-size:10px; color:#475569;">
                            💰 Income
                        </div>
                        <div style="font-size:13px; font-weight:600;
                                    color:#e2e8f0;">
                            ₹{int(row['avg_income']):,}
                        </div>
                    </div>
                    <div style="background:#050816; border-radius:8px;
                                padding:8px;">
                        <div style="font-size:10px; color:#475569;">
                            😊 Sentiment
                        </div>
                        <div style="font-size:13px; font-weight:600;
                                    color:#e2e8f0;">
                            {row['sentiment_score']}/10
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── City Overview ──────────────────────────────────────────
    st.markdown("""
    <div class="section-title">🌆 City Overview</div>
    <div class="section-sub">
        Average metrics across all 5 NCR cities
    </div>
    """, unsafe_allow_html=True)

    cities = df.groupby("city").agg(
        areas=("area", "count"),
        avg_score=("opportunity_score", "mean"),
        avg_rent=("avg_rent", "mean"),
        avg_growth=("growth_rate", "mean"),
        avg_income=("avg_income", "mean"),
        avg_competition=("competition_score", "mean"),
    ).reset_index().round(1)

    cols = st.columns(5)
    city_icons = {
        "Noida": "🏙️",
        "Delhi": "🏛️",
        "Gurgaon": "💼",
        "Ghaziabad": "🏘️",
        "Greater Noida": "🌱"
    }

    for i, row in cities.iterrows():
        with cols[i % 5]:
            st.markdown(f"""
            <div class="city-card">
                <div style="font-size:28px; margin-bottom:8px;">
                    {city_icons.get(row['city'], '🏙️')}
                </div>
                <div style="font-size:15px; font-weight:700;
                            color:#fff; margin-bottom:12px;">
                    {row['city']}
                </div>
                <div style="font-size:11px; color:#475569;
                            margin-bottom:4px;">
                    {int(row['areas'])} areas
                </div>
                <div style="background:linear-gradient(135deg,#0ea5e9,#7c3aed);
                            border-radius:8px; padding:6px;
                            font-size:16px; font-weight:800;
                            color:white; margin-bottom:12px;">
                    {row['avg_score']}
                </div>
                <div style="font-size:11px; color:#475569;
                            margin-bottom:4px;">Avg Score</div>
                <div style="display:flex; flex-direction:column;
                            gap:4px; margin-top:8px;">
                    <div style="display:flex; justify-content:space-between;">
                        <span style="font-size:11px; color:#475569;">
                            💰 Rent
                        </span>
                        <span style="font-size:11px; color:#e2e8f0;
                                     font-weight:600;">
                            ₹{int(row['avg_rent']):,}
                        </span>
                    </div>
                    <div style="display:flex; justify-content:space-between;">
                        <span style="font-size:11px; color:#475569;">
                            📈 Growth
                        </span>
                        <span style="font-size:11px; color:#22c55e;
                                     font-weight:600;">
                            {row['avg_growth']}%
                        </span>
                    </div>
                    <div style="display:flex; justify-content:space-between;">
                        <span style="font-size:11px; color:#475569;">
                            ⚔️ Comp
                        </span>
                        <span style="font-size:11px; color:#f59e0b;
                                     font-weight:600;">
                            {row['avg_competition']}/10
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts Row ─────────────────────────────────────────────
    st.markdown("""
    <div class="section-title">📊 Quick Insights</div>
    <div class="section-sub">
        Visual overview of NCR business landscape
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
            title="Top 10 Areas by Opportunity Score"
        )
        fig.update_layout(
            plot_bgcolor="#0a0f1e",
            paper_bgcolor="#0a0f1e",
            font_color="#e2e8f0",
            showlegend=False,
            height=380,
            margin=dict(l=10, r=10, t=40, b=10),
            coloraxis_showscale=False,
            xaxis=dict(gridcolor="#1e293b", title="Score"),
            yaxis=dict(gridcolor="#1e293b", title=""),
            title_font=dict(size=14, color="#94a3b8")
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.scatter(
            df,
            x="avg_rent",
            y="opportunity_score",
            color="city",
            size="population_density",
            hover_name="area",
            template="plotly_dark",
            title="Rent vs Opportunity Score",
            labels={
                "avg_rent": "Avg Rent (₹)",
                "opportunity_score": "Opportunity Score"
            }
        )
        fig2.update_layout(
            plot_bgcolor="#0a0f1e",
            paper_bgcolor="#0a0f1e",
            font_color="#e2e8f0",
            height=380,
            margin=dict(l=10, r=10, t=40, b=10),
            xaxis=dict(gridcolor="#1e293b"),
            yaxis=dict(gridcolor="#1e293b"),
            legend=dict(
                bgcolor="#0a0f1e",
                bordercolor="#1e293b"
            ),
            title_font=dict(size=14, color="#94a3b8")
        )
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        fig3 = px.box(
            df,
            x="city",
            y="avg_rent",
            color="city",
            template="plotly_dark",
            title="Rent Distribution by City",
            labels={"avg_rent": "Avg Rent (₹)", "city": ""}
        )
        fig3.update_layout(
            plot_bgcolor="#0a0f1e",
            paper_bgcolor="#0a0f1e",
            font_color="#e2e8f0",
            showlegend=False,
            height=320,
            margin=dict(l=10, r=10, t=40, b=10),
            xaxis=dict(gridcolor="#1e293b"),
            yaxis=dict(gridcolor="#1e293b"),
            title_font=dict(size=14, color="#94a3b8")
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        fig4 = px.bar(
            df.nlargest(10, "growth_rate"),
            x="area",
            y="growth_rate",
            color="growth_rate",
            color_continuous_scale=["#1e293b", "#22c55e"],
            template="plotly_dark",
            title="Top 10 Fastest Growing Areas",
            labels={"growth_rate": "Growth %", "area": ""}
        )
        fig4.update_layout(
            plot_bgcolor="#0a0f1e",
            paper_bgcolor="#0a0f1e",
            font_color="#e2e8f0",
            showlegend=False,
            height=320,
            margin=dict(l=10, r=10, t=40, b=10),
            coloraxis_showscale=False,
            xaxis=dict(gridcolor="#1e293b",
                       tickangle=45),
            yaxis=dict(gridcolor="#1e293b"),
            title_font=dict(size=14, color="#94a3b8")
        )
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Market Insights ────────────────────────────────────────
    st.markdown("""
    <div class="section-title">💡 Market Insights</div>
    <div class="section-sub">
        Key findings from the NCR business landscape
    </div>
    """, unsafe_allow_html=True)

    best_growth = df.loc[df["growth_rate"].idxmax()]
    best_income = df.loc[df["avg_income"].idxmax()]
    lowest_rent = df.loc[df["avg_rent"].idxmin()]
    best_metro  = df.loc[df["metro_distance_km"].idxmin()]
    most_hosp   = df.loc[df["hospitals_nearby"].idxmax()]
    least_comp  = df.loc[df["competition_score"].idxmin()]

    insights = [
        ("📈", "Fastest Growing",
         best_growth["area"],
         f"{best_growth['growth_rate']}% annual growth",
         "#22c55e"),
        ("💰", "Highest Income",
         best_income["area"],
         f"₹{int(best_income['avg_income']):,} avg income",
         "#0ea5e9"),
        ("💸", "Most Affordable",
         lowest_rent["area"],
         f"₹{int(lowest_rent['avg_rent']):,}/mo rent",
         "#a78bfa"),
        ("🚇", "Best Metro Access",
         best_metro["area"],
         f"{best_metro['metro_distance_km']} km to metro",
         "#f59e0b"),
        ("🏥", "Best Healthcare",
         most_hosp["area"],
         f"{int(most_hosp['hospitals_nearby'])} hospitals nearby",
         "#ec4899"),
        ("⚔️", "Least Competition",
         least_comp["area"],
         f"Score: {least_comp['competition_score']}/10",
         "#34d399"),
    ]

    cols = st.columns(3)
    for i, (icon, title, area, detail, color) in enumerate(insights):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="insight-card" style="margin-bottom:12px;">
                <div style="display:flex; align-items:center;
                            gap:12px; margin-bottom:8px;">
                    <div style="
                        width:40px; height:40px;
                        background:{color}22;
                        border:1px solid {color}44;
                        border-radius:10px;
                        display:flex; align-items:center;
                        justify-content:center;
                        font-size:18px;
                    ">{icon}</div>
                    <div>
                        <div style="font-size:11px; color:#475569;
                                    font-weight:600;
                                    text-transform:uppercase;
                                    letter-spacing:1px;">
                            {title}
                        </div>
                        <div style="font-size:16px; font-weight:700;
                                    color:#fff;">{area}</div>
                    </div>
                </div>
                <div style="font-size:13px; color:{color};
                            font-weight:600; padding-left:52px;">
                    {detail}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Business Types ─────────────────────────────────────────
    st.markdown("""
    <div class="section-title">🏢 Supported Business Types</div>
    <div class="section-sub">
        Each type has unique AI-powered scoring weights
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
            <div class="biz-card">
                <div style="font-size:26px;">{icon}</div>
                <div style="font-size:12px; color:#e2e8f0;
                            font-weight:600; margin-top:8px;">
                    {name}
                </div>
                <div style="font-size:10px; color:#475569;
                            margin-top:4px; line-height:1.4;">
                    {desc}
                </div>
            </div>
            """, unsafe_allow_html=True)