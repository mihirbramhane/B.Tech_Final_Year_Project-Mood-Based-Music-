"""
🎧 Mood-Based Music Player — Streamlit Web Application
Detects facial emotions in real-time and plays matching Spotify playlists.
"""

import streamlit as st

import auth
from styles import CSS
from tabs import render_detect_tab, render_history_tab, render_playlists_tab, render_settings_tab

# ---------------------------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Mood Music Player",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------------------------

if "emotions" not in st.session_state:
    st.session_state.emotions = []
if "status" not in st.session_state:
    st.session_state.status = "waiting"         # waiting | detecting | playing | error
if "last_emotion" not in st.session_state:
    st.session_state.last_emotion = None
if "last_confidence" not in st.session_state:
    st.session_state.last_confidence = None
if "play_message" not in st.session_state:
    st.session_state.play_message = ""
if "detection_count" not in st.session_state:
    st.session_state.detection_count = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "detection_threshold" not in st.session_state:
    st.session_state.detection_threshold = 5

# ---------------------------------------------------------------------------
# Spotify Sign-In Gate
# ---------------------------------------------------------------------------

auth.handle_redirect()

if not auth.is_authenticated():
    st.markdown('<h1 class="hero-title">🎧 Mood Music Player</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-subtitle">Let AI read your emotions and play the perfect playlist</p>',
        unsafe_allow_html=True,
    )

    if st.session_state.get("auth_error"):
        st.error(st.session_state.pop("auth_error"))

    st.markdown('<div class="signin-wrap">', unsafe_allow_html=True)
    st.markdown('''
        <div class="signin-steps">
            <div class="signin-step"><span class="step-emoji">📷</span><span class="step-label">Show your face</span></div>
            <div class="signin-arrow">→</div>
            <div class="signin-step"><span class="step-emoji">🧠</span><span class="step-label">AI detects mood</span></div>
            <div class="signin-arrow">→</div>
            <div class="signin-step"><span class="step-emoji">🎵</span><span class="step-label">Spotify plays it</span></div>
        </div>
    ''', unsafe_allow_html=True)

    try:
        authorize_url = auth.build_authorize_url()
        st.markdown(
            f'<a class="spotify-connect-btn" href="{authorize_url}">'
            f'🎧 Connect with Spotify</a>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p style="color:#64748b; font-size:0.85rem; margin-top:1.5rem;">'
            'You need Spotify Premium and an active Spotify device (phone, desktop, or web player) '
            'for playback to start.</p>',
            unsafe_allow_html=True,
        )
    except RuntimeError as e:
        st.error(str(e))

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ---------------------------------------------------------------------------
# Signed-in: build the Spotify client for this session
# ---------------------------------------------------------------------------

sp = auth.get_spotify_client()
if sp is None:
    st.warning("Your Spotify session expired. Please sign in again.")
    st.rerun()

# ---------------------------------------------------------------------------
# Sidebar: account + connection status
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown('<p class="sidebar-title">🎧 Mood Music Player</p>', unsafe_allow_html=True)
    st.markdown(
        '<span class="status-badge status-playing">✅ Spotify Connected</span>',
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown(
        '<p style="color:#64748b; font-size:0.8rem; text-align:center;">'
        'Built with ❤️ using Streamlit, TensorFlow & Spotify API'
        '</p>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Main Content
# ---------------------------------------------------------------------------

st.markdown('<h1 class="hero-title">🎧 Mood Music Player</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-subtitle">Let AI read your emotions and play the perfect playlist</p>',
    unsafe_allow_html=True,
)
st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

tab_detect, tab_history, tab_playlists, tab_settings = st.tabs(
    ["🎯 Detect", "📊 History", "🎵 Playlists", "⚙️ Settings"]
)

with tab_detect:
    render_detect_tab(sp)

with tab_history:
    render_history_tab()

with tab_playlists:
    render_playlists_tab()

with tab_settings:
    render_settings_tab(sp)

# ---- Footer ----
st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center; color:#475569; font-size:0.8rem; padding:1rem 0;">'
    '🎧 Mood Music Player • Powered by TensorFlow + Spotify • Take snapshots to detect your emotion'
    '</p>',
    unsafe_allow_html=True,
)
