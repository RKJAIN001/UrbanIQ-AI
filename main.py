# main.py
import streamlit as st
# Auto-initialize database
from setup import initialize
initialize()

st.set_page_config(
    page_title="UrbanIQ AI",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

from dashboard.home import show_home
from dashboard.map_page import show_map
from dashboard.rankings import show_rankings
from dashboard.analytics import show_analytics
from dashboard.ai_advisor import show_ai_advisor
from dashboard.landing import show_landing
from dashboard.auth import show_auth
from dashboard.compare import show_compare

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
* { font-family: 'Inter', sans-serif; }

/* ── Hide ALL Streamlit chrome ── */
[data-testid="stHeader"]      { display: none !important; }
[data-testid="stToolbar"]     { display: none !important; }
[data-testid="stDecoration"]  { display: none !important; }
[data-testid="stStatusWidget"]{ display: none !important; }
[data-testid="stMainMenu"]    { display: none !important; }
.stApp > header               { display: none !important; }
#MainMenu                     { display: none !important; }
footer                        { display: none !important; }

/* ── App base ── */
.stApp {
    margin-top: 0 !important;
    background-color: #050816 !important;
    color: #e2e8f0 !important;
}
.block-container {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    max-width: 100% !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #0a0f1e !important;
    border-right: 1px solid #1e293b !important;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="collapsedControl"] {
    display: block !important;
    visibility: visible !important;
    color: white !important;
    background: #0a0f1e !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: #0a0f1e !important;
    border: 1px solid #1e293b !important;
    border-radius: 12px !important;
    padding: 16px !important;
}
[data-testid="stMetricLabel"] {
    color: #475569 !important;
    font-size: 12px !important;
}
[data-testid="stMetricValue"] {
    color: #e2e8f0 !important;
    font-size: 24px !important;
    font-weight: 700 !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #0ea5e9, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.3s !important;
}
.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(124,58,237,0.4) !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: #0a0f1e !important;
    border: 1px solid #1e293b !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0a0f1e !important;
    border-radius: 12px !important;
    padding: 4px !important;
    border: 1px solid #1e293b !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: #475569 !important;
    font-weight: 600 !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #0ea5e9, #7c3aed) !important;
    color: white !important;
}

/* ── Input ── */
.stTextInput > div > div > input {
    background: #0a0f1e !important;
    border: 1px solid #1e293b !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}
.stTextInput > div > div > input:focus {
    border-color: #0ea5e9 !important;
    box-shadow: 0 0 0 2px rgba(14,165,233,0.15) !important;
}
.stTextInput label { color: #94a3b8 !important; }

/* ── Text area ── */
.stTextArea > div > div > textarea {
    background: #0a0f1e !important;
    border: 1px solid #1e293b !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

/* ── Divider ── */
hr { border-color: #1e293b !important; }

/* ── Containers ── */
[data-testid="stVerticalBlock"] > div {
    background: transparent !important;
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
if not st.session_state.logged_in:
    if st.session_state.show_auth:
        show_auth()
    else:
        show_landing()

else:
    # ── Sidebar ────────────────────────────────────────────────
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center; padding:24px 0 16px 0;">
            <div style="
                width:56px; height:56px;
                background:linear-gradient(135deg,#0ea5e9,#7c3aed);
                border-radius:16px;
                display:flex; align-items:center;
                justify-content:center;
                font-size:28px;
                margin:0 auto 12px auto;
                box-shadow:0 8px 24px rgba(124,58,237,0.4);
            ">🏙️</div>
            <div style="font-size:18px; font-weight:800;
                        color:#fff;">UrbanIQ AI</div>
            <div style="font-size:11px; color:#475569; margin-top:4px;">
                Business Location Intelligence
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#050816; border:1px solid #1e293b;
                    border-radius:10px; padding:12px 14px;
                    margin:0 0 12px 0;">
            <div style="font-size:11px; color:#475569;">
                Logged in as
            </div>
            <div style="font-size:14px; color:#0ea5e9;
                        font-weight:600; margin-top:2px;">
        """ + st.session_state.user_name + """
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#1e293b; margin:0 0 12px 0;'>",
                    unsafe_allow_html=True)

        page = st.selectbox(
            "Navigate",
            ["🏠 Home", "🗺️ Map", "🏆 Rankings",
             "📊 Analytics", "🤖 AI Advisor", "⚖️ Compare"],
            label_visibility="collapsed"
        )

        st.markdown("<hr style='border-color:#1e293b; margin:12px 0;'>",
                    unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#050816; border:1px solid #1e293b;
                    border-radius:10px; padding:14px;
                    margin-bottom:12px;">
            <div style="font-size:11px; color:#475569;
                        font-weight:600; margin-bottom:10px;
                        letter-spacing:1px;">PLATFORM STATS</div>
            <div style="display:flex; justify-content:space-between;
                        margin-bottom:8px;">
                <span style="font-size:12px; color:#475569;">
                    📍 Areas
                </span>
                <span style="font-size:12px; color:#0ea5e9;
                             font-weight:700;">60</span>
            </div>
            <div style="display:flex; justify-content:space-between;
                        margin-bottom:8px;">
                <span style="font-size:12px; color:#475569;">
                    🏢 Business Types
                </span>
                <span style="font-size:12px; color:#0ea5e9;
                             font-weight:700;">8</span>
            </div>
            <div style="display:flex; justify-content:space-between;
                        margin-bottom:8px;">
                <span style="font-size:12px; color:#475569;">
                    🌆 Cities
                </span>
                <span style="font-size:12px; color:#0ea5e9;
                             font-weight:700;">5</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <span style="font-size:12px; color:#475569;">
                    📊 Data Points
                </span>
                <span style="font-size:12px; color:#0ea5e9;
                             font-weight:700;">900+</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_name = ""
            st.session_state.show_auth = False
            st.rerun()

        st.markdown("""
        <div style="font-size:11px; color:#334155;
                    text-align:center; padding:8px 0;">
            UrbanIQ Engine v2.0 · NCR India
        </div>
        """, unsafe_allow_html=True)

    # ── Page Routing ───────────────────────────────────────────
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