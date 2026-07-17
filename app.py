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

# --- CUSTOM CSS (PREMIUM LIGHT THEME & VFX) ---
st.markdown("""
    <style>
    /* Full page modern crisp light theme styling */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        color: #2c3e50;
    }
    
    /* Elegant Clean Header */
    .neon-title {
        font-size: 3rem !important;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(45deg, #1e3c72, #2a5298);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    .neon-subtitle {
        text-align: center;
        color: #576574;
        font-family: monospace;
        letter-spacing: 2px;
        margin-bottom: 30px;
        font-weight: bold;
    }

    /* Soft shadow neumorphic input cards */
    div[data-testid="stVerticalBlock"] > div:has(div.stSlider) {
        background: rgba(255, 255, 255, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 25px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
        backdrop-filter: blur(8px);
        margin-bottom: 20px;
    }

    /* Override slider labels to remain dark and readable */
    .stSlider label, .stSlider div {
        color: #2c3e50 !important;
        font-weight: 600;
    }

    /* Sleek Clean Button Matrix */
    div.stButton > button {
        background: linear-gradient(45deg, #1e3c72, #2a5298) !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        border: none !important;
        padding: 14px 40px !important;
        border-radius: 50px !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(42, 82, 152, 0.3) !important;
        transition: all 0.3s ease-in-out !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(42, 82, 152, 0.5) !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- HELPER: LOAD MUSIC LOTTIE ANIMATIONS ---
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except:
        return None

# Elegant ambient music wave for the top header
lottie_header_wave = load_lottieurl("https://lottie.host/5b26be23-c5a4-4f23-a189-9b4f0b2bb25a/fM4oHhN9oW.json")
# Confetti music notes animation for the success screen (Replaces generic balloons)
lottie_music_celebration = load_lottieurl("https://lottie.host/80c436ab-6b08-45ec-b91c-7f51be0ccf5d/c3qCgQ2fCc.json")

# --- LOAD MODEL PIPELINE ---
@st.cache_resource
def load_artifacts():
    model = joblib.load('music_genre_svm.pkl')
    scaler = joblib.load('scaler.pkl')
    return model, scaler

model, scaler = load_artifacts()

# --- HERO HEADER ---
st.markdown('<p class="neon-title">🎵 VIBECHECK // AI</p>', unsafe_allow_html=True)
st.markdown('<p class="neon-subtitle">AUDIO FEATURE INTELLIGENCE</p>', unsafe_allow_html=True)

if lottie_header_wave:
    st_lottie(lottie_header_wave, height=100, key="header_wave")

st.write("")

# --- INTERACTIVE INTERFACE ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("### ⚡ Dynamic Pace")
    tempo = st.slider("Tempo (Beats Per Minute)", min_value=50.0, max_value=250.0, value=120.0, step=1.0)

with col2:
    st.markdown("### 🎻 Sound Profile")
    acousticness = st.slider("Acousticness Score (%)", min_value=0.0, max_value=100.0, value=15.0, step=1.0)

st.write("")

# --- INFERENCE ENGINE TRIGGER ---
if st.button("ANALYZE SONIC SIGNATURE"):
    
    # Format input data
    input_data = pd.DataFrame([[tempo, acousticness]], columns=['tempo', 'acousticness'])
    scaled_input = scaler.transform(input_data)
    
    # Classify
    prediction = model.predict(scaled_input)[0]
    
    # Custom Genre Mapping Engine with deep technical breakdown text
    genre_profiles = {
        'pop': {
            'color': '#ff007f', 
            'name': '🎤 POP HITS',
            'desc': f"Pop tracks typically thrive in mid-to-high tempo ranges (currently set at **{tempo} BPM**). Combined with a low acoustic footprint (**{acousticness}%**), this signature signals highly structured, compressed production engineered for modern radio playlists."
        },
        'rock': {
            'color': '#d35400', 
            'name': '🎸 ROCK / ANTHEM',
            'desc': f"The model detected high physical audio energy. Driving drums and string amplification are tightly associated with your dialed **{tempo} BPM**. A low-to-mid acousticness index confirms heavy processing, characteristic of classic guitar-driven wall-of-sound production."
        },
        'electronic/edm': {
            'color': '#00a8ff', 
            'name': '⚡ ELECTRONIC / EDM',
            'desc': f"A crisp **{tempo} BPM** combined with an ultra-low acoustic profile (**{acousticness}%**) lands straight inside synthetic territory. This indicates heavily quantized, synthesized waveforms built explicitly for high-intensity rhythm arrays."
        },
        'hip-hop/rap': {
            'color': '#8e44ad', 
            'name': '🔥 HIP-HOP / RAP',
            'desc': f"Your chosen profile match fits modern urban track metrics perfectly. A rhythmic heartbeat pacing at **{tempo} BPM** blended with custom digital soundscapes maps directly to structural loop elements and strong transient responses."
        }
    }
    
    profile = genre_profiles.get(prediction.lower(), {
        'color': '#2a5298', 
        'name': prediction.upper(), 
        'desc': f"Classified successfully. Features calculated: Tempo at {tempo} BPM and Acousticness scale at {acousticness}%."
    })
    
    # Render beautiful Custom Music Notes animation over the output card
    if lottie_music_celebration:
        st_lottie(lottie_music_celebration, height=180, speed=1.2, key="notes_vfx")
        
    # Elegant Output Presentation Display Card
    st.markdown(f"""
        <div style="background: white; padding: 35px; border-radius: 20px; border-top: 8px solid {profile['color']}; box-shadow: 0 15px 40px rgba(0,0,0,0.08); text-align: left; margin-top: -20px;">
            <p style="color: #7f8c8d; text-transform: uppercase; font-size: 0.85rem; font-weight: bold; letter-spacing: 2px; margin: 0 0 5px 0;">Classification Report Summary</p>
            <h1 style="color: {profile['color']}; margin: 0 0 15px 0; font-weight: 800; font-size: 2.2rem;">{profile['name']}</h1>
            <hr style="border: 0; border-top: 1px solid #eaeeed; margin-bottom: 15px;">
            <p style="color: #4f5f6f; font-size: 1.05rem; line-height: 1.6; margin: 0;">{profile['desc']}</p>
        </div>
    """, unsafe_allow_html=True)
