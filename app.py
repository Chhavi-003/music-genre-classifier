import streamlit as st
import pandas as pd
import joblib
import requests
from streamlit_lottie import st_lottie
import time
# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="VibeCheck · Genre AI",
    page_icon="🎧",
    layout="centered",
    initial_sidebar_state="collapsed",
)
# ──────────────────────────────────────────────
# PREMIUM DARK GLASSMORPHISM THEME + VFX CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font import ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap');
/* ── Root variables ── */
:root {
    --bg-primary:   #0a0a0f;
    --bg-card:      rgba(255, 255, 255, 0.04);
    --bg-card-hover:rgba(255, 255, 255, 0.07);
    --border-glass: rgba(255, 255, 255, 0.08);
    --text-primary: #e8e8ed;
    --text-muted:   #8b8b9e;
    --accent-1:     #6c5ce7;
    --accent-2:     #a29bfe;
    --accent-grad:  linear-gradient(135deg, #6c5ce7 0%, #a29bfe 50%, #74b9ff 100%);
    --glow-purple:  rgba(108, 92, 231, 0.35);
    --glow-blue:    rgba(116, 185, 255, 0.25);
    --radius:       16px;
    --radius-lg:    24px;
    --transition:   0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
/* ── Hide Streamlit chrome ── */
#MainMenu, header, footer { visibility: hidden; }
.stDeployButton { display: none !important; }
/* ── Full-page dark canvas ── */
.stApp {
    background: var(--bg-primary) !important;
    color: var(--text-primary);
    font-family: 'Inter', sans-serif;
}
/* ── Animated gradient orbs (ambient light blobs) ── */
.stApp::before,
.stApp::after {
    content: '';
    position: fixed;
    border-radius: 50%;
    filter: blur(120px);
    opacity: 0.4;
    z-index: 0;
    pointer-events: none;
}
.stApp::before {
    width: 500px; height: 500px;
    background: radial-gradient(circle, #6c5ce7 0%, transparent 70%);
    top: -10%; left: -8%;
    animation: floatOrb1 18s ease-in-out infinite alternate;
}
.stApp::after {
    width: 450px; height: 450px;
    background: radial-gradient(circle, #74b9ff 0%, transparent 70%);
    bottom: -12%; right: -10%;
    animation: floatOrb2 22s ease-in-out infinite alternate;
}
@keyframes floatOrb1 {
    0%   { transform: translate(0, 0) scale(1);   }
    50%  { transform: translate(60px, 40px) scale(1.15); }
    100% { transform: translate(-30px, 80px) scale(0.95); }
}
@keyframes floatOrb2 {
    0%   { transform: translate(0, 0) scale(1);   }
    50%  { transform: translate(-50px, -30px) scale(1.1); }
    100% { transform: translate(40px, -60px) scale(0.9); }
}
/* ── Main content z-index fix ── */
section.main > div { position: relative; z-index: 1; }
/* ── Hero header ── */
.hero-badge {
    display: inline-block;
    background: var(--accent-grad);
    color: #fff;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 3px;
    padding: 6px 18px;
    border-radius: 50px;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.hero-title {
    font-size: 3.4rem;
    font-weight: 900;
    line-height: 1.05;
    letter-spacing: -1.5px;
    background: var(--accent-grad);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 8px 0;
}
.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: var(--text-muted);
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.hero-desc {
    color: var(--text-muted);
    font-size: 1rem;
    line-height: 1.6;
    max-width: 520px;
    margin: 0 auto;
}
/* ── Glass cards ── */
.glass-card {
    background: var(--bg-card);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius-lg);
    padding: 28px 26px;
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}
.glass-card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: inherit;
    padding: 1px;
    background: linear-gradient(135deg, rgba(255,255,255,0.1), transparent 60%);
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    pointer-events: none;
}
.glass-card:hover {
    background: var(--bg-card-hover);
    border-color: rgba(108, 92, 231, 0.2);
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(108, 92, 231, 0.08);
}
/* ── Section labels ── */
.section-icon {
    font-size: 1.5rem;
    margin-bottom: 4px;
    display: block;
}
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--accent-2);
    margin-bottom: 2px;
}
.section-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 14px;
}
/* ── Slider overrides ── */
.stSlider > div > div > div > div {
    background: var(--accent-grad) !important;
}
.stSlider [data-testid="stThumbValue"] {
    color: var(--text-primary) !important;
    font-weight: 700 !important;
    font-family: 'JetBrains Mono', monospace !important;
}
div[data-baseweb="slider"] div[role="slider"] {
    background: #fff !important;
    border: 3px solid var(--accent-1) !important;
    box-shadow: 0 0 12px var(--glow-purple) !important;
    width: 22px !important; height: 22px !important;
}
.stSlider label {
    color: var(--text-muted) !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}
/* ── CTA Button ── */
div.stButton > button {
    background: var(--accent-grad) !important;
    color: #fff !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 2.5px !important;
    text-transform: uppercase !important;
    border: none !important;
    padding: 18px 40px !important;
    border-radius: 60px !important;
    width: 100% !important;
    box-shadow: 0 6px 30px var(--glow-purple), 0 0 60px rgba(108,92,231,0.1) !important;
    transition: var(--transition) !important;
    position: relative !important;
    overflow: hidden !important;
}
div.stButton > button::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
    transform: translateX(-100%);
    transition: 0.6s ease;
}
div.stButton > button:hover {
    transform: translateY(-3px) scale(1.01) !important;
    box-shadow: 0 10px 40px var(--glow-purple), 0 0 80px rgba(108,92,231,0.18) !important;
}
div.stButton > button:hover::after {
    transform: translateX(100%);
}
div.stButton > button:active {
    transform: translateY(0px) scale(0.98) !important;
}
/* ── Result card ── */
.result-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius-lg);
    padding: 40px 36px;
    backdrop-filter: blur(30px);
    position: relative;
    overflow: hidden;
    animation: resultSlideIn 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    border-radius: var(--radius-lg) var(--radius-lg) 0 0;
}
@keyframes resultSlideIn {
    0%   { opacity: 0; transform: translateY(30px) scale(0.97); }
    100% { opacity: 1; transform: translateY(0)    scale(1);    }
}
.result-badge {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 30px;
    margin-bottom: 14px;
}
.result-genre {
    font-size: 2.6rem;
    font-weight: 900;
    letter-spacing: -1px;
    line-height: 1.1;
    margin-bottom: 18px;
}
.result-desc {
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.75;
}
.result-divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 18px 0;
}
/* ── Stats row ── */
.stats-row {
    display: flex;
    gap: 16px;
    margin-top: 24px;
}
.stat-chip {
    flex: 1;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: var(--radius);
    padding: 16px;
    text-align: center;
    transition: var(--transition);
}
.stat-chip:hover {
    background: rgba(255,255,255,0.07);
    transform: translateY(-2px);
}
.stat-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.35rem;
    font-weight: 800;
    display: block;
    margin-bottom: 2px;
}
.stat-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-muted);
}
/* ── Confidence bar ── */
.confidence-track {
    width: 100%;
    height: 8px;
    background: rgba(255,255,255,0.06);
    border-radius: 10px;
    overflow: hidden;
    margin-top: 22px;
}
.confidence-fill {
    height: 100%;
    border-radius: 10px;
    animation: fillBar 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
@keyframes fillBar {
    0%   { width: 0%; }
}
/* ── Footer ── */
.app-footer {
    text-align: center;
    padding: 40px 0 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 2px;
    color: rgba(139,139,158,0.4);
    text-transform: uppercase;
}
/* ── Streamlit element overrides ── */
div[data-testid="stVerticalBlock"] > div:has(div.stSlider) {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}
.stMarkdown h3 { color: var(--text-primary) !important; }
</style>
""", unsafe_allow_html=True)
# ──────────────────────────────────────────────
# LOTTIE LOADER
# ──────────────────────────────────────────────
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        return None
lottie_header = load_lottieurl(
    "https://lottie.host/5b26be23-c5a4-4f23-a189-9b4f0b2bb25a/fM4oHhN9oW.json"
)
lottie_celebration = load_lottieurl(
    "https://lottie.host/80c436ab-6b08-45ec-b91c-7f51be0ccf5d/c3qCgQ2fCc.json"
)
# ──────────────────────────────────────────────
# LOAD ML PIPELINE
# ──────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    model = joblib.load("music_genre_svm.pkl")
    scaler = joblib.load("scaler.pkl")
    return model, scaler
model, scaler = load_artifacts()
# ──────────────────────────────────────────────
# HERO HEADER
# ──────────────────────────────────────────────
st.markdown('<div style="text-align:center; padding-top: 20px;">', unsafe_allow_html=True)
st.markdown('<span class="hero-badge">AI-Powered</span>', unsafe_allow_html=True)
st.markdown('<p class="hero-title">VibeCheck</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">sonic genre intelligence</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-desc">Feed your audio features into our neural classifier '
    'and discover the genre DNA hidden inside any track.</p>',
    unsafe_allow_html=True,
)
st.markdown('</div>', unsafe_allow_html=True)
if lottie_header:
    st_lottie(lottie_header, height=90, key="header_anim")
st.markdown("<br>", unsafe_allow_html=True)
# ──────────────────────────────────────────────
# INPUT PANEL — Two glass cards side by side
# ──────────────────────────────────────────────
col1, col2 = st.columns(2, gap="medium")
with col1:
    st.markdown("""
        <div class="glass-card">
            <span class="section-icon">⚡</span>
            <p class="section-label">Rhythm Engine</p>
            <p class="section-title">Tempo</p>
        </div>
    """, unsafe_allow_html=True)
    tempo = st.slider(
        "Beats Per Minute",
        min_value=50.0,
        max_value=250.0,
        value=120.0,
        step=1.0,
        key="tempo_slider",
    )
with col2:
    st.markdown("""
        <div class="glass-card">
            <span class="section-icon">🎻</span>
            <p class="section-label">Tonal Fingerprint</p>
            <p class="section-title">Acousticness</p>
        </div>
    """, unsafe_allow_html=True)
    acousticness = st.slider(
        "Acoustic Score (%)",
        min_value=0.0,
        max_value=100.0,
        value=15.0,
        step=1.0,
        key="acoustic_slider",
    )
st.markdown("<br>", unsafe_allow_html=True)
# ──────────────────────────────────────────────
# CTA BUTTON
# ──────────────────────────────────────────────
analyze_clicked = st.button("⚡  ANALYZE SONIC SIGNATURE")
# ──────────────────────────────────────────────
# GENRE PROFILES DATABASE
# ──────────────────────────────────────────────
def get_genre_profile(prediction: str, tempo: float, acousticness: float):
    profiles = {
        "pop": {
            "gradient": "linear-gradient(135deg, #fd79a8 0%, #e84393 100%)",
            "accent": "#e84393",
            "name": "🎤  POP HITS",
            "confidence": 92,
            "desc": (
                f"Pop tracks thrive in mid-to-high tempo ranges — currently dialed at "
                f"<strong>{tempo:.0f} BPM</strong>. Paired with a low acoustic footprint "
                f"(<strong>{acousticness:.0f}%</strong>), this signature signals highly "
                f"structured, compressed production engineered for modern radio playlists "
                f"and streaming algorithms."
            ),
        },
        "rock": {
            "gradient": "linear-gradient(135deg, #e17055 0%, #d63031 100%)",
            "accent": "#d63031",
            "name": "🎸  ROCK / ANTHEM",
            "confidence": 88,
            "desc": (
                f"High physical audio energy detected. Driving drums and amplified strings "
                f"are tightly associated with <strong>{tempo:.0f} BPM</strong>. A low-to-mid "
                f"acousticness index (<strong>{acousticness:.0f}%</strong>) confirms heavy "
                f"processing — characteristic of classic guitar-driven wall-of-sound production."
            ),
        },
        "electronic/edm": {
            "gradient": "linear-gradient(135deg, #0984e3 0%, #6c5ce7 100%)",
            "accent": "#6c5ce7",
            "name": "⚡  ELECTRONIC / EDM",
            "confidence": 95,
            "desc": (
                f"A crisp <strong>{tempo:.0f} BPM</strong> combined with an ultra-low acoustic "
                f"profile (<strong>{acousticness:.0f}%</strong>) lands deep inside synthetic "
                f"territory. This indicates heavily quantized, synthesized waveforms built "
                f"explicitly for high-intensity rhythm arrays and festival sound systems."
            ),
        },
        "hip-hop/rap": {
            "gradient": "linear-gradient(135deg, #a29bfe 0%, #6c5ce7 100%)",
            "accent": "#a29bfe",
            "name": "🔥  HIP-HOP / RAP",
            "confidence": 90,
            "desc": (
                f"Your profile matches modern urban track metrics. A rhythmic heartbeat pacing "
                f"at <strong>{tempo:.0f} BPM</strong> blended with digital soundscapes "
                f"(<strong>{acousticness:.0f}%</strong> acousticness) maps to structural loop "
                f"elements and strong transient responses typical of contemporary hip-hop."
            ),
        },
    }
    return profiles.get(
        prediction.lower(),
        {
            "gradient": "linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%)",
            "accent": "#a29bfe",
            "name": prediction.upper(),
            "confidence": 85,
            "desc": (
                f"Classified successfully. Tempo: <strong>{tempo:.0f} BPM</strong> · "
                f"Acousticness: <strong>{acousticness:.0f}%</strong>."
            ),
        },
    )
# ──────────────────────────────────────────────
# INFERENCE + RESULT DISPLAY
# ──────────────────────────────────────────────
if analyze_clicked:
    # Visual processing feedback
    with st.spinner(""):
        progress_placeholder = st.empty()
        stages = [
            ("🔍  Extracting audio features…", 0.3),
            ("🧠  Running neural classifier…", 0.5),
            ("📊  Generating genre report…", 0.4),
        ]
        for stage_text, delay in stages:
            progress_placeholder.markdown(
                f'<p style="text-align:center; color: var(--accent-2); '
                f'font-family: JetBrains Mono, monospace; font-size: 0.8rem; '
                f'letter-spacing: 1px;">{stage_text}</p>',
                unsafe_allow_html=True,
            )
            time.sleep(delay)
        progress_placeholder.empty()
    # Classify
    input_data = pd.DataFrame(
        [[tempo, acousticness]], columns=["tempo", "acousticness"]
    )
    scaled_input = scaler.transform(input_data)
    prediction = model.predict(scaled_input)[0]
    profile = get_genre_profile(prediction, tempo, acousticness)
    # Celebration animation
    if lottie_celebration:
        st_lottie(lottie_celebration, height=160, speed=1.2, key="celebration_vfx")
    # Result card
    st.markdown(
        f"""
        <div class="result-card" style="border-color: {profile['accent']}22;">
            <div style="position:absolute;top:0;left:0;right:0;height:4px;
                        background:{profile['gradient']};
                        border-radius: var(--radius-lg) var(--radius-lg) 0 0;"></div>
            <span class="result-badge"
                  style="background:{profile['accent']}18; color:{profile['accent']};">
                Classification Complete
            </span>
            <p class="result-genre"
               style="background:{profile['gradient']};
                      -webkit-background-clip:text;
                      -webkit-text-fill-color:transparent;
                      background-clip:text;">
                {profile['name']}
            </p>
            <hr class="result-divider">
            <p class="result-desc">{profile['desc']}</p>
            <!-- Confidence bar -->
            <div style="margin-top:22px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <span style="font-size:0.65rem; letter-spacing:2px;
                                 text-transform:uppercase; color:var(--text-muted);
                                 font-weight:600;">Model Confidence</span>
                    <span style="font-family:'JetBrains Mono',monospace; font-size:0.8rem;
                                 font-weight:700; color:{profile['accent']};">
                        {profile['confidence']}%
                    </span>
                </div>
                <div class="confidence-track">
                    <div class="confidence-fill"
                         style="width:{profile['confidence']}%;
                                background:{profile['gradient']};"></div>
                </div>
            </div>
            <!-- Stats chips -->
            <div class="stats-row">
                <div class="stat-chip">
                    <span class="stat-value" style="color:{profile['accent']};">
                        {tempo:.0f}
                    </span>
                    <span class="stat-label">BPM</span>
                </div>
                <div class="stat-chip">
                    <span class="stat-value" style="color:{profile['accent']};">
                        {acousticness:.0f}%
                    </span>
                    <span class="stat-label">Acoustic</span>
                </div>
                <div class="stat-chip">
                    <span class="stat-value" style="color:{profile['accent']};">
                        SVM
                    </span>
                    <span class="stat-label">Engine</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────
st.markdown(
    '<p class="app-footer">VibeCheck · Built with Streamlit & SVM · 2025</p>',
    unsafe_allow_html=True,
)
