# dashboard/landing.py
import streamlit as st

def show_landing():

    # Check if auth was triggered via query param
    if st.query_params.get("action") == "login":
        st.session_state.show_auth = True
        st.query_params.clear()
        st.rerun()

    st.markdown("""
    <style>
    .stApp { background-color: #050816 !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; }

    @keyframes orb-float {
        0%, 100% { transform: translate(0,0) scale(1); }
        50% { transform: translate(20px,-20px) scale(1.05); }
    }
    @keyframes shimmer {
        0% { background-position: 0% center; }
        100% { background-position: 300% center; }
    }
    @keyframes fade-up {
        from { opacity:0; transform:translateY(24px); }
        to   { opacity:1; transform:translateY(0); }
    }
    @keyframes float {
        0%,100% { transform:translateY(0); }
        50%     { transform:translateY(-8px); }
    }
    @keyframes glow-pulse {
        0%,100% { box-shadow: 0 0 20px rgba(14,165,233,0.3); }
        50%     { box-shadow: 0 0 40px rgba(124,58,237,0.6); }
    }

    .orb-1 {
        position:fixed; width:700px; height:700px;
        background:radial-gradient(circle,#7c3aed22,transparent 70%);
        border-radius:50%; top:-250px; left:-250px;
        pointer-events:none; z-index:0;
        animation:orb-float 8s ease-in-out infinite;
    }
    .orb-2 {
        position:fixed; width:600px; height:600px;
        background:radial-gradient(circle,#0ea5e922,transparent 70%);
        border-radius:50%; bottom:-200px; right:-200px;
        pointer-events:none; z-index:0;
        animation:orb-float 8s ease-in-out infinite reverse;
    }
    .orb-3 {
        position:fixed; width:400px; height:400px;
        background:radial-gradient(circle,#7c3aed11,transparent 70%);
        border-radius:50%; top:40%; right:10%;
        pointer-events:none; z-index:0;
        animation:orb-float 6s ease-in-out infinite 2s;
    }
    .grid-bg {
        position:fixed; inset:0; z-index:0;
        background-image:
            linear-gradient(rgba(14,165,233,0.03) 1px,transparent 1px),
            linear-gradient(90deg,rgba(14,165,233,0.03) 1px,transparent 1px);
        background-size:60px 60px;
        pointer-events:none;
    }

    .navbar {
        position:relative; z-index:100;
        width:100%; height:68px;
        background:rgba(5,8,22,0.95);
        border-bottom:1px solid #1e293b;
        display:flex; align-items:center;
        justify-content:space-between;
        padding:0 60px;
    }
    .nav-logo {
        display:flex; align-items:center; gap:12px;
    }
    .nav-logo-icon {
        width:38px; height:38px;
        background:linear-gradient(135deg,#0ea5e9,#7c3aed);
        border-radius:10px;
        display:flex; align-items:center;
        justify-content:center; font-size:20px;
        box-shadow:0 4px 16px rgba(124,58,237,0.4);
    }
    .nav-logo-text {
        font-size:18px; font-weight:800; color:#fff;
    }
    .nav-links {
        display:flex; align-items:center;
        gap:36px; list-style:none;
    }
    .nav-links a {
        color:#475569; text-decoration:none;
        font-size:14px; font-weight:500;
        transition:color 0.2s; cursor:pointer;
    }
    .nav-links a:hover { color:#e2e8f0; }
    .nav-actions {
        display:flex; align-items:center; gap:12px;
    }
    .nav-cta-link {
        padding:8px 20px;
        background:linear-gradient(135deg,#0ea5e9,#7c3aed);
        border-radius:8px; color:white !important;
        font-size:14px; font-weight:600;
        text-decoration:none;
        animation:glow-pulse 3s ease-in-out infinite;
        display:inline-block;
    }
    .nav-login-link {
        padding:8px 20px;
        border:1px solid #1e293b;
        border-radius:8px; color:#94a3b8 !important;
        font-size:14px; font-weight:500;
        text-decoration:none;
        display:inline-block;
        transition:all 0.2s;
    }
    .nav-login-link:hover {
        border-color:#0ea5e9;
        color:#0ea5e9 !important;
    }

    .hero {
        min-height:100vh;
        display:flex; flex-direction:column;
        align-items:center; justify-content:center;
        text-align:center;
        padding:80px 40px 60px;
        position:relative; z-index:1;
    }
    .hero-badge {
        display:inline-flex; align-items:center; gap:8px;
        background:rgba(14,165,233,0.08);
        border:1px solid rgba(14,165,233,0.25);
        border-radius:100px; padding:6px 18px;
        font-size:12px; font-weight:700;
        color:#0ea5e9; letter-spacing:2px;
        margin-bottom:32px;
        animation:fade-up 0.6s ease both;
        text-transform:uppercase;
    }
    .hero-title {
        font-size:88px; font-weight:900;
        line-height:1.0; margin:0 0 24px 0;
        background:linear-gradient(135deg,
            #fff 0%,#e2e8f0 25%,
            #0ea5e9 50%,#7c3aed 75%,#fff 100%);
        background-size:300% auto;
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
        animation:shimmer 5s linear infinite,
                  fade-up 0.6s ease 0.1s both;
    }
    .hero-sub {
        font-size:20px; color:#64748b;
        max-width:540px; line-height:1.7;
        margin:0 auto 48px auto;
        animation:fade-up 0.6s ease 0.2s both;
    }
    .hero-sub strong { color:#94a3b8; }
    .hero-cta {
        display:flex; gap:16px;
        justify-content:center; margin-bottom:64px;
        flex-wrap:wrap;
        animation:fade-up 0.6s ease 0.3s both;
    }
    .btn-primary-lg {
        padding:14px 36px;
        font-size:16px; font-weight:700;
        background:linear-gradient(135deg,#0ea5e9,#7c3aed);
        border-radius:12px; color:white !important;
        cursor:pointer; transition:all 0.3s;
        box-shadow:0 8px 32px rgba(124,58,237,0.35);
        display:inline-block; text-decoration:none;
        animation:glow-pulse 3s ease-in-out infinite;
    }
    .btn-primary-lg:hover {
        opacity:0.9; transform:translateY(-2px);
        box-shadow:0 16px 48px rgba(124,58,237,0.5);
    }
    .btn-ghost-lg {
        padding:14px 36px;
        font-size:16px; font-weight:600;
        background:transparent;
        border:1px solid #1e293b;
        border-radius:12px; color:#94a3b8 !important;
        cursor:pointer; transition:all 0.2s;
        display:inline-block; text-decoration:none;
    }
    .btn-ghost-lg:hover {
        border-color:#0ea5e9; color:#0ea5e9 !important;
    }
    .stats-bar {
        display:flex; border:1px solid #1e293b;
        border-radius:16px; overflow:hidden;
        animation:fade-up 0.6s ease 0.4s both;
        background:rgba(10,15,30,0.8);
    }
    .stat-item {
        padding:20px 44px; text-align:center;
        border-right:1px solid #1e293b;
        transition:background 0.2s;
    }
    .stat-item:last-child { border-right:none; }
    .stat-item:hover { background:rgba(14,165,233,0.06); }
    .stat-num {
        font-size:34px; font-weight:900;
        background:linear-gradient(135deg,#0ea5e9,#7c3aed);
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
    }
    .stat-label {
        font-size:11px; color:#475569;
        margin-top:4px; letter-spacing:1.5px;
        text-transform:uppercase;
    }

    .section {
        position:relative; z-index:1;
        max-width:1100px; margin:0 auto;
        padding:40px 40px;
    }
    .section-label {
        font-size:12px; font-weight:700;
        color:#0ea5e9; letter-spacing:3px;
        text-align:center; margin-bottom:16px;
        text-transform:uppercase;
    }
    .section-title {
        font-size:48px; font-weight:900;
        color:#fff; text-align:center;
        line-height:1.1; margin:0 0 12px 0;
    }
    .section-sub {
        font-size:15px; color:#475569;
        text-align:center; margin:0 0 48px 0;
    }
    .divider {
        border:none; border-top:1px solid #1e293b;
        width:100%; margin:0;
        position:relative; z-index:1;
    }

    .features-grid {
        display:grid;
        grid-template-columns:repeat(3,1fr);
        gap:20px;
    }
    .feature-card {
        background:#0a0f1e;
        border:1px solid #1e293b;
        border-radius:20px; padding:32px;
        transition:all 0.3s; position:relative;
        overflow:hidden;
    }
    .feature-card::before {
        content:''; position:absolute;
        top:0; left:0; right:0; height:2px;
        background:linear-gradient(90deg,#0ea5e9,#7c3aed);
        opacity:0; transition:opacity 0.3s;
    }
    .feature-card:hover::before { opacity:1; }
    .feature-card:hover {
        border-color:rgba(14,165,233,0.3);
        transform:translateY(-6px);
        box-shadow:0 20px 60px rgba(14,165,233,0.08);
        background:#0d1526;
    }
    .feature-icon-wrap {
        width:52px; height:52px;
        background:linear-gradient(135deg,
            rgba(14,165,233,0.15),rgba(124,58,237,0.15));
        border:1px solid rgba(14,165,233,0.2);
        border-radius:14px;
        display:flex; align-items:center;
        justify-content:center; font-size:24px;
        margin-bottom:20px;
        animation:float 4s ease-in-out infinite;
    }
    .feature-title {
        font-size:17px; font-weight:700;
        color:#e2e8f0; margin-bottom:10px;
    }
    .feature-desc {
        font-size:13px; color:#475569; line-height:1.8;
    }

    .steps-grid {
        display:grid;
        grid-template-columns:repeat(3,1fr);
        gap:24px;
    }
    .step-card {
        background:#0a0f1e;
        border:1px solid #1e293b;
        border-radius:20px; padding:40px 28px;
        text-align:center; transition:all 0.3s;
    }
    .step-card:hover {
        border-color:rgba(124,58,237,0.3);
        box-shadow:0 0 40px rgba(124,58,237,0.08);
        transform:translateY(-4px);
    }
    .step-num {
        width:60px; height:60px;
        background:linear-gradient(135deg,#0ea5e9,#7c3aed);
        border-radius:50%;
        display:flex; align-items:center;
        justify-content:center;
        font-size:24px; font-weight:900; color:white;
        margin:0 auto 24px auto;
        box-shadow:0 8px 32px rgba(124,58,237,0.4);
    }
    .step-title {
        font-size:18px; font-weight:700;
        color:#e2e8f0; margin-bottom:12px;
    }
    .step-desc {
        font-size:13px; color:#475569; line-height:1.8;
    }

    .biz-grid {
        display:grid;
        grid-template-columns:repeat(8,1fr);
        gap:16px;
    }
    .biz-card {
        background:#0a0f1e;
        border:1px solid #1e293b;
        border-radius:16px; padding:20px 8px;
        text-align:center; transition:all 0.3s;
        cursor:pointer;
    }
    .biz-card:hover {
        border-color:rgba(14,165,233,0.4);
        background:rgba(14,165,233,0.05);
        transform:translateY(-4px);
        box-shadow:0 8px 24px rgba(14,165,233,0.15);
    }
    .biz-icon { font-size:32px; }
    .biz-name {
        font-size:11px; color:#475569;
        margin-top:10px; font-weight:500;
    }

    .testimonials-grid {
        display:grid;
        grid-template-columns:repeat(3,1fr);
        gap:20px;
    }
    .testimonial-card {
        background:#0a0f1e;
        border:1px solid #1e293b;
        border-radius:20px; padding:28px;
        transition:all 0.3s;
    }
    .testimonial-card:hover {
        border-color:rgba(124,58,237,0.3);
        transform:translateY(-4px);
    }
    .testimonial-text {
        font-size:14px; color:#94a3b8;
        line-height:1.8; margin-bottom:20px;
        font-style:italic;
    }
    .testimonial-author {
        display:flex; align-items:center; gap:12px;
    }
    .testimonial-avatar {
        width:40px; height:40px;
        background:linear-gradient(135deg,#0ea5e9,#7c3aed);
        border-radius:50%;
        display:flex; align-items:center;
        justify-content:center;
        font-size:16px; font-weight:700; color:white;
    }
    .testimonial-name {
        font-size:14px; font-weight:600; color:#e2e8f0;
    }
    .testimonial-role { font-size:12px; color:#475569; }
    .stars { color:#f59e0b; font-size:14px; margin-bottom:12px; }

    .cta-box {
        background:linear-gradient(135deg,#0a0f1e,#0d1a2e);
        border:1px solid #1e293b;
        border-radius:28px; padding:80px 48px;
        text-align:center; position:relative;
        overflow:hidden; margin:0;
    }
    .cta-box::before {
        content:''; position:absolute;
        top:50%; left:50%;
        transform:translate(-50%,-50%);
        width:600px; height:400px;
        background:radial-gradient(ellipse,
            rgba(124,58,237,0.12) 0%,transparent 70%);
        pointer-events:none;
    }
    .cta-title {
        font-size:52px; font-weight:900;
        color:#fff; margin:0 0 16px 0;
        line-height:1.1; position:relative; z-index:1;
    }
    .cta-sub {
        font-size:16px; color:#475569;
        margin:0 0 40px 0;
        position:relative; z-index:1;
    }

    .footer {
        position:relative; z-index:1;
        border-top:1px solid #1e293b;
        padding:32px 60px;
        display:flex; align-items:center;
        justify-content:space-between;
        flex-wrap:wrap; gap:16px;
    }
    .footer-logo {
        display:flex; align-items:center; gap:10px;
    }
    .footer-copy { font-size:13px; color:#334155; }
    .footer-links { display:flex; gap:24px; }
    .footer-links a {
        font-size:13px; color:#334155;
        text-decoration:none; transition:color 0.2s;
    }
    .footer-links a:hover { color:#e2e8f0; }
    </style>

    <!-- Background -->
    <div class="orb-1"></div>
    <div class="orb-2"></div>
    <div class="orb-3"></div>
    <div class="grid-bg"></div>

    <!-- Navbar — Login/Signup use query params -->
    <div class="navbar">
        <div class="nav-logo">
            <div class="nav-logo-icon">🏙️</div>
            <span class="nav-logo-text">UrbanIQ AI</span>
        </div>
        <ul class="nav-links">
            <li><a href="#features">Features</a></li>
            <li><a href="#how-it-works">How it Works</a></li>
            <li><a href="#businesses">Businesses</a></li>
            <li><a href="#testimonials">Reviews</a></li>
        </ul>
        <div class="nav-actions">
            <a href="?action=login" class="nav-login-link">Login</a>
            <a href="?action=login" class="nav-cta-link">Get Started →</a>
        </div>
    </div>

    <!-- Hero -->
    <div class="hero">
        <div class="hero-badge">✦ AI-POWERED · NCR INDIA · v2.0</div>
        <h1 class="hero-title">UrbanIQ AI</h1>
        <p class="hero-sub">
            Find the <strong>perfect location</strong> for your business.<br>
            Data-driven intelligence for smart entrepreneurs.
        </p>
        <div class="hero-cta">
            <a href="?action=login" class="btn-primary-lg">
                🚀 Get Started Free
            </a>
            <a href="#features" class="btn-ghost-lg">
                Explore Features ↓
            </a>
        </div>
        <div class="stats-bar">
            <div class="stat-item">
                <div class="stat-num">60+</div>
                <div class="stat-label">NCR Locations</div>
            </div>
            <div class="stat-item">
                <div class="stat-num">8</div>
                <div class="stat-label">Business Types</div>
            </div>
            <div class="stat-item">
                <div class="stat-num">5</div>
                <div class="stat-label">Cities</div>
            </div>
            <div class="stat-item">
                <div class="stat-num">900+</div>
                <div class="stat-label">Data Points</div>
            </div>
        </div>
    </div>

    <hr class="divider" id="features">

    <!-- Features -->
    <div class="section">
        <div class="section-label">✦ FEATURES</div>
        <h2 class="section-title">Everything you need</h2>
        <p class="section-sub">to find the perfect business location in NCR</p>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon-wrap">🗺️</div>
                <div class="feature-title">Interactive Map</div>
                <div class="feature-desc">Live dark map with heatmaps, animated marker clusters and rich popups for every NCR location.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon-wrap">🧠</div>
                <div class="feature-title">AI Scoring Engine</div>
                <div class="feature-desc">Business-specific weighted scoring ranks every location perfectly for your exact business type.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon-wrap">📊</div>
                <div class="feature-title">Deep Analytics</div>
                <div class="feature-desc">6+ interactive Plotly charts — rent, growth, competition, income, radar profiles and more.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon-wrap">🏆</div>
                <div class="feature-title">Smart Rankings</div>
                <div class="feature-desc">Ranked recommendations with AI-generated explanations for why each area was chosen.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon-wrap">🤖</div>
                <div class="feature-title">AI Business Advisor</div>
                <div class="feature-desc">Type your idea in plain English. Extract business, city and budget — get instant results.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon-wrap">⚡</div>
                <div class="feature-title">Real-time Scoring</div>
                <div class="feature-desc">Every filter change instantly recalculates scores across all 60 areas. Zero waiting.</div>
            </div>
        </div>
    </div>

    <hr class="divider" id="how-it-works">

    <!-- How it Works -->
    <div class="section">
        <div class="section-label">✦ HOW IT WORKS</div>
        <h2 class="section-title">3 simple steps</h2>
        <p class="section-sub">to find your perfect business location</p>
        <div class="steps-grid">
            <div class="step-card">
                <div class="step-num">1</div>
                <div class="step-title">Choose Business Type</div>
                <div class="step-desc">Select from 8 business types — cafe, gym, pharmacy, restaurant and more. Each has unique AI scoring weights.</div>
            </div>
            <div class="step-card">
                <div class="step-num">2</div>
                <div class="step-title">Set Your Filters</div>
                <div class="step-desc">Filter by city and budget. Our AI engine instantly scores and ranks all 60+ matching locations.</div>
            </div>
            <div class="step-card">
                <div class="step-num">3</div>
                <div class="step-title">Get Recommendations</div>
                <div class="step-desc">View ranked areas on map with scores, detailed analytics and AI-generated explanations.</div>
            </div>
        </div>
    </div>

    <hr class="divider" id="businesses">

    <!-- Business Types -->
    <div class="section">
        <div class="section-label">✦ SUPPORTED BUSINESSES</div>
        <h2 class="section-title">8 business types</h2>
        <p class="section-sub">each with its own intelligent scoring profile</p>
        <div class="biz-grid">
            <div class="biz-card"><div class="biz-icon">☕</div><div class="biz-name">Cafe</div></div>
            <div class="biz-card"><div class="biz-icon">🍕</div><div class="biz-name">Restaurant</div></div>
            <div class="biz-card"><div class="biz-icon">🏋</div><div class="biz-name">Gym</div></div>
            <div class="biz-card"><div class="biz-icon">💊</div><div class="biz-name">Pharmacy</div></div>
            <div class="biz-card"><div class="biz-icon">🛒</div><div class="biz-name">Grocery</div></div>
            <div class="biz-card"><div class="biz-icon">💻</div><div class="biz-name">Co-working</div></div>
            <div class="biz-card"><div class="biz-icon">👕</div><div class="biz-name">Clothing</div></div>
            <div class="biz-card"><div class="biz-icon">📚</div><div class="biz-name">Bookstore</div></div>
        </div>
    </div>

    <hr class="divider" id="testimonials">

    <!-- Testimonials -->
    <div class="section">
        <div class="section-label">✦ WHAT PEOPLE SAY</div>
        <h2 class="section-title">Trusted by entrepreneurs</h2>
        <p class="section-sub">See what business owners say about UrbanIQ AI</p>
        <div class="testimonials-grid">
            <div class="testimonial-card">
                <div class="stars">★★★★★</div>
                <div class="testimonial-text">"UrbanIQ AI saved me months of research. I found the perfect location for my cafe in Noida in just minutes. The scoring system is incredibly accurate."</div>
                <div class="testimonial-author">
                    <div class="testimonial-avatar">R</div>
                    <div>
                        <div class="testimonial-name">Rahul Sharma</div>
                        <div class="testimonial-role">Cafe Owner · Sector 62, Noida</div>
                    </div>
                </div>
            </div>
            <div class="testimonial-card">
                <div class="stars">★★★★★</div>
                <div class="testimonial-text">"The AI advisor understood exactly what I needed. I typed my requirements and got ranked recommendations with detailed explanations. Amazing tool!"</div>
                <div class="testimonial-author">
                    <div class="testimonial-avatar">P</div>
                    <div>
                        <div class="testimonial-name">Priya Mehta</div>
                        <div class="testimonial-role">Gym Owner · Cyber City, Gurgaon</div>
                    </div>
                </div>
            </div>
            <div class="testimonial-card">
                <div class="stars">★★★★★</div>
                <div class="testimonial-text">"As a real estate consultant, I now use UrbanIQ AI for every client recommendation. The analytics and competition data are incredibly valuable."</div>
                <div class="testimonial-author">
                    <div class="testimonial-avatar">A</div>
                    <div>
                        <div class="testimonial-name">Amit Jain</div>
                        <div class="testimonial-role">Real Estate Consultant · Delhi</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <hr class="divider">

    <!-- CTA -->
    <div class="section">
        <div class="cta-box">
            <div class="section-label">✦ GET STARTED TODAY</div>
            <h2 class="cta-title">Ready to find your<br>perfect location?</h2>
            <p class="cta-sub">
                Join smart entrepreneurs using data to make better decisions.
            </p>
            <a href="?action=login" class="btn-primary-lg">
                🚀 Start Now →
            </a>
        </div>
    </div>

    <!-- Footer -->
    <div class="footer">
        <div class="footer-logo">
            <div class="nav-logo-icon">🏙️</div>
            <div>
                <div style="font-size:14px;font-weight:700;color:#fff;">
                    UrbanIQ AI
                </div>
                <div style="font-size:11px;color:#334155;">
                    Business Location Intelligence
                </div>
            </div>
        </div>
        <div style="text-align:center;">
            <div class="footer-copy">
                © 2026 UrbanIQ AI · NCR India · v2.0
            </div>
            <div style="font-size:13px; color:#475569; margin-top:4px;">
                Built with ❤️ by
                <span style="color:#0ea5e9; font-weight:600;">
                    Rakshit Jain
                </span>
            </div>
        </div>
        <div class="footer-links">
            <a href="#features">Features</a>
            <a href="#how-it-works">How it Works</a>
            <a href="#businesses">Businesses</a>
            <a href="#testimonials">Reviews</a>
        </div>
    </div>
    """, unsafe_allow_html=True)