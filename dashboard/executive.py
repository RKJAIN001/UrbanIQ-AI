# dashboard/executive.py
import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
from engine.recommender import get_recommendations
from engine.business_profiles import BUSINESS_PROFILES

def load_data():
    conn = sqlite3.connect("database/urbaniq.db")
    df = pd.read_sql("SELECT * FROM locations_processed", conn)
    conn.close()
    return df

def estimate_revenue(area_row, business_type):
    """Estimate annual revenue potential based on area metrics"""
    base_revenues = {
        "cafe":           15000000,
        "restaurant":     25000000,
        "gym":            12000000,
        "pharmacy":       20000000,
        "grocery_store":  35000000,
        "coworking":      18000000,
        "clothing_store": 22000000,
        "bookstore":       8000000,
    }

    base = base_revenues.get(business_type, 15000000)

    # Multipliers based on area metrics
    pop_mult      = 0.8 + (area_row["pop_norm"] * 0.4)
    income_mult   = 0.8 + (area_row["income_norm"] * 0.4)
    footfall_mult = 0.8 + (area_row["footfall_norm"] * 0.4)
    comp_mult     = 1.2 - (area_row["competition_score"] / 10 * 0.3)

    revenue = base * pop_mult * income_mult * footfall_mult * comp_mult
    return round(revenue / 10000000, 1)  # Convert to Cr

def get_competition_level(score):
    if score <= 4:
        return "🟢 Low", "#22c55e"
    elif score <= 7:
        return "🟡 Medium", "#f59e0b"
    else:
        return "🔴 High", "#ef4444"

def get_demand_level(pop_norm, income_norm, footfall_norm):
    avg = (pop_norm + income_norm + footfall_norm) / 3
    if avg >= 0.7:
        return "🔥 Very High", "#0ea5e9"
    elif avg >= 0.5:
        return "📈 High", "#22c55e"
    elif avg >= 0.3:
        return "📊 Medium", "#f59e0b"
    else:
        return "📉 Low", "#ef4444"

def get_best_businesses(area_row):
    """Find top 3 business types for this area"""
    scores = {}
    for btype, profile in BUSINESS_PROFILES.items():
        score = 0
        for col, weight in profile["weights"].items():
            if col in area_row:
                score += area_row[col] * weight
        scores[btype] = score

    top3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
    return [(BUSINESS_PROFILES[b]["display_name"], s * 100) for b, s in top3]

def show_executive():
    df = load_data()

    st.markdown("""
    <style>
    .stApp { background-color: #050816 !important; }
    .exec-header {
        background: linear-gradient(135deg, #0a0f1e, #0d1a2e);
        border: 1px solid #1e293b;
        border-radius: 20px;
        padding: 32px 40px;
        margin-bottom: 24px;
    }
    .exec-card {
        background: #0a0f1e;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 24px;
        height: 100%;
        transition: all 0.3s;
    }
    .exec-card:hover {
        border-color: rgba(14,165,233,0.3);
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(14,165,233,0.08);
    }
    .score-ring {
        width: 120px; height: 120px;
        border-radius: 50%;
        display: flex; align-items: center;
        justify-content: center;
        margin: 0 auto 16px auto;
        font-size: 32px; font-weight: 900;
        color: white;
    }
    .kpi-row {
        display: flex; align-items: center;
        gap: 12px; padding: 12px;
        background: #050816;
        border-radius: 10px;
        margin-bottom: 8px;
        border: 1px solid #1e293b;
    }
    .kpi-icon { font-size: 20px; width: 32px; }
    .kpi-label { font-size: 12px; color: #475569; }
    .kpi-value { font-size: 15px; font-weight: 700; color: #e2e8f0; }
    .biz-tag {
        display: inline-block;
        background: rgba(14,165,233,0.1);
        border: 1px solid rgba(14,165,233,0.2);
        border-radius: 8px;
        padding: 6px 12px;
        font-size: 13px;
        color: #0ea5e9;
        margin: 4px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Header ─────────────────────────────────────────────────
    st.markdown("""
    <div class="exec-header">
        <div style="display:flex; justify-content:space-between;
                    align-items:center;">
            <div>
                <div style="font-size:28px; font-weight:800;
                            color:#fff; margin-bottom:6px;">
                    📋 Executive Summary
                </div>
                <div style="font-size:14px; color:#475569;">
                     Business intelligence report
                    for NCR location decisions
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:11px; color:#475569;">
                    Report Type
                </div>
                <div style="font-size:14px; color:#0ea5e9;
                            font-weight:700;">
                    Business Intelligence · Live Data
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Filters ────────────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        area_name = st.selectbox(
            "📍 Select Area",
            df["area"].tolist(),
            index=0
        )

    with col2:
        display_names = {k: v["display_name"]
                        for k, v in BUSINESS_PROFILES.items()}
        biz_label = st.selectbox(
            "🏢 Business Type",
            list(display_names.values())
        )
        business_type = [k for k, v in display_names.items()
                        if v == biz_label][0]

    st.divider()

    # ── Get Area Data ──────────────────────────────────────────
    row = df[df["area"] == area_name].iloc[0]

    # Calculate metrics
    revenue       = estimate_revenue(row, business_type)
    comp_text, comp_color = get_competition_level(row["competition_score"])
    demand_text, demand_color = get_demand_level(
        row["pop_norm"], row["income_norm"], row["footfall_norm"]
    )
    best_biz      = get_best_businesses(row)
    overall_score = min(99, round(row["opportunity_score"] * 1.5))

    # ── Executive Summary Card ─────────────────────────────────
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #0a0f1e, #0d1a2e);
        border: 2px solid #0ea5e9;
        border-radius: 20px;
        padding: 32px;
        margin-bottom: 24px;
        box-shadow: 0 0 40px rgba(14,165,233,0.1);
    ">
        <div style="display:flex; justify-content:space-between;
                    align-items:flex-start; flex-wrap:wrap; gap:24px;">

            <!-- Left: Area Info -->
            <div style="flex:1; min-width:280px;">
                <div style="font-size:12px; color:#475569;
                            letter-spacing:2px; margin-bottom:8px;">
                    EXECUTIVE REPORT · {row['city'].upper()}
                </div>
                <div style="font-size:32px; font-weight:900;
                            color:#fff; margin-bottom:4px;">
                    📍 {area_name}
                </div>
                <div style="font-size:14px; color:#475569;
                            margin-bottom:24px;">
                    {biz_label} Location Analysis
                </div>

                <div class="kpi-row">
                    <div class="kpi-icon">💰</div>
                    <div style="flex:1;">
                        <div class="kpi-label">Revenue Potential</div>
                        <div class="kpi-value">
                            ₹{revenue} Cr/year
                        </div>
                    </div>
                </div>

                <div class="kpi-row">
                    <div class="kpi-icon">⚔️</div>
                    <div style="flex:1;">
                        <div class="kpi-label">Competition Level</div>
                        <div style="font-size:15px; font-weight:700;
                                    color:{comp_color};">
                            {comp_text}
                        </div>
                    </div>
                </div>

                <div class="kpi-row">
                    <div class="kpi-icon">👥</div>
                    <div style="flex:1;">
                        <div class="kpi-label">Customer Demand</div>
                        <div style="font-size:15px; font-weight:700;
                                    color:{demand_color};">
                            {demand_text}
                        </div>
                    </div>
                </div>

                <div class="kpi-row">
                    <div class="kpi-icon">🚇</div>
                    <div style="flex:1;">
                        <div class="kpi-label">Metro Connectivity</div>
                        <div class="kpi-value">
                            {row['metro_distance_km']} km away
                        </div>
                    </div>
                </div>

                <div class="kpi-row">
                    <div class="kpi-icon">🏠</div>
                    <div style="flex:1;">
                        <div class="kpi-label">Commercial Rent</div>
                        <div class="kpi-value">
                            ₹{int(row['avg_rent']):,}/month
                        </div>
                    </div>
                </div>

                <div class="kpi-row">
                    <div class="kpi-icon">📈</div>
                    <div style="flex:1;">
                        <div class="kpi-label">Area Growth Rate</div>
                        <div style="font-size:15px; font-weight:700;
                                    color:#22c55e;">
                            {row['growth_rate']}% per year
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right: Score + Best Business -->
            <div style="text-align:center; min-width:220px;">
                <div style="font-size:12px; color:#475569;
                            letter-spacing:2px; margin-bottom:16px;">
                    OVERALL BUSINESS SCORE
                </div>
                <div style="
                    width:140px; height:140px;
                    border-radius:50%;
                    background: conic-gradient(
                        #0ea5e9 {overall_score * 3.6}deg,
                        #1e293b 0deg
                    );
                    display:flex; align-items:center;
                    justify-content:center;
                    margin:0 auto 8px auto;
                    box-shadow: 0 0 32px rgba(14,165,233,0.3);
                ">
                    <div style="
                        width:110px; height:110px;
                        background:#0a0f1e;
                        border-radius:50%;
                        display:flex; align-items:center;
                        justify-content:center;
                        flex-direction:column;
                    ">
                        <div style="font-size:36px; font-weight:900;
                                    color:#0ea5e9;">{overall_score}</div>
                        <div style="font-size:11px; color:#475569;">
                            / 100
                        </div>
                    </div>
                </div>

                <div style="font-size:13px; color:#475569;
                            margin-bottom:24px;">
                    {"🏆 Excellent Choice" if overall_score >= 80
                     else "✅ Good Choice" if overall_score >= 60
                     else "⚠️ Consider Alternatives"}
                </div>

                <div style="font-size:12px; color:#475569;
                            letter-spacing:2px; margin-bottom:12px;">
                    BEST BUSINESSES FOR THIS AREA
                </div>
                {"".join([f'<div class="biz-tag">✓ {name}</div>'
                          for name, _ in best_biz])}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Detailed Metrics ───────────────────────────────────────
    st.markdown("""
    <div style="font-size:20px; font-weight:800; color:#fff;
                margin-bottom:16px;">📊 Detailed Analysis</div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    # Market Size
    with col1:
        st.markdown(f"""
        <div class="exec-card">
            <div style="font-size:13px; color:#0ea5e9;
                        font-weight:700; letter-spacing:1px;
                        margin-bottom:16px;">📦 MARKET SIZE</div>
            <div style="font-size:28px; font-weight:800;
                        color:#fff; margin-bottom:4px;">
                ₹{revenue} Cr
            </div>
            <div style="font-size:12px; color:#475569;
                        margin-bottom:20px;">Annual Revenue Potential</div>
            <div style="height:1px; background:#1e293b;
                        margin-bottom:16px;"></div>
            <div style="display:flex; justify-content:space-between;
                        margin-bottom:8px;">
                <span style="font-size:12px; color:#475569;">
                    Population Density
                </span>
                <span style="font-size:12px; color:#e2e8f0;
                             font-weight:600;">
                    {row['population_density']}/km²
                </span>
            </div>
            <div style="display:flex; justify-content:space-between;
                        margin-bottom:8px;">
                <span style="font-size:12px; color:#475569;">
                    Avg Income
                </span>
                <span style="font-size:12px; color:#e2e8f0;
                             font-weight:600;">
                    ₹{int(row['avg_income']):,}
                </span>
            </div>
            <div style="display:flex; justify-content:space-between;
                        margin-bottom:8px;">
                <span style="font-size:12px; color:#475569;">
                    Footfall Score
                </span>
                <span style="font-size:12px; color:#e2e8f0;
                             font-weight:600;">
                    {row['footfall_score']}/10
                </span>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <span style="font-size:12px; color:#475569;">
                    Sentiment Score
                </span>
                <span style="font-size:12px; color:#22c55e;
                             font-weight:600;">
                    {row['sentiment_score']}/10
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Infrastructure
    with col2:
        st.markdown(f"""
        <div class="exec-card">
            <div style="font-size:13px; color:#7c3aed;
                        font-weight:700; letter-spacing:1px;
                        margin-bottom:16px;">🏗️ INFRASTRUCTURE</div>
            <div style="font-size:28px; font-weight:800;
                        color:#fff; margin-bottom:4px;">
                {row['metro_distance_km']} km
            </div>
            <div style="font-size:12px; color:#475569;
                        margin-bottom:20px;">Nearest Metro Station</div>
            <div style="height:1px; background:#1e293b;
                        margin-bottom:16px;"></div>
            <div style="display:flex; justify-content:space-between;
                        margin-bottom:8px;">
                <span style="font-size:12px; color:#475569;">
                    Hospitals Nearby
                </span>
                <span style="font-size:12px; color:#e2e8f0;
                             font-weight:600;">
                    {int(row['hospitals_nearby'])}
                </span>
            </div>
            <div style="display:flex; justify-content:space-between;
                        margin-bottom:8px;">
                <span style="font-size:12px; color:#475569;">
                    Schools Nearby
                </span>
                <span style="font-size:12px; color:#e2e8f0;
                             font-weight:600;">
                    {int(row['schools_nearby'])}
                </span>
            </div>
            <div style="display:flex; justify-content:space-between;
                        margin-bottom:8px;">
                <span style="font-size:12px; color:#475569;">
                    Office Density
                </span>
                <span style="font-size:12px; color:#e2e8f0;
                             font-weight:600;">
                    {row['office_density']}/10
                </span>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <span style="font-size:12px; color:#475569;">
                    Parking Score
                </span>
                <span style="font-size:12px; color:#e2e8f0;
                             font-weight:600;">
                    {row['parking_score']}/10
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Risk Assessment
    with col3:
        risk_score = round(
            (row["competition_score"] * 0.4 +
             (1 - row["growth_norm"]) * 3 * 0.3 +
             (row["avg_rent"] / 150000) * 10 * 0.3), 1
        )
        risk_level = ("🟢 Low Risk" if risk_score <= 4
                     else "🟡 Medium Risk" if risk_score <= 7
                     else "🔴 High Risk")
        risk_color = ("#22c55e" if risk_score <= 4
                     else "#f59e0b" if risk_score <= 7
                     else "#ef4444")

        st.markdown(f"""
        <div class="exec-card">
            <div style="font-size:13px; color:#f59e0b;
                        font-weight:700; letter-spacing:1px;
                        margin-bottom:16px;">⚠️ RISK ASSESSMENT</div>
            <div style="font-size:28px; font-weight:800;
                        color:{risk_color}; margin-bottom:4px;">
                {risk_level}
            </div>
            <div style="font-size:12px; color:#475569;
                        margin-bottom:20px;">
                Overall Risk Score: {risk_score}/10
            </div>
            <div style="height:1px; background:#1e293b;
                        margin-bottom:16px;"></div>
            <div style="display:flex; justify-content:space-between;
                        margin-bottom:8px;">
                <span style="font-size:12px; color:#475569;">
                    Competition Risk
                </span>
                <span style="font-size:12px;
                             color:{'#ef4444' if row['competition_score'] > 7 else '#22c55e'};
                             font-weight:600;">
                    {row['competition_score']}/10
                </span>
            </div>
            <div style="display:flex; justify-content:space-between;
                        margin-bottom:8px;">
                <span style="font-size:12px; color:#475569;">
                    Rent Burden
                </span>
                <span style="font-size:12px;
                             color:{'#ef4444' if row['avg_rent'] > 100000 else '#22c55e'};
                             font-weight:600;">
                    ₹{int(row['avg_rent']):,}/mo
                </span>
            </div>
            <div style="display:flex; justify-content:space-between;
                        margin-bottom:8px;">
                <span style="font-size:12px; color:#475569;">
                    Market Growth
                </span>
                <span style="font-size:12px; color:#22c55e;
                             font-weight:600;">
                    {row['growth_rate']}%/yr
                </span>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <span style="font-size:12px; color:#475569;">
                    Area Sentiment
                </span>
                <span style="font-size:12px; color:#22c55e;
                             font-weight:600;">
                    {row['sentiment_score']}/10
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Radar Chart ────────────────────────────────────────────
    st.markdown("""
    <div style="font-size:20px; font-weight:800; color:#fff;
                margin-bottom:16px;">🕸️ Area Profile</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        categories = [
            "Population", "Income", "Metro",
            "Office", "Growth", "Sentiment",
            "Footfall", "Parking"
        ]
        values = [
            row["pop_norm"] * 100,
            row["income_norm"] * 100,
            row["metro_norm"] * 100,
            row["office_norm"] * 100,
            row["growth_norm"] * 100,
            row["sentiment_norm"] * 100,
            row["footfall_norm"] * 100,
            row["parking_norm"] * 100,
        ]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            fillcolor="rgba(14,165,233,0.15)",
            line=dict(color="#0ea5e9", width=2),
            name=area_name
        ))
        fig.update_layout(
            polar=dict(
                bgcolor="#0a0f1e",
                radialaxis=dict(
                    visible=True, range=[0, 100],
                    gridcolor="#1e293b",
                    tickfont=dict(color="#475569")
                ),
                angularaxis=dict(
                    gridcolor="#1e293b",
                    tickfont=dict(color="#e2e8f0")
                )
            ),
            paper_bgcolor="#050816",
            font_color="#e2e8f0",
            showlegend=False,
            height=380,
            margin=dict(l=40, r=40, t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Top 5 best businesses for this area
        all_scores = []
        for btype, profile in BUSINESS_PROFILES.items():
            score = sum(
                row.get(col, 0) * weight
                for col, weight in profile["weights"].items()
                if col in row.index
            )
            all_scores.append({
                "business": profile["display_name"],
                "score": round(score * 100, 1)
            })

        biz_df = pd.DataFrame(all_scores).sort_values(
            "score", ascending=True
        )

        fig2 = go.Figure(go.Bar(
            x=biz_df["score"],
            y=biz_df["business"],
            orientation="h",
            marker=dict(
                color=biz_df["score"],
                colorscale=[[0, "#1e293b"], [0.5, "#0ea5e9"],
                            [1, "#7c3aed"]],
            )
        ))
        fig2.update_layout(
            plot_bgcolor="#0a0f1e",
            paper_bgcolor="#050816",
            font_color="#e2e8f0",
            showlegend=False,
            height=380,
            margin=dict(l=10, r=10, t=20, b=10),
            xaxis=dict(gridcolor="#1e293b", title="Score"),
            yaxis=dict(gridcolor="#1e293b"),
            title=dict(
                text="Best Business Types for This Area",
                font=dict(size=14, color="#94a3b8")
            )
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Executive Recommendation ───────────────────────────────
    verdict = ("🏆 Highly Recommended" if overall_score >= 80
               else "✅ Recommended" if overall_score >= 60
               else "⚠️ Proceed with Caution")

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #0a0f1e, #0d1a2e);
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 28px;
        margin-top: 8px;
    ">
        <div style="font-size:18px; font-weight:700;
                    color:#fff; margin-bottom:16px;">
            📋 Executive Recommendation
        </div>
        <div style="font-size:15px; color:#94a3b8; line-height:1.8;">
            <strong style="color:{
                '#22c55e' if overall_score >= 80
                else '#f59e0b' if overall_score >= 60
                else '#ef4444'
            };">{verdict}</strong> —
            {area_name} in {row['city']} scores
            <strong style="color:#0ea5e9;">{overall_score}/100</strong>
            for {biz_label}.
            With an estimated revenue potential of
            <strong style="color:#0ea5e9;">₹{revenue} Cr/year</strong>,
            {comp_text.lower()} competition, and
            {row['growth_rate']}% annual growth,
            this area {"presents an excellent opportunity"
                       if overall_score >= 80
                       else "shows good potential"
                       if overall_score >= 60
                       else "may require additional market research"}.
            The {row['metro_distance_km']} km metro proximity and
            {int(row['hospitals_nearby'])} nearby hospitals
            further {"strengthen" if overall_score >= 60
                     else "partially offset"} the business case.
        </div>
    </div>
    """, unsafe_allow_html=True)