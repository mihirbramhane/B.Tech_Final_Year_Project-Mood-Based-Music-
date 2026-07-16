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
)

st.markdown(CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------------------------

if "status" not in st.session_state:
    st.session_state.status = "waiting"         # waiting | playing | error
if "last_emotion" not in st.session_state:
    st.session_state.last_emotion = None
if "last_confidence" not in st.session_state:
    st.session_state.last_confidence = None
if "play_message" not in st.session_state:
    st.session_state.play_message = ""
if "history" not in st.session_state:
    st.session_state.history = []
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "detect"

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
# Sticky slim header: branding + connection status (replaces the sidebar)
# ---------------------------------------------------------------------------

st.markdown(
    '<div class="sticky-header">'
    '<div class="sticky-header-brand">'
    '<span class="sticky-logo">🎧</span>'
    '<span class="sticky-title">Mood Music Player</span>'
    '</div>'
    '<span class="status-badge status-playing sticky-status">'
    '<span class="dot"></span><span class="sticky-status-text">Connected</span>'
    '</span>'
    '</div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Navigation: bottom bar on mobile, pill row on desktop — same buttons, one
# CSS media query flips the layout. Drives st.session_state.active_tab,
# which the dispatch below reads to call the matching render_*_tab().
# ---------------------------------------------------------------------------

NAV_ITEMS = [
    ("detect", "🎯 Detect"),
    ("history", "📊 History"),
    ("playlists", "🎵 Playlists"),
    ("settings", "⚙️ Settings"),
]

with st.container(border=True):
    st.markdown('<span class="bottom-nav-marker"></span>', unsafe_allow_html=True)
    nav_cols = st.columns(len(NAV_ITEMS))
    for col, (tab_key, label) in zip(nav_cols, NAV_ITEMS):
        with col:
            is_active = st.session_state.active_tab == tab_key
            if st.button(
                label,
                key=f"nav_{tab_key}",
                type="primary" if is_active else "secondary",
                use_container_width=True,
            ):
                st.session_state.active_tab = tab_key
                st.rerun()

# ---------------------------------------------------------------------------
# Main Content: dispatch to the active tab's render function
# ---------------------------------------------------------------------------

active_tab = st.session_state.active_tab
if active_tab == "detect":
    render_detect_tab(sp)
elif active_tab == "history":
    render_history_tab()
elif active_tab == "playlists":
    render_playlists_tab()
elif active_tab == "settings":
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
