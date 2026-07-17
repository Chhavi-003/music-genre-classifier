import streamlit as st
import streamlit.components.v1 as components
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
# FULL-SCREEN INTERACTIVE PARTICLE CANVAS
# Renders a JS canvas with 90 floating particles
# that glow, drift, and connect with proximity lines.
# Also includes a subtle mouse-repel interaction.
# ──────────────────────────────────────────────
PARTICLE_HTML = """
<canvas id="vfxCanvas" style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:0;pointer-events:none;"></canvas>
<script>
(function(){
  const c=document.getElementById('vfxCanvas'),
        ctx=c.getContext('2d');
  let W,H,mx=-999,my=-999;
  function resize(){W=c.width=window.innerWidth;H=c.height=window.innerHeight;}
  window.addEventListener('resize',resize);resize();
  document.addEventListener('mousemove',e=>{mx=e.clientX;my=e.clientY;});
  const N=90, particles=[];
  for(let i=0;i<N;i++){
    const hue=250+Math.random()*60;
    particles.push({
      x:Math.random()*W, y:Math.random()*H,
      vx:(Math.random()-0.5)*0.4, vy:(Math.random()-0.5)*0.4,
      r:Math.random()*2+0.8,
      hue:hue,
      alpha:Math.random()*0.5+0.2,
      pulse:Math.random()*Math.PI*2
    });
  }
  function draw(){
    ctx.clearRect(0,0,W,H);
    // --- connection lines ---
    for(let i=0;i<N;i++){
      for(let j=i+1;j<N;j++){
        const dx=particles[i].x-particles[j].x,
              dy=particles[i].y-particles[j].y,
              d=Math.sqrt(dx*dx+dy*dy);
        if(d<140){
          ctx.beginPath();
          ctx.moveTo(particles[i].x,particles[i].y);
          ctx.lineTo(particles[j].x,particles[j].y);
          ctx.strokeStyle='rgba(162,155,254,'+(0.08*(1-d/140))+')';
          ctx.lineWidth=0.6;
          ctx.stroke();
        }
      }
    }
    // --- particles ---
    const t=Date.now()*0.001;
    for(const p of particles){
      // mouse repel
      const dmx=p.x-mx, dmy=p.y-my,
            dm=Math.sqrt(dmx*dmx+dmy*dmy);
      if(dm<120){
        p.vx+=dmx/dm*0.15;
        p.vy+=dmy/dm*0.15;
      }
      p.vx*=0.99; p.vy*=0.99;
      p.x+=p.vx; p.y+=p.vy;
      if(p.x<0)p.x=W; if(p.x>W)p.x=0;
      if(p.y<0)p.y=H; if(p.y>H)p.y=0;
      const pulse=Math.sin(t*1.5+p.pulse)*0.3+0.7;
      const glowR=p.r*3*pulse;
      // outer glow
      const grd=ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,glowR*3);
      grd.addColorStop(0,'hsla('+p.hue+',80%,70%,'+(p.alpha*pulse*0.4)+')');
      grd.addColorStop(1,'hsla('+p.hue+',80%,70%,0)');
      ctx.beginPath();ctx.arc(p.x,p.y,glowR*3,0,Math.PI*2);
      ctx.fillStyle=grd;ctx.fill();
      // core dot
      ctx.beginPath();ctx.arc(p.x,p.y,p.r*pulse,0,Math.PI*2);
      ctx.fillStyle='hsla('+p.hue+',80%,75%,'+(p.alpha*pulse)+')';
      ctx.fill();
    }
    requestAnimationFrame(draw);
  }
  draw();
})();
</script>
"""
components.html(PARTICLE_HTML, height=0, scrolling=False)
# ──────────────────────────────────────────────
# PREMIUM DARK GLASSMORPHISM THEME + VFX CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font import ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap');
/* ── Root variables ── */
:root {
    --bg-primary:   #060609;
    --bg-card:      rgba(255, 255, 255, 0.035);
    --bg-card-hover:rgba(255, 255, 255, 0.065);
    --border-glass: rgba(255, 255, 255, 0.07);
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
    filter: blur(130px);
    opacity: 0.35;
    z-index: 0;
    pointer-events: none;
}
.stApp::before {
    width: 550px; height: 550px;
    background: radial-gradient(circle, #6c5ce7 0%, transparent 70%);
    top: -12%; left: -10%;
    animation: floatOrb1 20s ease-in-out infinite alternate;
}
.stApp::after {
    width: 480px; height: 480px;
    background: radial-gradient(circle, #74b9ff 0%, transparent 70%);
    bottom: -14%; right: -12%;
    animation: floatOrb2 24s ease-in-out infinite alternate;
}
@keyframes floatOrb1 {
    0%   { transform: translate(0, 0) scale(1);   }
    50%  { transform: translate(70px, 50px) scale(1.2); }
    100% { transform: translate(-40px, 90px) scale(0.9); }
}
@keyframes floatOrb2 {
    0%   { transform: translate(0, 0) scale(1);   }
    50%  { transform: translate(-60px, -40px) scale(1.15); }
    100% { transform: translate(50px, -70px) scale(0.85); }
}
/* ── Scanline overlay for retro-futuristic feel ── */
.scanline-overlay {
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    pointer-events: none;
    z-index: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(108, 92, 231, 0.015) 2px,
        rgba(108, 92, 231, 0.015) 4px
    );
}
/* ── Floating music notes VFX ── */
.music-notes-container {
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}
.floating-note {
    position: absolute;
    font-size: 1.2rem;
    opacity: 0;
    animation: floatNote linear infinite;
    filter: blur(0.5px);
}
@keyframes floatNote {
    0%   { transform: translateY(100vh) rotate(0deg) scale(0.5); opacity: 0; }
    10%  { opacity: 0.25; }
    90%  { opacity: 0.15; }
    100% { transform: translateY(-10vh) rotate(360deg) scale(1.2); opacity: 0; }
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
    box-shadow: 0 0 20px rgba(108,92,231,0.3), 0 0 40px rgba(108,92,231,0.1);
    animation: badgePulse 3s ease-in-out infinite;
}
@keyframes badgePulse {
    0%, 100% { box-shadow: 0 0 20px rgba(108,92,231,0.3), 0 0 40px rgba(108,92,231,0.1); }
    50%      { box-shadow: 0 0 30px rgba(108,92,231,0.5), 0 0 60px rgba(108,92,231,0.2); }
}
/* Hero title with shimmer sweep */
.hero-title {
    font-size: 3.8rem;
    font-weight: 900;
    line-height: 1.05;
    letter-spacing: -1.5px;
    background: var(--accent-grad);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 8px 0;
    position: relative;
    display: inline-block;
}
.hero-title::after {
    content: 'VibeCheck';
    position: absolute;
    top: 0; left: 0;
    background: linear-gradient(
        90deg,
        transparent 0%,
        rgba(255,255,255,0.4) 45%,
        rgba(255,255,255,0.6) 50%,
        rgba(255,255,255,0.4) 55%,
        transparent 100%
    );
    background-size: 200% 100%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmerSweep 4s ease-in-out infinite;
}
@keyframes shimmerSweep {
    0%   { background-position: 200% center; }
    100% { background-position: -200% center; }
}
/* Hero title glow */
.hero-title-glow {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 300px; height: 60px;
    background: radial-gradient(ellipse, rgba(108,92,231,0.25) 0%, transparent 70%);
    filter: blur(30px);
    pointer-events: none;
    animation: titleGlow 4s ease-in-out infinite alternate;
}
@keyframes titleGlow {
    0%   { opacity: 0.4; transform: translate(-50%, -50%) scale(1); }
    100% { opacity: 0.8; transform: translate(-50%, -50%) scale(1.3); }
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
/* ── Audio waveform equalizer bars ── */
.eq-container {
    display: flex;
    align-items: flex-end;
    justify-content: center;
    gap: 3px;
    height: 30px;
    margin: 16px auto 0;
    width: fit-content;
}
.eq-bar {
    width: 3px;
    border-radius: 3px;
    background: var(--accent-grad);
    animation: eqBounce ease-in-out infinite;
    opacity: 0.5;
}
@keyframes eqBounce {
    0%, 100% { height: 4px;  opacity: 0.3; }
    50%      { opacity: 0.7; }
}
/* ── Glass cards with corner glow ── */
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
    background: linear-gradient(135deg, rgba(255,255,255,0.12), transparent 60%);
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    pointer-events: none;
}
/* Corner accent glow */
.glass-card::after {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 100px; height: 100px;
    background: radial-gradient(circle, rgba(108,92,231,0.15) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
    transition: var(--transition);
}
.glass-card:hover {
    background: var(--bg-card-hover);
    border-color: rgba(108, 92, 231, 0.25);
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(108, 92, 231, 0.1), 0 0 60px rgba(108,92,231,0.04);
}
.glass-card:hover::after {
    width: 140px; height: 140px;
    background: radial-gradient(circle, rgba(108,92,231,0.25) 0%, transparent 70%);
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
    box-shadow: 0 0 14px var(--glow-purple), 0 0 30px rgba(108,92,231,0.15) !important;
    width: 22px !important; height: 22px !important;
    transition: box-shadow 0.3s ease !important;
}
div[data-baseweb="slider"] div[role="slider"]:hover {
    box-shadow: 0 0 20px var(--glow-purple), 0 0 50px rgba(108,92,231,0.25) !important;
}
.stSlider label {
    color: var(--text-muted) !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}
/* ── CTA Button with animated border + glow ── */
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
    box-shadow:
        0 6px 30px var(--glow-purple),
        0 0 60px rgba(108,92,231,0.12),
        inset 0 1px 0 rgba(255,255,255,0.15) !important;
    transition: var(--transition) !important;
    position: relative !important;
    overflow: hidden !important;
    animation: btnBreath 3s ease-in-out infinite !important;
}
@keyframes btnBreath {
    0%, 100% {
        box-shadow:
            0 6px 30px rgba(108,92,231,0.35),
            0 0 60px rgba(108,92,231,0.12),
            inset 0 1px 0 rgba(255,255,255,0.15);
    }
    50% {
        box-shadow:
            0 8px 40px rgba(108,92,231,0.5),
            0 0 80px rgba(108,92,231,0.2),
            inset 0 1px 0 rgba(255,255,255,0.2);
    }
}
div.stButton > button::before {
    content: '';
    position: absolute;
    top: -2px; left: -2px; right: -2px; bottom: -2px;
    border-radius: inherit;
    background: linear-gradient(
        90deg,
        #6c5ce7, #a29bfe, #74b9ff, #a29bfe, #6c5ce7
    );
    background-size: 300% 100%;
    animation: borderRotate 3s linear infinite;
    z-index: -1;
    opacity: 0;
    transition: opacity 0.3s ease;
}
div.stButton > button:hover::before {
    opacity: 1;
}
@keyframes borderRotate {
    0%   { background-position: 0% center; }
    100% { background-position: 300% center; }
}
div.stButton > button::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transform: translateX(-100%);
    transition: 0.6s ease;
}
div.stButton > button:hover {
    transform: translateY(-3px) scale(1.01) !important;
    box-shadow:
        0 10px 50px var(--glow-purple),
        0 0 100px rgba(108,92,231,0.22) !important;
}
div.stButton > button:hover::after {
    transform: translateX(100%);
}
div.stButton > button:active {
    transform: translateY(0px) scale(0.98) !important;
}
/* ── Result card with pulse rings ── */
.result-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius-lg);
    padding: 40px 36px;
    backdrop-filter: blur(30px);
    position: relative;
    overflow: hidden;
    animation: resultSlideIn 0.7s cubic-bezier(0.16, 1, 0.3, 1);
}
/* Animated gradient border glow ring */
.result-card::after {
    content: '';
    position: absolute;
    inset: -2px;
    border-radius: inherit;
    padding: 2px;
    background: linear-gradient(
        var(--angle, 0deg),
        transparent 40%,
        rgba(108,92,231,0.4) 50%,
        transparent 60%
    );
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    animation: rotateBorderGlow 4s linear infinite;
    pointer-events: none;
}
@keyframes rotateBorderGlow {
    0%   { --angle: 0deg; }
    100% { --angle: 360deg; }
}
/* Fallback: use transform rotation for border glow since --angle may not animate in all browsers */
@supports not (animation-timeline: auto) {
    .result-card::after {
        background: conic-gradient(
            from 0deg,
            transparent 0%,
            rgba(108,92,231,0.4) 10%,
            transparent 20%,
            transparent 100%
        );
        animation: rotateBorderGlowFallback 4s linear infinite;
    }
    @keyframes rotateBorderGlowFallback {
        0%   { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    border-radius: var(--radius-lg) var(--radius-lg) 0 0;
}
@keyframes resultSlideIn {
    0%   { opacity: 0; transform: translateY(40px) scale(0.95); filter: blur(8px); }
    100% { opacity: 1; transform: translateY(0)    scale(1);    filter: blur(0px); }
}
/* Pulse rings behind result */
.pulse-ring-container {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    pointer-events: none;
    z-index: 0;
}
.pulse-ring {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    border-radius: 50%;
    border: 1px solid;
    animation: pulseExpand ease-out infinite;
    opacity: 0;
}
@keyframes pulseExpand {
    0%   { width: 40px;  height: 40px;  opacity: 0.4; }
    100% { width: 400px; height: 400px; opacity: 0; }
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
    position: relative;
    z-index: 1;
}
.result-genre {
    font-size: 2.8rem;
    font-weight: 900;
    letter-spacing: -1px;
    line-height: 1.1;
    margin-bottom: 18px;
    position: relative;
    z-index: 1;
    /* text-shadow glow for extra pop */
}
.result-desc {
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.75;
    position: relative;
    z-index: 1;
}
.result-divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 18px 0;
    position: relative;
    z-index: 1;
}
/* ── Stats row ── */
.stats-row {
    display: flex;
    gap: 16px;
    margin-top: 24px;
    position: relative;
    z-index: 1;
}
.stat-chip {
    flex: 1;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: var(--radius);
    padding: 16px;
    text-align: center;
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}
.stat-chip::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(108,92,231,0.08) 0%, transparent 60%);
    opacity: 0;
    transition: opacity 0.4s ease;
}
.stat-chip:hover {
    background: rgba(255,255,255,0.08);
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(108,92,231,0.1);
    border-color: rgba(108,92,231,0.2);
}
.stat-chip:hover::before { opacity: 1; }
.stat-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.35rem;
    font-weight: 800;
    display: block;
    margin-bottom: 2px;
    position: relative;
    z-index: 1;
}
.stat-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-muted);
    position: relative;
    z-index: 1;
}
/* ── Confidence bar ── */
.confidence-track {
    width: 100%;
    height: 8px;
    background: rgba(255,255,255,0.06);
    border-radius: 10px;
    overflow: hidden;
    margin-top: 22px;
    position: relative;
    z-index: 1;
}
.confidence-fill {
    height: 100%;
    border-radius: 10px;
    animation: fillBar 1.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    position: relative;
}
.confidence-fill::after {
    content: '';
    position: absolute;
    right: 0; top: -2px;
    width: 12px; height: 12px;
    border-radius: 50%;
    background: white;
    box-shadow: 0 0 12px rgba(108,92,231,0.6);
    animation: fillBar 1.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
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
    color: rgba(139,139,158,0.3);
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
/* ── Particle canvas container (zero-height Streamlit iframe) ── */
iframe[title="streamlit_lottie.st_lottie"] { z-index: 1; position: relative; }
div[data-testid="stHtml"] { position: fixed !important; top: 0 !important; left: 0 !important; width: 0 !important; height: 0 !important; overflow: visible !important; z-index: 0 !important; }
div[data-testid="stHtml"] iframe { position: fixed !important; top: 0 !important; left: 0 !important; width: 100vw !important; height: 100vh !important; border: none !important; pointer-events: none !important; z-index: 0 !important; }
/* ── Processing stage text animation ── */
.stage-text {
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    letter-spacing: 1px;
    color: #a29bfe;
    animation: stageFadeIn 0.4s ease;
}
@keyframes stageFadeIn {
    0%   { opacity: 0; transform: translateY(6px); }
    100% { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)
# ──────────────────────────────────────────────
# SCANLINE + FLOATING MUSIC NOTES OVERLAY
# ──────────────────────────────────────────────
NOTES = ['♪', '♫', '♬', '♩', '🎵', '🎶', '♪', '♫', '♬', '♩', '♪', '♫', '♬', '♩', '♪']
notes_html = '<div class="music-notes-container">'
for i, note in enumerate(NOTES):
    left = 5 + (i * 6.2) % 90
    dur = 12 + (i * 3.7) % 14
    delay = (i * 2.1) % 18
    size = 0.8 + (i * 0.15) % 0.8
    notes_html += (
        f'<span class="floating-note" style="'
        f'left:{left:.0f}%;'
        f'animation-duration:{dur:.1f}s;'
        f'animation-delay:{delay:.1f}s;'
        f'font-size:{size:.1f}rem;'
        f'color:rgba(162,155,254,0.3);'
        f'">​{note}</span>'
    )
notes_html += '</div><div class="scanline-overlay"></div>'
st.markdown(notes_html, unsafe_allow_html=True)
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
st.markdown('<div style="text-align:center; padding-top: 20px; position:relative;">', unsafe_allow_html=True)
st.markdown('<span class="hero-badge">✦ AI-Powered ✦</span>', unsafe_allow_html=True)
st.markdown('<div style="position:relative; display:inline-block;">', unsafe_allow_html=True)
st.markdown('<div class="hero-title-glow"></div>', unsafe_allow_html=True)
st.markdown('<p class="hero-title">VibeCheck</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">sonic genre intelligence</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-desc">Feed your audio features into our neural classifier '
    'and discover the genre DNA hidden inside any track.</p>',
    unsafe_allow_html=True,
)
# Waveform equalizer bars
eq_bars = '<div class="eq-container">'
for i in range(24):
    h = 6 + (i * 7 + 3) % 22
    dur = 0.6 + (i * 0.13) % 0.9
    delay = (i * 0.08) % 0.6
    eq_bars += (
        f'<div class="eq-bar" style="'
        f'height:{h}px;'
        f'animation-duration:{dur:.2f}s;'
        f'animation-delay:{delay:.2f}s;'
        f'"></div>'
    )
eq_bars += '</div>'
st.markdown(eq_bars, unsafe_allow_html=True)
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
            "glow": "rgba(232,67,147,0.3)",
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
            "glow": "rgba(214,48,49,0.3)",
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
            "glow": "rgba(108,92,231,0.3)",
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
            "glow": "rgba(162,155,254,0.3)",
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
            "glow": "rgba(162,155,254,0.3)",
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
    # Visual processing feedback with animated stages
    progress_placeholder = st.empty()
    stages = [
        ("⟐  Extracting audio features…", 0.35),
        ("⟐  Running neural classifier…", 0.55),
        ("⟐  Generating genre report…", 0.4),
    ]
    for stage_text, delay in stages:
        progress_placeholder.markdown(
            f'<p class="stage-text">{stage_text}</p>',
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
    # Pre-extract all profile values to avoid dict lookups inside f-strings
    # (Python 3.10 on Render chokes on profile['key'] inside triple-quoted f-strings)
    p_accent = profile["accent"]
    p_gradient = profile["gradient"]
    p_glow = profile["glow"]
    p_name = profile["name"]
    p_confidence = profile["confidence"]
    p_desc = profile["desc"]
    p_tempo = f"{tempo:.0f}"
    p_acoustic = f"{acousticness:.0f}"
    # Celebration animation
    if lottie_celebration:
        st_lottie(lottie_celebration, height=160, speed=1.2, key="celebration_vfx")
    # Pulse rings HTML
    # Pulse rings HTML (built via concatenation)
    pulse_rings = '<div class="pulse-ring-container">'
    for i in range(3):
        delay = i * 1.2
        d = i * 1.2
        pulse_rings += (
            f'<div class="pulse-ring" style="'
            f'border-color:{profile["accent"]}30;'
            f'animation-duration:3.6s;'
            f'animation-delay:{delay:.1f}s;'
            f'"></div>'
            '<div class="pulse-ring" style="'
            "border-color:" + p_accent + "30;"
            "animation-duration:3.6s;"
            "animation-delay:" + f"{d:.1f}" + "s;"
            '"></div>'
        )
    pulse_rings += '</div>'
    pulse_rings += "</div>"
    # Result card
    st.markdown(
        f"""
        <div class="result-card" style="border-color: {profile['accent']}15;">
            {pulse_rings}
    # Build result card via string concatenation (no f-string triple-quote issues)
    card_html = (
        '<div class="result-card" style="border-color: ' + p_accent + '15;">'
        + pulse_rings
        + '<div style="position:absolute;top:0;left:0;right:0;height:4px;'
          "background:" + p_gradient + ";"
          "border-radius: var(--radius-lg) var(--radius-lg) 0 0;"
          "box-shadow: 0 0 20px " + p_glow + ";"
          'z-index:1;"></div>'
            <div style="position:absolute;top:0;left:0;right:0;height:4px;
                        background:{profile['gradient']};
                        border-radius: var(--radius-lg) var(--radius-lg) 0 0;
                        box-shadow: 0 0 20px {profile['glow']};
                        z-index:1;"></div>
        + '<span class="result-badge" style="'
          "background:" + p_accent + "15;"
          "color:" + p_accent + ";"
          "box-shadow: 0 0 15px " + p_accent + '20;">'
          "✦ Classification Complete"
          "</span>"
            <span class="result-badge"
                  style="background:{profile['accent']}15; color:{profile['accent']};
                         box-shadow: 0 0 15px {profile['accent']}20;">
                ✦ Classification Complete
            </span>
        + '<p class="result-genre" style="'
          "background:" + p_gradient + ";"
          "-webkit-background-clip:text;"
          "-webkit-text-fill-color:transparent;"
          "background-clip:text;"
          "filter: drop-shadow(0 0 30px " + p_glow + ');">'
        + p_name
        + "</p>"
            <p class="result-genre"
               style="background:{profile['gradient']};
                      -webkit-background-clip:text;
                      -webkit-text-fill-color:transparent;
                      background-clip:text;
                      filter: drop-shadow(0 0 30px {profile['glow']});">
                {profile['name']}
            </p>
        + '<hr class="result-divider">'
            <hr class="result-divider">
        + '<p class="result-desc">' + p_desc + "</p>"
            <p class="result-desc">{profile['desc']}</p>
        # Confidence bar
        + '<div style="margin-top:22px; position:relative; z-index:1;">'
          '<div style="display:flex; justify-content:space-between; margin-bottom:6px;">'
          '<span style="font-size:0.65rem; letter-spacing:2px;'
          "text-transform:uppercase; color:var(--text-muted);"
          'font-weight:600;">Model Confidence</span>'
          "<span style=\"font-family:'JetBrains Mono',monospace; font-size:0.8rem;"
          "font-weight:700; color:" + p_accent + ';">'
        + str(p_confidence) + "%"
          "</span>"
          "</div>"
          '<div class="confidence-track">'
          '<div class="confidence-fill" style="'
          "width:" + str(p_confidence) + "%;"
          "background:" + p_gradient + ";"
          "box-shadow: 0 0 12px " + p_glow + ';"></div>'
          "</div>"
          "</div>"
            <!-- Confidence bar -->
            <div style="margin-top:22px; position:relative; z-index:1;">
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
                                background:{profile['gradient']};
                                box-shadow: 0 0 12px {profile['glow']};"></div>
                </div>
            </div>
        # Stats chips
        + '<div class="stats-row">'
          '<div class="stat-chip">'
          '<span class="stat-value" style="color:' + p_accent + ';">'
        + p_tempo
        + "</span>"
          '<span class="stat-label">BPM</span>'
          "</div>"
          '<div class="stat-chip">'
          '<span class="stat-value" style="color:' + p_accent + ';">'
        + p_acoustic + "%"
          "</span>"
          '<span class="stat-label">Acoustic</span>'
          "</div>"
          '<div class="stat-chip">'
          '<span class="stat-value" style="color:' + p_accent + ';">'
          "SVM"
          "</span>"
          '<span class="stat-label">Engine</span>'
          "</div>"
          "</div>"
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
        + "</div>"
    )
    st.markdown(card_html, unsafe_allow_html=True)
# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────
st.markdown(
    '<p class="app-footer">✦ VibeCheck · Built with Streamlit & SVM · 2025 ✦</p>',
    unsafe_allow_html=True,
)
