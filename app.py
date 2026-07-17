import streamlit as st
import pandas as pd
import joblib
import requests
from streamlit_lottie import st_lottie

# Set up stunning page configuration
st.set_page_config(
    page_title="VibeCheck // Genre AI",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS (THE VFX SUITE) ---
st.markdown("""
    <style>
    /* Full page dark synthwave styling */
    .stApp {
        background: linear-gradient(135deg, #0f0c20 0%, #15102a 50%, #06040a 100%);
        color: #e0e0ff;
    }
    
    /* Custom Neon Title styling */
    .neon-title {
        font-size: 3rem !important;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(45deg, #ff007f, #7f00ff, #00f0ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(127, 0, 255, 0.3);
        margin-bottom: 5px;
    }
    .neon-subtitle {
        text-align: center;
        color: #8fa0dd;
        font-family: monospace;
        letter-spacing: 2px;
        margin-bottom: 30px;
    }

    /* Glassmorphic input cards */
    div[data-testid="stVerticalBlock"] > div:has(div.stSlider) {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 25px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(4px);
        margin-bottom: 20px;
    }

    /* Glowing Custom Button Matrix */
    div.stButton > button {
        background: linear-gradient(45deg, #7f00ff, #ff007f) !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        border: none !important;
        padding: 12px 40px !important;
        border-radius: 50px !important;
        width: 100% !important;
        box-shadow: 0 4px 20px rgba(255, 0, 127, 0.4) !important;
        transition: all 0.3s ease-in-out !important;
    }
    div.stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 7px 30px rgba(127, 0, 255, 0.7) !important;
        color: #fff !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- HELPER: LOAD LOTTIE ANIMATIONS (VFX) ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Dynamic audio wave animation
lottie_wave = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_j1adxtlq.json") 

# --- LOAD MODEL MACHINE ---
@st.cache_resource
def load_artifacts():
    model = joblib.load('music_genre_svm.pkl')
    scaler = joblib.load('scaler.pkl')
    return model, scaler

model, scaler = load_artifacts()

# --- HERO HEADER ---
st.markdown('<p class="neon-title">VIBECHECK // AI</p>', unsafe_allow_html=True)
st.markdown('<p class="neon-subtitle">HIGH-PRECISION AUDIO GENRE CLASSIFIER</p>', unsafe_allow_html=True)

# Render VFX audio wave if available
if lottie_wave:
    st_lottie(lottie_wave, height=120, key="wave")

st.write("")

# --- INTERACTIVE GLASS CONTROLS ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("### ⚡ Dynamic Pace")
    tempo = st.slider("Tempo (Beats Per Minute)", min_value=50.0, max_value=250.0, value=120.0, step=1.0)

with col2:
    st.markdown("### 🎻 Sound Profile")
    # Matching scale structure from training (if scaled 0-100 or 0-1)
    acousticness = st.slider("Acousticness Score (%)", min_value=0.0, max_value=100.0, value=15.0, step=1.0)

st.write("")

# --- INFERENCE ENGINE TRIGGER ---
if st.button("ANALYZE SONIC FINGERPRINT"):
    
    # Prep data framework
    input_data = pd.DataFrame([[tempo, acousticness]], columns=['tempo', 'acousticness'])
    scaled_input = scaler.transform(input_data)
    
    # Classify
    prediction = model.predict(scaled_input)[0]
    
    # Visual Effects Pop
    st.balloons()
    
    # Dynamic styling blocks depending on the output genre
    genre_colors = {
        'pop': ('#ff007f', '🎤 POP HITS'),
        'rock': ('#ff5500', '🎸 ROCK / ANTHEM'),
        'edm': ('#00f0ff', '⚡ ELECTRONIC / EDM'),
        'hip-hop/rap': ('#7f00ff', '🔥 HIP-HOP / RAP')
    }
    
    color, display_name = genre_colors.get(prediction.lower(), ('#7f00ff', prediction.upper()))
    
    st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 30px; border-radius: 15px; border-left: 8px solid {color}; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
            <h4 style="color: #8fa0dd; text-transform: uppercase; letter-spacing: 2px; margin: 0;">Classification Complete</h4>
            <h1 style="color: {color}; margin-top: 10px; font-weight: 800; text-shadow: 0 0 15px {color}44;">{display_name}</h1>
        </div>
    """, unsafe_allow_html=True)
