# dashboard/rankings.py
import streamlit as st
from engine.recommender import get_recommendations, explain_recommendation
from engine.business_profiles import BUSINESS_PROFILES, get_display_names

def show_rankings():

    st.markdown("## 🏆 Location Rankings")
    st.caption("Select your business type and city to see ranked recommendations")

    col1, col2, col3 = st.columns([2, 2, 1])
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
            "City",
            ["All", "Noida", "Delhi", "Gurgaon", "Ghaziabad", "Greater Noida"]
        )

    with col3:
        top_n = st.selectbox("Show Top", [5, 10, 15, 30], index=1)

    st.divider()

    results = get_recommendations(business_type, city_filter, top_n)

    if results.empty:
        st.warning("No areas found for the selected filters.")
        return

    profile = BUSINESS_PROFILES[business_type]

    with st.container(border=True):
        st.markdown(f"### {profile['display_name']}")
        st.caption(profile['description'])
        st.caption(f"Ideal for: {', '.join(profile['ideal_for'])}")

    st.divider()

    medals = {1: "🥇", 2: "🥈", 3: "🥉"}

    for _, row in results.iterrows():
        rank  = row["rank"]
        medal = medals.get(rank, f"#{rank}")
        score = row["business_score"]

        if score >= 65:
            indicator = "🟢"
        elif score >= 50:
            indicator = "🟡"
        elif score >= 35:
            indicator = "🔵"
        else:
            indicator = "🔴"

        explanations = explain_recommendation(row, business_type)

        with st.container(border=True):
            col_left, col_right = st.columns([4, 1])

            with col_left:
                st.markdown(f"### {medal} {row['area']}")
                st.caption(row['city'])

                m1, m2, m3, m4, m5 = st.columns(5)
                m1.metric("🚇 Metro",       f"{row['metro_distance_km']} km")
                m2.metric("🏠 Rent",        f"₹{int(row['avg_rent']):,}")
                m3.metric("⚔️ Competition", f"{row['competition_score']}/10")
                m4.metric("📈 Growth",      f"{row['growth_rate']}%")
                m5.metric("💰 Income",      f"₹{int(row['avg_income']):,}")

                if explanations:
                    st.markdown("**Why this location?**")
                    for exp in explanations:
                        st.markdown(f"- {exp}")

            with col_right:
                st.markdown(f"## {indicator}")
                st.metric("Score", score)