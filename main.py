# main.py
# UrbanIQ AI - Main Application Entry Point

import streamlit as st

# Page config - MUST be first streamlit command
st.set_page_config(
    page_title="UrbanIQ AI",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import pages
from dashboard.home import show_home
from dashboard.map_page import show_map
from dashboard.rankings import show_rankings
from dashboard.analytics import show_analytics
from dashboard.ai_advisor import show_ai_advisor

# ── Global CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp { background-color: #0f0f1a; color: #e2e8f0; }

[data-testid="stSidebar"] {
    background-color: #1e1e2e;
    border-right: 1px solid #2d2d44;
}

[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

[data-testid="stMetric"] {
    background: #1e1e2e;
    border: 1px solid #2d2d44;
    border-radius: 12px;
    padding: 16px;
}

[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    font-size: 13px !important;
}

[data-testid="stMetricValue"] {
    color: #fff !important;
    font-size: 24px !important;
    font-weight: 700 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-weight: 600;
    transition: all 0.3s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(37, 99, 235, 0.4);
}

.stSelectbox > div > div {
    background: #1e1e2e;
    border: 1px solid #2d2d44;
    border-radius: 8px;
    color: #e2e8f0;
}

.urban-card {
    background: #1e1e2e;
    border: 1px solid #2d2d44;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    transition: all 0.3s;
}

.urban-card:hover {
    border-color: #2563eb;
    box-shadow: 0 4px 20px rgba(37, 99, 235, 0.2);
    transform: translateY(-2px);
}

.section-header {
    font-size: 24px;
    font-weight: 700;
    color: #fff;
    margin-bottom: 8px;
}

.section-sub {
    font-size: 14px;
    color: #94a3b8;
    margin-bottom: 24px;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar Navigation ──────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 20px 0;">
        <div style="font-size:40px;">🏙️</div>
        <div style="font-size:20px; font-weight:700; color:#fff;">UrbanIQ AI</div>
        <div style="font-size:12px; color:#94a3b8;">Business Location Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#2d2d44;'>", unsafe_allow_html=True)

    page = st.selectbox(
        "Navigate",
        ["🏠 Home", "🗺️ Map", "🏆 Rankings", "📊 Analytics", "🤖 AI Advisor"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color:#2d2d44;'>", unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:12px; color:#64748b; text-align:center; padding:10px 0;">
        Powered by UrbanIQ Engine v1.0<br>
        NCR · 30 Areas · 8 Business Types
    </div>
    """, unsafe_allow_html=True)

# ── Route to Pages ──────────────────────────────────────────────
if page == "🏠 Home":
    show_home()
elif page == "🗺️ Map":
    show_map()
elif page == "🏆 Rankings":
    show_rankings()
elif page == "📊 Analytics":
    show_analytics()
elif page == "🤖 AI Advisor":
    show_ai_advisor()