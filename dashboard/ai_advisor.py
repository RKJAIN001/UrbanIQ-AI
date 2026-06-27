# dashboard/ai_advisor.py
import streamlit as st
from engine.ai_advisor import generate_response
from engine.business_profiles import BUSINESS_PROFILES

def show_ai_advisor():

    st.markdown("## 🤖 AI Business Advisor")
    st.caption("Describe your business idea in plain English and get location recommendations")

    # ── Example Queries ────────────────────────────────────────
    st.markdown("**💡 Try these examples:**")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("☕ Cafe in Noida, budget ₹60,000"):
            st.session_state.query = "I want to open a cafe in Noida with budget 60000"
    with col2:
        if st.button("🏋 Gym in Delhi, budget ₹80,000"):
            st.session_state.query = "I want to open a gym in Delhi with budget 80000"
    with col3:
        if st.button("💊 Pharmacy in Gurgaon"):
            st.session_state.query = "I want to open a pharmacy in Gurgaon"

    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("🛒 Grocery Store in Ghaziabad"):
            st.session_state.query = "I want to open a grocery store in Ghaziabad"
    with col5:
        if st.button("💻 Coworking Space in Noida"):
            st.session_state.query = "I want to open a coworking space in Noida"
    with col6:
        if st.button("🍕 Restaurant in Delhi, budget ₹1,00,000"):
            st.session_state.query = "I want to open a restaurant in Delhi with budget 100000"

    st.divider()

    # ── Query Input ────────────────────────────────────────────
    query = st.text_area(
        "Ask the Business Advisor",
        value=st.session_state.get("query", ""),
        placeholder="e.g. I want to open a cafe in Noida with a budget of ₹60,000",
        height=100
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        analyze = st.button("🔍 Analyze", use_container_width=True)

    if not analyze or not query.strip():
        return

    # ── Process Query ──────────────────────────────────────────
    with st.spinner("Analyzing locations..."):
        response = generate_response(query)

    # ── What I Understood ──────────────────────────────────────
    understood = response["understood"]
    st.markdown("### 🧠 What I Understood")

    col1, col2, col3 = st.columns(3)
    with col1:
        btype = understood.get("business")
        if btype:
            profile = BUSINESS_PROFILES[btype]
            st.success(f"Business: {profile['display_name']}")
        else:
            st.error("Business: Not detected")

    with col2:
        city = understood.get("city", "All")
        st.info(f"📍 City: {city}")

    with col3:
        budget = understood.get("budget")
        if budget:
            st.info(f"💰 Budget: ₹{budget:,}/month")
        else:
            st.info("💰 Budget: Not specified")

    # ── Error Handling ─────────────────────────────────────────
    if response.get("error"):
        st.error(f"❌ {response['error']}")
        return

    if response.get("message"):
        st.warning(f"⚠️ {response['message']}")

    st.divider()

    # ── Recommendations ────────────────────────────────────────
    st.markdown("### 📍 Recommended Locations")

    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
    recs   = response["recommendations"]

    for rec in recs:
        rank  = rec["rank"]
        medal = medals.get(rank, f"#{rank}")
        score = rec["score"]

        if score >= 65:
            score_color = "🟢"
        elif score >= 50:
            score_color = "🟡"
        else:
            score_color = "🔵"

        with st.container(border=True):
            col_left, col_right = st.columns([4, 1])

            with col_left:
                st.markdown(f"### {medal} {rec['area']}")
                st.caption(f"{rec['city']}")

                m1, m2, m3, m4 = st.columns(4)
                m1.metric("🏠 Rent",        f"₹{rec['rent']:,}/mo")
                m2.metric("🚇 Metro",       f"{rec['metro']} km")
                m3.metric("⚔️ Competition", f"{rec['competition']}/10")
                m4.metric("📈 Growth",      f"{rec['growth']}%")

                if rec["explanations"]:
                    st.markdown("**✅ Why this location?**")
                    for exp in rec["explanations"]:
                        st.markdown(f"- {exp}")

            with col_right:
                st.markdown(f"## {score_color}")
                st.metric("Score", score)

    st.divider()

    # ── Chat History ───────────────────────────────────────────
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.session_state.chat_history.append({
        "query": query,
        "business": understood.get("business", "unknown"),
        "city": understood.get("city", "All"),
        "top_result": recs[0]["area"] if recs else "N/A"
    })

    if len(st.session_state.chat_history) > 1:
        st.markdown("### 🕐 Recent Searches")
        for item in reversed(st.session_state.chat_history[-4:]):
            profile = BUSINESS_PROFILES.get(item["business"], {})
            name    = profile.get("display_name", item["business"])
            st.caption(
                f"{name} in {item['city']} → "
                f"Top result: **{item['top_result']}**"
            )