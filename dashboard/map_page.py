# dashboard/map_page.py
import streamlit as st
from streamlit_folium import st_folium
from engine.map_engine import build_map
from engine.business_profiles import get_display_names

def show_map():
    st.markdown("## 🗺️ Interactive Location Map")
    st.caption("Explore NCR areas — click any marker for detailed insights")

    # ── Filters ────────────────────────────────────────────────
    col1, col2 = st.columns([2, 2])

    display_names = get_display_names()

    with col1:
        business_label = st.selectbox(
            "Business Type",
            list(display_names.values())
        )
        business_type = [k for k, v in display_names.items()
                        if v == business_label][0]

    with col2:
        city_filter = st.selectbox(
            "City Filter",
            ["All", "Noida", "Delhi", "Gurgaon", "Ghaziabad", "Greater Noida"]
        )

    st.divider()

    # ── Score Legend ───────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.success("🟢 Score 65+  Excellent")
    c2.warning("🟡 Score 50–65  Good")
    c3.info("🔵 Score 35–50  Average")
    c4.error("🔴 Below 35  Low")

    st.divider()

    # ── Build and Display Map ──────────────────────────────────
    with st.spinner("Building map..."):
        m = build_map(business_type=business_type, city_filter=city_filter)

    st_folium(m, width=1100, height=600)