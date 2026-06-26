# engine/map_engine.py
# Enhanced Folium map for UrbanIQ AI

import folium
import pandas as pd
from folium.plugins import MarkerCluster, HeatMap
from engine.recommender import load_processed_data, calculate_score
from engine.business_profiles import BUSINESS_PROFILES

def get_marker_color(score):
    if score >= 65:
        return "green"
    elif score >= 50:
        return "orange"
    elif score >= 35:
        return "blue"
    else:
        return "red"

def get_marker_icon(business_type):
    icons = {
        "cafe":           "coffee",
        "restaurant":     "cutlery",
        "gym":            "fire",
        "pharmacy":       "plus-sign",
        "grocery_store":  "shopping-cart",
        "coworking":      "laptop",
        "clothing_store": "tags",
        "bookstore":      "book"
    }
    return icons.get(business_type, "map-marker")

def build_mini_chart(row):
    """Build a mini HTML bar chart for popup"""
    metrics = {
        "Population": row["population_density"] / 100,
        "Income":     row["avg_income"] / 100000,
        "Office":     row["office_density"] / 10,
        "Sentiment":  row["sentiment_score"] / 10,
        "Growth":     row["growth_rate"] / 12,
    }

    bars = ""
    for label, value in metrics.items():
        pct = min(int(value * 100), 100)
        color = "#22c55e" if pct >= 70 else "#f59e0b" if pct >= 40 else "#ef4444"
        bars += f"""
        <div style="margin:3px 0;">
            <div style="display:flex; align-items:center; gap:6px;">
                <span style="font-size:11px; width:65px; color:#ccc;">{label}</span>
                <div style="flex:1; background:#333; border-radius:4px; height:8px;">
                    <div style="width:{pct}%; background:{color};
                                border-radius:4px; height:8px;"></div>
                </div>
                <span style="font-size:10px; color:#aaa; width:28px;">{pct}%</span>
            </div>
        </div>
        """
    return bars

def build_map(business_type="cafe", city_filter="All"):
    # Load and score data
    df = load_processed_data()
    if city_filter and city_filter != "All":
        df = df[df["city"] == city_filter].copy()

    df["business_score"] = calculate_score(df, business_type)
    df = df.sort_values("business_score", ascending=False).reset_index(drop=True)
    df["rank"] = range(1, len(df) + 1)

    business_display = BUSINESS_PROFILES[business_type]["display_name"]

    # Base map - dark theme
    m = folium.Map(
        location=[28.5355, 77.3910],
        zoom_start=11,
        tiles="CartoDB dark_matter"
    )

    # ── Heatmap Layer ──────────────────────────────────────────
    heat_data = [
        [row["latitude"], row["longitude"], row["business_score"] / 100]
        for _, row in df.iterrows()
    ]
    HeatMap(
        heat_data,
        min_opacity=0.3,
        max_zoom=13,
        radius=35,
        blur=25,
        gradient={
            "0.2": "#1a237e",
            "0.4": "#1565c0",
            "0.6": "#f59e0b",
            "0.8": "#ef4444",
            "1.0": "#22c55e"
        }
    ).add_to(m)

    # ── Marker Cluster ─────────────────────────────────────────
    cluster = MarkerCluster(
        options={
            "maxClusterRadius": 60,
            "spiderfyOnMaxZoom": True,
            "showCoverageOnHover": False,
        }
    ).add_to(m)

    for _, row in df.iterrows():
        score = row["business_score"]
        rank  = row["rank"]
        color = get_marker_color(score)
        icon  = get_marker_icon(business_type)

        # Rank labels
        if rank == 1:
            rank_label = "🥇 Best Location"
            border_color = "#FFD700"
        elif rank == 2:
            rank_label = "🥈 2nd Best"
            border_color = "#C0C0C0"
        elif rank == 3:
            rank_label = "🥉 3rd Best"
            border_color = "#CD7F32"
        else:
            rank_label = f"#{rank}"
            border_color = "#444"

        # Animated pulse ring for top 3
        pulse_html = ""
        if rank <= 3:
            pulse_html = f"""
            <style>
            @keyframes pulse_{rank} {{
                0%   {{ transform: scale(1);   opacity: 0.8; }}
                50%  {{ transform: scale(1.6); opacity: 0.2; }}
                100% {{ transform: scale(1);   opacity: 0.8; }}
            }}
            .pulse-ring-{rank} {{
                width: 40px; height: 40px;
                border: 3px solid {border_color};
                border-radius: 50%;
                animation: pulse_{rank} 1.5s infinite;
                position: absolute;
                top: -10px; left: -10px;
                pointer-events: none;
            }}
            </style>
            <div class="pulse-ring-{rank}"></div>
            """

        mini_chart = build_mini_chart(row)

        popup_html = f"""
        <div style="
            font-family: 'Segoe UI', Arial, sans-serif;
            min-width: 250px;
            background: #1e1e2e;
            color: #e2e8f0;
            border-radius: 10px;
            padding: 14px;
            position: relative;
        ">
            {pulse_html}

            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <h3 style="margin:0; color:#fff; font-size:16px;">{row['area']}</h3>
                    <span style="color:#94a3b8; font-size:12px;">{row['city']} · {rank_label}</span>
                </div>
                <div style="
                    background: linear-gradient(135deg, #2563eb, #7c3aed);
                    border-radius: 50%;
                    width: 48px; height: 48px;
                    display: flex; align-items: center;
                    justify-content: center;
                    font-weight: bold; font-size: 13px;
                    color: white;
                ">{score}</div>
            </div>

            <hr style="border-color:#333; margin:10px 0;">

            <div style="font-size:12px; color:#94a3b8; margin-bottom:6px;">
                <b style="color:#e2e8f0;">📊 Area Metrics</b>
            </div>
            {mini_chart}

            <hr style="border-color:#333; margin:10px 0;">

            <table style="width:100%; font-size:12px; color:#cbd5e1;">
                <tr>
                    <td>🏠 Rent</td>
                    <td style="text-align:right; color:#fff;">
                        <b>₹{int(row['avg_rent']):,}/mo</b>
                    </td>
                    <td style="width:10px;"></td>
                    <td>🚇 Metro</td>
                    <td style="text-align:right; color:#fff;">
                        <b>{row['metro_distance_km']} km</b>
                    </td>
                </tr>
                <tr>
                    <td>⚔️ Competition</td>
                    <td style="text-align:right; color:#fff;">
                        <b>{row['competition_score']}/10</b>
                    </td>
                    <td></td>
                    <td>📈 Growth</td>
                    <td style="text-align:right; color:#fff;">
                        <b>{row['growth_rate']}%</b>
                    </td>
                </tr>
                <tr>
                    <td>🏥 Hospitals</td>
                    <td style="text-align:right; color:#fff;">
                        <b>{int(row['hospitals_nearby'])}</b>
                    </td>
                    <td></td>
                    <td>💰 Income</td>
                    <td style="text-align:right; color:#fff;">
                        <b>₹{int(row['avg_income']):,}</b>
                    </td>
                </tr>
            </table>

            <div style="
                margin-top:10px;
                background:#2d2d44;
                border-radius:6px;
                padding:6px 10px;
                font-size:11px;
                color:#94a3b8;
                text-align:center;
            ">
                {business_display} · Opportunity Score: <b style="color:#22c55e;">{score}</b>
            </div>
        </div>
        """

        # Use custom DivIcon for top 3 (animated), regular Icon for rest
        if rank <= 3:
            marker_icon = folium.DivIcon(
                html=f"""
                <div style="position:relative;">
                    <div style="
                        background: linear-gradient(135deg, #2563eb, #7c3aed);
                        color: white;
                        border: 3px solid {border_color};
                        border-radius: 50%;
                        width: 36px; height: 36px;
                        display: flex; align-items: center;
                        justify-content: center;
                        font-weight: bold; font-size: 13px;
                        box-shadow: 0 0 12px {border_color};
                    ">{rank}</div>
                </div>
                """,
                icon_size=(36, 36),
                icon_anchor=(18, 18)
            )
        else:
            marker_icon = folium.Icon(
                color=color,
                icon=icon,
                prefix="glyphicon"
            )

        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{row['area']} · Score: {score}",
            icon=marker_icon
        ).add_to(cluster)

    # ── Legend ─────────────────────────────────────────────────
    legend_html = f"""
    <div style="
        position: fixed;
        bottom: 30px; right: 30px;
        background: #1e1e2e;
        border: 1px solid #333;
        padding: 14px 18px;
        border-radius: 10px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.5);
        font-family: 'Segoe UI', Arial;
        font-size: 13px;
        color: #e2e8f0;
        z-index: 1000;
    ">
        <b style="font-size:14px;">{business_display}</b>
        <hr style="border-color:#333; margin:8px 0;">
        <div>🟢 Score 65+&nbsp;&nbsp;Excellent</div>
        <div>🟠 Score 50–65&nbsp;Good</div>
        <div>🔵 Score 35–50&nbsp;Average</div>
        <div>🔴 Below 35&nbsp;&nbsp;&nbsp;Low</div>
        <hr style="border-color:#333; margin:8px 0;">
        <div style="font-size:11px; color:#94a3b8;">
            🥇🥈🥉 = Top 3 animated<br>
            🔥 Heatmap = demand zones
        </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    return m

if __name__ == "__main__":
    print("🗺️ Building enhanced map...")
    m = build_map(business_type="cafe", city_filter="All")
    m.save("test_map.html")
    print("✅ Enhanced map saved as test_map.html")
    print("   Open in browser to see all enhancements!")