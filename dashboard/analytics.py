# dashboard/analytics.py
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from engine.recommender import get_recommendations
from engine.business_profiles import get_display_names

def load_data():
    conn = sqlite3.connect("database/urbaniq.db")
    df = pd.read_sql("SELECT * FROM locations_processed", conn)
    conn.close()
    return df

def show_analytics():
    st.markdown("## 📊 Analytics Dashboard")
    st.caption("Deep dive into NCR location data across all metrics")

    df = load_data()

    # ── City Filter ────────────────────────────────────────────
    city = st.selectbox(
        "Filter by City",
        ["All", "Noida", "Delhi", "Gurgaon", "Ghaziabad", "Greater Noida"]
    )

    if city != "All":
        df = df[df["city"] == city]

    st.divider()

    # ── KPI Row ────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Areas",    len(df))
    col2.metric("Avg Rent",       f"₹{int(df['avg_rent'].mean()):,}")
    col3.metric("Avg Income",     f"₹{int(df['avg_income'].mean()):,}")
    col4.metric("Avg Growth",     f"{df['growth_rate'].mean():.1f}%")

    st.divider()

    # ── Row 1: Opportunity Score + Rent ───────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🏆 Opportunity Score by Area")
        fig = px.bar(
            df.sort_values("opportunity_score", ascending=True).tail(15),
            x="opportunity_score",
            y="area",
            orientation="h",
            color="opportunity_score",
            color_continuous_scale="Blues",
            template="plotly_dark",
            labels={"opportunity_score": "Score", "area": "Area"}
        )
        fig.update_layout(
            plot_bgcolor="#1e1e2e",
            paper_bgcolor="#1e1e2e",
            font_color="#e2e8f0",
            showlegend=False,
            height=400,
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🏠 Average Rent by City")
        rent_by_city = df.groupby("city")["avg_rent"].mean().reset_index()
        fig = px.bar(
            rent_by_city,
            x="city",
            y="avg_rent",
            color="avg_rent",
            color_continuous_scale="Reds",
            template="plotly_dark",
            labels={"avg_rent": "Avg Rent (₹)", "city": "City"}
        )
        fig.update_layout(
            plot_bgcolor="#1e1e2e",
            paper_bgcolor="#1e1e2e",
            font_color="#e2e8f0",
            showlegend=False,
            height=400,
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Row 2: Growth + Competition ───────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📈 Growth Rate by Area")
        fig = px.bar(
            df.sort_values("growth_rate", ascending=True).tail(15),
            x="growth_rate",
            y="area",
            orientation="h",
            color="growth_rate",
            color_continuous_scale="Greens",
            template="plotly_dark",
            labels={"growth_rate": "Growth %", "area": "Area"}
        )
        fig.update_layout(
            plot_bgcolor="#1e1e2e",
            paper_bgcolor="#1e1e2e",
            font_color="#e2e8f0",
            showlegend=False,
            height=400,
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### ⚔️ Competition Score by Area")
        fig = px.bar(
            df.sort_values("competition_score", ascending=True).tail(15),
            x="competition_score",
            y="area",
            orientation="h",
            color="competition_score",
            color_continuous_scale="Oranges",
            template="plotly_dark",
            labels={"competition_score": "Competition", "area": "Area"}
        )
        fig.update_layout(
            plot_bgcolor="#1e1e2e",
            paper_bgcolor="#1e1e2e",
            font_color="#e2e8f0",
            showlegend=False,
            height=400,
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Row 3: Scatter + Radar ────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💡 Rent vs Opportunity Score")
        fig = px.scatter(
            df,
            x="avg_rent",
            y="opportunity_score",
            color="city",
            size="population_density",
            hover_name="area",
            template="plotly_dark",
            labels={
                "avg_rent": "Avg Rent (₹)",
                "opportunity_score": "Opportunity Score"
            }
        )
        fig.update_layout(
            plot_bgcolor="#1e1e2e",
            paper_bgcolor="#1e1e2e",
            font_color="#e2e8f0",
            height=400,
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🕸️ Area Profile Radar")
        area_select = st.selectbox(
            "Select Area for Radar",
            df["area"].tolist()
        )
        row = df[df["area"] == area_select].iloc[0]

        categories = [
            "Population", "Income", "Metro Access",
            "Office Density", "Growth", "Sentiment"
        ]
        values = [
            row["pop_norm"]      * 100,
            row["income_norm"]   * 100,
            row["metro_norm"]    * 100,
            row["office_norm"]   * 100,
            row["growth_norm"]   * 100,
            row["sentiment_norm"]* 100,
        ]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            fillcolor="rgba(37, 99, 235, 0.3)",
            line=dict(color="#2563eb", width=2),
            name=area_select
        ))
        fig.update_layout(
            polar=dict(
                bgcolor="#1e1e2e",
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor="#2d2d44",
                    tickfont=dict(color="#94a3b8")
                ),
                angularaxis=dict(
                    gridcolor="#2d2d44",
                    tickfont=dict(color="#e2e8f0")
                )
            ),
            paper_bgcolor="#1e1e2e",
            font_color="#e2e8f0",
            showlegend=False,
            height=400,
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Row 4: Income Distribution ────────────────────────────
    st.markdown("### 💰 Income Distribution Across Areas")
    fig = px.box(
        df,
        x="city",
        y="avg_income",
        color="city",
        template="plotly_dark",
        labels={"avg_income": "Avg Income (₹)", "city": "City"}
    )
    fig.update_layout(
        plot_bgcolor="#1e1e2e",
        paper_bgcolor="#1e1e2e",
        font_color="#e2e8f0",
        showlegend=False,
        height=350,
        margin=dict(l=10, r=10, t=30, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)