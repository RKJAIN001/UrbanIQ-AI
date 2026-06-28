# main.py
import streamlit as st

st.set_page_config(
    page_title="UrbanIQ AI",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)
from dashboard.compare import show_compare
from dashboard.home import show_home
from dashboard.map_page import show_map
from dashboard.rankings import show_rankings
from dashboard.analytics import show_analytics
from dashboard.ai_advisor import show_ai_advisor
from dashboard.landing import show_landing
from dashboard.auth import show_auth

# ── Global CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background-color: #0f0f1a; color: #e2e8f0; }
[data-testid="stSidebar"] {
    background-color: #1e1e2e !important;
    border-right: 1px solid #2d2d44 !important;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="collapsedControl"] {
    display: block !important;
    visibility: visible !important;
}
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
[data-testid="stMetric"] {
    background: #1e1e2e;
    border: 1px solid #2d2d44;
    border-radius: 12px;
    padding: 16px;
}
[data-testid="stMetricLabel"] { color: #94a3b8 !important; font-size: 13px !important; }
[data-testid="stMetricValue"] { color: #fff !important; font-size: 24px !important; font-weight: 700 !important; }
.stButton > button {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: white !important;
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
</style>
""", unsafe_allow_html=True)

# ── Session State Init ─────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "show_auth" not in st.session_state:
    st.session_state.show_auth = False
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

# ── Routing Logic ──────────────────────────────────────────────

# Not logged in — show landing or auth
if not st.session_state.logged_in:
    if st.session_state.show_auth:
        show_auth()
    else:
        show_landing()

# Logged in — show main app with sidebar
else:
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center; padding:20px 0 10px 0;">
            <div style="font-size:42px;">🏙️</div>
            <div style="font-size:20px; font-weight:700; color:#fff;
                        margin-top:8px;">UrbanIQ AI</div>
            <div style="font-size:11px; color:#64748b; margin-top:4px;">
                Business Location Intelligence
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#0f0f1a; border-radius:8px;
                    padding:10px 12px; margin:8px 0;">
            <div style="font-size:11px; color:#64748b;">Logged in as</div>
            <div style="font-size:14px; color:#60a5fa; font-weight:600;">
                {name}
            </div>
        </div>
        """.replace("{name}", st.session_state.user_name),
        unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#2d2d44; margin:12px 0;'>",
                    unsafe_allow_html=True)

        page = st.selectbox(
    "Navigate",
    ["🏠 Home", "🗺️ Map", "🏆 Rankings",
     "📊 Analytics", "🤖 AI Advisor", "⚖️ Compare"],
    label_visibility="collapsed"
)

        st.markdown("<hr style='border-color:#2d2d44; margin:12px 0;'>",
                    unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#0f0f1a; border-radius:10px;
                    padding:14px; margin-bottom:12px;">
            <div style="font-size:11px; color:#64748b;
                        font-weight:600; margin-bottom:10px;
                        letter-spacing:1px;">PLATFORM STATS</div>
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span style="font-size:12px; color:#94a3b8;">📍 Areas</span>
                <span style="font-size:12px; color:#60a5fa; font-weight:700;">60</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span style="font-size:12px; color:#94a3b8;">🏢 Business Types</span>
                <span style="font-size:12px; color:#60a5fa; font-weight:700;">8</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span style="font-size:12px; color:#94a3b8;">🌆 Cities</span>
                <span style="font-size:12px; color:#60a5fa; font-weight:700;">5</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <span style="font-size:12px; color:#94a3b8;">📊 Data Points</span>
                <span style="font-size:12px; color:#60a5fa; font-weight:700;">900+</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_name = ""
            st.session_state.show_auth = False
            st.rerun()

        st.markdown("""
        <div style="font-size:11px; color:#64748b;
                    text-align:center; padding:8px 0;">
            UrbanIQ Engine v2.0 · NCR India
        </div>
        """, unsafe_allow_html=True)

    # Route pages
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
    elif page == "⚖️ Compare":
        show_compare()