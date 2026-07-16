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
    st.markdown(
        '<div class="app-header">'
        '<span class="app-logo-badge">🎧</span>'
        '<h1 class="hero-title">Mood Music Player</h1>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="hero-subtitle">Let AI read your emotions and play the perfect playlist</p>',
        unsafe_allow_html=True,
    )

    if st.session_state.get("auth_error"):
        st.error(st.session_state.pop("auth_error"))

    st.markdown('''
        <div class="signin-wrap">
            <div class="signin-steps">
                <div class="signin-step"><span class="step-num">1</span><span class="step-emoji">📷</span><span class="step-label">Show your face</span></div>
                <div class="signin-arrow">→</div>
                <div class="signin-step"><span class="step-num">2</span><span class="step-emoji">🧠</span><span class="step-label">AI detects mood</span></div>
                <div class="signin-arrow">→</div>
                <div class="signin-step"><span class="step-num">3</span><span class="step-emoji">🎵</span><span class="step-label">Spotify plays it</span></div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    try:
        authorize_url = auth.build_authorize_url()
        st.markdown(
            f'<div class="signin-wrap">'
            f'<a class="spotify-connect-btn" href="{authorize_url}">🎧 Connect with Spotify</a>'
            f'<p class="signin-note">You need Spotify Premium and an active Spotify device '
            f'(phone, desktop, or web player) for playback to start.</p>'
            f'</div>',
            unsafe_allow_html=True,
        )
    except RuntimeError as e:
        st.error(str(e))

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
    st.markdown(
        '<div class="sidebar-brand">'
        '<span class="badge-icon">🎧</span>'
        '<div><p class="sidebar-title">Mood Music</p>'
        '<p class="sidebar-tagline">AI-powered playback</p></div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<span class="status-badge status-playing"><span class="dot"></span>Spotify Connected</span>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="sidebar-section" style="margin-top:1.2rem;">'
        f'<div class="sidebar-stat-row"><span>Detections this session</span>'
        f'<span class="val">{len(st.session_state.history)}</span></div>'
        f'<div class="sidebar-stat-row"><span>Current status</span>'
        f'<span class="val" style="text-transform:capitalize;">{st.session_state.status}</span></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sidebar-footer">Built with ❤️ using<br/>Streamlit, TensorFlow &amp; Spotify API</p>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Main Content
# ---------------------------------------------------------------------------

st.markdown(
    '<div class="app-header">'
    '<span class="app-logo-badge">🎧</span>'
    '<h1 class="hero-title">Mood Music Player</h1>'
    '</div>',
    unsafe_allow_html=True,
)
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
    '<div class="app-footer">'
    '<span>🎧 Mood Music Player</span>'
    '<span class="foot-links">'
    '<span>Powered by TensorFlow</span>·<span>Spotify Web API</span>·<span>Streamlit</span>'
    '</span>'
    '</div>',
    unsafe_allow_html=True,
)
