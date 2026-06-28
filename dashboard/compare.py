# dashboard/compare.py
import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
import plotly.express as px

def load_data():
    conn = sqlite3.connect("database/urbaniq.db")
    df = pd.read_sql("SELECT * FROM locations_processed", conn)
    conn.close()
    return df

def show_compare():
    st.markdown("""
    <style>
    .stApp { background-color: #050816 !important; }
    .compare-header {
        background: linear-gradient(135deg, #0a0f1e, #0d1a2e);
        border: 1px solid #1e293b;
        border-radius: 20px;
        padding: 32px 40px;
        margin-bottom: 32px;
    }
    .vs-badge {
        background: linear-gradient(135deg, #0ea5e9, #7c3aed);
        border-radius: 50%;
        width: 48px; height: 48px;
        display: flex; align-items: center;
        justify-content: center;
        font-size: 16px; font-weight: 900;
        color: white; margin: 0 auto;
        box-shadow: 0 8px 32px rgba(124,58,237,0.4);
    }
    .winner-card {
        background: linear-gradient(135deg, #0a0f1e, #0d1a2e);
        border: 2px solid #0ea5e9;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 32px rgba(14,165,233,0.15);
    }
    .metric-row {
        background: #0a0f1e;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .metric-label {
        font-size: 13px;
        color: #475569;
        font-weight: 500;
    }
    .metric-val-left {
        font-size: 15px;
        font-weight: 700;
        color: #0ea5e9;
        text-align: right;
        min-width: 100px;
    }
    .metric-val-right {
        font-size: 15px;
        font-weight: 700;
        color: #7c3aed;
        text-align: left;
        min-width: 100px;
    }
    .metric-winner {
        font-size: 11px;
        color: #22c55e;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

    df = load_data()

    # ── Header ─────────────────────────────────────────────────
    st.markdown("""
    <div class="compare-header">
        <h2 style="font-size:28px; font-weight:800;
                   color:#fff; margin:0 0 8px 0;">
            ⚖️ Area Comparison
        </h2>
        <p style="font-size:14px; color:#475569; margin:0;">
            Compare two NCR areas side by side across
            all metrics to make the best decision
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Area Selection ─────────────────────────────────────────
    areas = df["area"].tolist()

    col1, col2, col3 = st.columns([2, 1, 2])

    with col1:
        area1 = st.selectbox(
            "📍 First Area",
            areas,
            index=0,
            key="compare_area1"
        )

    with col2:
        st.markdown("""
        <div style="display:flex; align-items:center;
                    justify-content:center; height:100%;
                    padding-top:28px;">
            <div class="vs-badge">VS</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        area2 = st.selectbox(
            "📍 Second Area",
            areas,
            index=1,
            key="compare_area2"
        )

    if area1 == area2:
        st.warning("Please select two different areas to compare!")
        return

    st.divider()

    # ── Get Data ───────────────────────────────────────────────
    r1 = df[df["area"] == area1].iloc[0]
    r2 = df[df["area"] == area2].iloc[0]

    # ── Score Cards ────────────────────────────────────────────
    col1, col2, col3 = st.columns([2, 1, 2])

    winner = area1 if r1["opportunity_score"] > r2["opportunity_score"] \
             else area2

    with col1:
        border = "2px solid #0ea5e9" if winner == area1 \
                 else "1px solid #1e293b"
        st.markdown(f"""
        <div style="background:#0a0f1e; border:{border};
                    border-radius:16px; padding:24px;
                    text-align:center;">
            <div style="font-size:24px; font-weight:800;
                        color:#fff; margin-bottom:4px;">
                {area1}
            </div>
            <div style="font-size:13px; color:#475569;
                        margin-bottom:16px;">{r1['city']}</div>
            <div style="font-size:48px; font-weight:900;
                        background:linear-gradient(135deg,#0ea5e9,#7c3aed);
                        -webkit-background-clip:text;
                        -webkit-text-fill-color:transparent;">
                {r1['opportunity_score']}
            </div>
            <div style="font-size:12px; color:#475569;">
                OPPORTUNITY SCORE
            </div>
            {"<div style='margin-top:12px; color:#22c55e; font-weight:700; font-size:14px;'>🏆 Winner</div>" if winner == area1 else ""}
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="display:flex; align-items:center;
                    justify-content:center; height:100%;">
            <div style="text-align:center;">
                <div style="font-size:11px; color:#475569;
                            letter-spacing:2px;">SCORE</div>
                <div style="font-size:11px; color:#475569;
                            letter-spacing:2px;">DIFF</div>
                <div style="font-size:24px; font-weight:800;
                            color:#f59e0b; margin-top:8px;">
        """ + f"{abs(r1['opportunity_score'] - r2['opportunity_score']):.1f}" + """
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        border = "2px solid #7c3aed" if winner == area2 \
                 else "1px solid #1e293b"
        st.markdown(f"""
        <div style="background:#0a0f1e; border:{border};
                    border-radius:16px; padding:24px;
                    text-align:center;">
            <div style="font-size:24px; font-weight:800;
                        color:#fff; margin-bottom:4px;">
                {area2}
            </div>
            <div style="font-size:13px; color:#475569;
                        margin-bottom:16px;">{r2['city']}</div>
            <div style="font-size:48px; font-weight:900;
                        background:linear-gradient(135deg,#7c3aed,#0ea5e9);
                        -webkit-background-clip:text;
                        -webkit-text-fill-color:transparent;">
                {r2['opportunity_score']}
            </div>
            <div style="font-size:12px; color:#475569;">
                OPPORTUNITY SCORE
            </div>
            {"<div style='margin-top:12px; color:#22c55e; font-weight:700; font-size:14px;'>🏆 Winner</div>" if winner == area2 else ""}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Metrics Comparison ─────────────────────────────────────
    st.markdown("""
    <div style="font-size:20px; font-weight:800; color:#fff;
                margin-bottom:16px;">📊 Detailed Metrics</div>
    """, unsafe_allow_html=True)

    metrics = [
        ("🏠 Avg Rent",        "avg_rent",          "₹{:,}/mo", False),
        ("🚇 Metro Distance",   "metro_distance_km", "{} km",    False),
        ("⚔️ Competition",      "competition_score", "{}/10",    False),
        ("📈 Growth Rate",      "growth_rate",       "{}%",      True),
        ("💰 Avg Income",       "avg_income",        "₹{:,}",   True),
        ("👥 Population",       "population_density","{}",       True),
        ("🏥 Hospitals",        "hospitals_nearby",  "{}",       True),
        ("🏫 Schools",          "schools_nearby",    "{}",       True),
        ("🏢 Office Density",   "office_density",    "{}/10",    True),
        ("😊 Sentiment",        "sentiment_score",   "{}/10",    True),
        ("🚗 Parking",          "parking_score",     "{}/10",    True),
        ("👣 Footfall",         "footfall_score",    "{}/10",    True),
    ]

    for label, col, fmt, higher_better in metrics:
        v1 = r1[col]
        v2 = r2[col]

        if higher_better:
            w1 = "🟢" if v1 > v2 else ("🔴" if v1 < v2 else "🟡")
            w2 = "🟢" if v2 > v1 else ("🔴" if v2 < v1 else "🟡")
        else:
            w1 = "🟢" if v1 < v2 else ("🔴" if v1 > v2 else "🟡")
            w2 = "🟢" if v2 < v1 else ("🔴" if v2 > v1 else "🟡")

        try:
            val1 = fmt.format(int(v1)) if isinstance(v1, float) \
                   and v1 == int(v1) else fmt.format(v1)
            val2 = fmt.format(int(v2)) if isinstance(v2, float) \
                   and v2 == int(v2) else fmt.format(v2)
        except:
            val1 = str(v1)
            val2 = str(v2)

        st.markdown(f"""
        <div class="metric-row">
            <div style="min-width:120px; text-align:right;">
                <span style="font-size:15px; font-weight:700;
                             color:#0ea5e9;">{val1}</span>
                <span style="margin-left:8px;">{w1}</span>
            </div>
            <div style="flex:1; text-align:center;">
                <div class="metric-label">{label}</div>
            </div>
            <div style="min-width:120px; text-align:left;">
                <span style="margin-right:8px;">{w2}</span>
                <span style="font-size:15px; font-weight:700;
                             color:#7c3aed;">{val2}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Radar Chart ────────────────────────────────────────────
    st.markdown("""
    <div style="font-size:20px; font-weight:800; color:#fff;
                margin-bottom:16px;">🕸️ Profile Radar</div>
    """, unsafe_allow_html=True)

    categories = [
        "Population", "Income", "Metro Access",
        "Office Density", "Growth", "Sentiment",
        "Footfall", "Parking"
    ]

    vals1 = [
        r1["pop_norm"] * 100,
        r1["income_norm"] * 100,
        r1["metro_norm"] * 100,
        r1["office_norm"] * 100,
        r1["growth_norm"] * 100,
        r1["sentiment_norm"] * 100,
        r1["footfall_norm"] * 100,
        r1["parking_norm"] * 100,
    ]

    vals2 = [
        r2["pop_norm"] * 100,
        r2["income_norm"] * 100,
        r2["metro_norm"] * 100,
        r2["office_norm"] * 100,
        r2["growth_norm"] * 100,
        r2["sentiment_norm"] * 100,
        r2["footfall_norm"] * 100,
        r2["parking_norm"] * 100,
    ]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=vals1 + [vals1[0]],
        theta=categories + [categories[0]],
        fill="toself",
        fillcolor="rgba(14,165,233,0.15)",
        line=dict(color="#0ea5e9", width=2),
        name=area1
    ))

    fig.add_trace(go.Scatterpolar(
        r=vals2 + [vals2[0]],
        theta=categories + [categories[0]],
        fill="toself",
        fillcolor="rgba(124,58,237,0.15)",
        line=dict(color="#7c3aed", width=2),
        name=area2
    ))

    fig.update_layout(
        polar=dict(
            bgcolor="#0a0f1e",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
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
        legend=dict(
            bgcolor="#0a0f1e",
            bordercolor="#1e293b",
            borderwidth=1
        ),
        height=500,
        margin=dict(l=40, r=40, t=40, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)

    # ── Bar Comparison ─────────────────────────────────────────
    st.markdown("""
    <div style="font-size:20px; font-weight:800; color:#fff;
                margin-bottom:16px;">📊 Score Breakdown</div>
    """, unsafe_allow_html=True)

    breakdown_metrics = [
        "Population", "Income", "Metro",
        "Office", "Growth", "Sentiment",
        "Footfall", "Parking"
    ]
    breakdown_vals1 = [round(v, 1) for v in vals1]
    breakdown_vals2 = [round(v, 1) for v in vals2]

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        name=area1,
        x=breakdown_metrics,
        y=breakdown_vals1,
        marker_color="#0ea5e9",
        opacity=0.85
    ))
    fig2.add_trace(go.Bar(
        name=area2,
        x=breakdown_metrics,
        y=breakdown_vals2,
        marker_color="#7c3aed",
        opacity=0.85
    ))

    fig2.update_layout(
        barmode="group",
        plot_bgcolor="#0a0f1e",
        paper_bgcolor="#050816",
        font_color="#e2e8f0",
        legend=dict(
            bgcolor="#0a0f1e",
            bordercolor="#1e293b",
            borderwidth=1
        ),
        height=380,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(gridcolor="#1e293b"),
        yaxis=dict(gridcolor="#1e293b", range=[0, 100]),
    )

    st.plotly_chart(fig2, use_container_width=True)

    # ── Summary ────────────────────────────────────────────────
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0a0f1e,#0d1a2e);
                border:1px solid #1e293b; border-radius:16px;
                padding:28px; margin-top:8px;">
        <div style="font-size:18px; font-weight:700;
                    color:#fff; margin-bottom:16px;">
            🏆 Verdict
        </div>
        <div style="font-size:15px; color:#94a3b8; line-height:1.8;">
            Based on overall opportunity score,
            <span style="color:#22c55e; font-weight:700;">{winner}</span>
            is the better location with a score of
            <span style="color:#0ea5e9; font-weight:700;">
                {r1['opportunity_score'] if winner == area1
                 else r2['opportunity_score']}
            </span>
            vs
            <span style="color:#7c3aed; font-weight:700;">
                {r2['opportunity_score'] if winner == area1
                 else r1['opportunity_score']}
            </span>.
            The difference of
            <span style="color:#f59e0b; font-weight:700;">
                {abs(r1['opportunity_score'] -
                     r2['opportunity_score']):.1f} points
            </span>
            suggests
            {"a clear winner." if abs(r1['opportunity_score'] -
             r2['opportunity_score']) > 5
             else "both areas are competitive choices."}
        </div>
    </div>
    """, unsafe_allow_html=True)