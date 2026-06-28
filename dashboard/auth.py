# dashboard/auth.py
import streamlit as st
import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_users_db():
    conn = sqlite3.connect("database/urbaniq.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def login_user(email, password):
    conn = sqlite3.connect("database/urbaniq.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name, email FROM users WHERE email=? AND password=?",
        (email, hash_password(password))
    )
    user = cursor.fetchone()
    conn.close()
    return user

def register_user(name, email, password):
    try:
        conn = sqlite3.connect("database/urbaniq.db")
        conn.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, hash_password(password))
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def show_auth():
    init_users_db()

    st.markdown("""
    <style>
    .stApp { background-color: #050816 !important; }

    @keyframes orb-float {
        0%, 100% { transform: translate(0,0) scale(1); }
        50% { transform: translate(20px,-20px) scale(1.05); }
    }

    .auth-orb-1 {
        position: fixed;
        width: 500px; height: 500px;
        background: radial-gradient(circle, #7c3aed22, transparent 70%);
        border-radius: 50%;
        top: -150px; left: -150px;
        pointer-events: none;
        animation: orb-float 8s ease-in-out infinite;
        z-index: 0;
    }

    .auth-orb-2 {
        position: fixed;
        width: 400px; height: 400px;
        background: radial-gradient(circle, #0ea5e922, transparent 70%);
        border-radius: 50%;
        bottom: -100px; right: -100px;
        pointer-events: none;
        animation: orb-float 8s ease-in-out infinite reverse;
        z-index: 0;
    }

    .auth-grid {
        position: fixed;
        inset: 0;
        background-image:
            linear-gradient(rgba(14,165,233,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(14,165,233,0.03) 1px, transparent 1px);
        background-size: 60px 60px;
        pointer-events: none;
        z-index: 0;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: #0a0f1e !important;
        border-radius: 12px !important;
        padding: 4px !important;
        border: 1px solid #1e293b !important;
        gap: 4px !important;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 8px !important;
        color: #475569 !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0ea5e9, #7c3aed) !important;
        color: white !important;
    }

    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 24px !important;
    }

    .stTextInput > div > div > input {
        background: #0a0f1e !important;
        border: 1px solid #1e293b !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #0ea5e9 !important;
        box-shadow: 0 0 0 2px rgba(14,165,233,0.15) !important;
    }

    .stTextInput label {
        color: #94a3b8 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }
    </style>

    <div class="auth-orb-1"></div>
    <div class="auth-orb-2"></div>
    <div class="auth-grid"></div>
    """, unsafe_allow_html=True)

    # ── Back Button ────────────────────────────────────────────
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("← Back"):
            st.session_state.show_auth = False
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ── Auth Card ──────────────────────────────────────────────
    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        st.markdown("""
        <div style="text-align:center; margin-bottom:32px;">
            <div style="
                width:64px; height:64px;
                background: linear-gradient(135deg, #0ea5e9, #7c3aed);
                border-radius:18px;
                display:flex; align-items:center;
                justify-content:center;
                font-size:32px;
                margin:0 auto 16px auto;
                box-shadow: 0 8px 32px rgba(124,58,237,0.4);
            ">🏙️</div>
            <h2 style="font-size:28px; font-weight:800;
                       color:#fff; margin:0 0 8px 0;">UrbanIQ AI</h2>
            <p style="font-size:14px; color:#475569; margin:0;">
                Business Location Intelligence
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="
            background: #0a0f1e;
            border: 1px solid #1e293b;
            border-radius: 24px;
            padding: 32px;
        ">
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🔑 Sign In", "✨ Sign Up"])

        with tab1:
            st.markdown("""
            <div style="margin-bottom:24px;">
                <div style="font-size:20px; font-weight:700;
                            color:#fff; margin-bottom:6px;">
                    Welcome back!
                </div>
                <div style="font-size:13px; color:#475569;">
                    Sign in to your UrbanIQ account
                </div>
            </div>
            """, unsafe_allow_html=True)

            email = st.text_input(
                "Email address",
                placeholder="you@example.com",
                key="login_email"
            )
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_pass"
            )

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("🚀 Sign In",
                         use_container_width=True,
                         key="login_btn"):
                if email and password:
                    user = login_user(email, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user_name = user[0]
                        st.session_state.show_auth = False
                        st.session_state["sidebar_open"] = True
                        st.rerun()
                    else:
                        st.error("❌ Invalid email or password")
                else:
                    st.warning("Please fill in all fields")

            st.markdown("""
            <div style="text-align:center; margin-top:20px;
                        font-size:13px; color:#475569;">
                Don't have an account?
                <span style="color:#0ea5e9;">Click Sign Up above</span>
            </div>
            """, unsafe_allow_html=True)

        with tab2:
            st.markdown("""
            <div style="margin-bottom:24px;">
                <div style="font-size:20px; font-weight:700;
                            color:#fff; margin-bottom:6px;">
                    Create account
                </div>
                <div style="font-size:13px; color:#475569;">
                    Start finding perfect business locations
                </div>
            </div>
            """, unsafe_allow_html=True)

            name = st.text_input(
                "Full Name",
                placeholder="Rakshit Jain",
                key="reg_name"
            )
            email = st.text_input(
                "Email address",
                placeholder="you@example.com",
                key="reg_email"
            )
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Min 6 characters",
                key="reg_pass"
            )
            confirm = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Repeat password",
                key="reg_confirm"
            )

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("✅ Create Account",
                         use_container_width=True,
                         key="reg_btn"):
                if name and email and password and confirm:
                    if password != confirm:
                        st.error("❌ Passwords don't match")
                    elif len(password) < 6:
                        st.error("❌ Password must be at least 6 characters")
                    else:
                        if register_user(name, email, password):
                            st.success("✅ Account created! Please sign in.")
                        else:
                            st.error("❌ Email already registered")
                else:
                    st.warning("Please fill in all fields")

            st.markdown("""
            <div style="text-align:center; margin-top:20px;
                        font-size:13px; color:#475569;">
                Already have an account?
                <span style="color:#0ea5e9;">Click Sign In above</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div style="display:flex; justify-content:center;
                    gap:24px; margin-top:24px;">
            <div style="font-size:12px; color:#334155;">
                🔒 Secure Login
            </div>
            <div style="font-size:12px; color:#334155;">
                ⚡ Instant Access
            </div>
            <div style="font-size:12px; color:#334155;">
                🆓 Free Forever
            </div>
        </div>
        <div style="text-align:center; margin-top:16px;
                    font-size:12px; color:#334155;">
            Built with ❤️ by
            <span style="color:#0ea5e9; font-weight:600;">
                Rakshit Jain
            </span>
        </div>
        """, unsafe_allow_html=True)