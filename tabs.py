"""Render functions for each main-app tab."""

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

import auth
from functions import (
    detect_face,
    play_song,
    EMOTION_EMOJIS,
    EMOTION_LABELS,
    PLAYLIST_MAP,
)

# Color coding per emotion, used across detection results, history timeline
# and playlist cards for a consistent visual identity.
EMOTION_COLORS = {
    'aggressive': '#ef4444',
    'contempt':   '#f97316',
    'disgust':    '#22c55e',
    'fear':       '#8b5cf6',
    'happy':      '#eab308',
    'sad':        '#3b82f6',
    'surprise':   '#ec4899',
}


def render_detect_tab(sp):
    col_camera, col_result = st.columns([1.2, 1], gap="large")

    with col_camera:
        with st.container(border=True):
            st.markdown('<span class="card-marker"></span>', unsafe_allow_html=True)
            st.markdown('<h3>📷 Camera</h3>', unsafe_allow_html=True)
            img_file_buffer = st.camera_input(
                "Point your face at the camera and take a snapshot",
                label_visibility="collapsed",
            )

    face_img = None
    if img_file_buffer is not None:
        image = Image.open(img_file_buffer)
        frame = np.array(image)

        face_img, emotion, confidence = detect_face(frame)

        if emotion is not None:
            st.session_state.last_emotion = emotion
            st.session_state.last_confidence = confidence
            st.session_state.history.append(emotion)

            # Instantly play music based on the detected mood
            st.session_state.status = "playing"
            try:
                success, message = play_song(sp, emotion)
                st.session_state.play_message = message
                if not success:
                    st.session_state.status = "error"
            except Exception as e:
                st.session_state.status = "error"
                st.session_state.play_message = f"Failed to play: {str(e)}"
        else:
            st.session_state.last_emotion = None
            st.session_state.last_confidence = None

    with col_result:
        with st.container(border=True):
            st.markdown('<span class="card-marker"></span>', unsafe_allow_html=True)
            if st.session_state.last_emotion:
                emotion = st.session_state.last_emotion
                emoji = EMOTION_EMOJIS.get(emotion, '❓')
                color = EMOTION_COLORS.get(emotion, '#a855f7')
                conf = st.session_state.last_confidence.get(emotion, 0) if st.session_state.last_confidence else 0

                st.markdown(f'''
                    <div class="emotion-display" style="color:{color};">
                        <span class="emotion-emoji">{emoji}</span>
                        <span class="emotion-label">{emotion}</span>
                        <p class="emotion-confidence">Confidence: {conf:.1%}</p>
                    </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown('''
                    <div class="emotion-display">
                        <span class="emotion-waiting-icon">🤔</span>
                        <span class="emotion-label" style="font-size:1.2rem; color:#94a3b8;">Waiting...</span>
                        <p class="emotion-confidence">Take a photo to detect your mood</p>
                    </div>
                ''', unsafe_allow_html=True)

        status = st.session_state.status
        badge_class, badge_text = {
            "waiting": ("status-waiting", "WAITING FOR INPUT"),
            "playing": ("status-playing", "PLAYING MUSIC"),
        }.get(status, ("status-error", "ERROR"))

        st.markdown(
            f'<div style="text-align:center; margin: 0.5rem 0;">'
            f'<span class="status-badge {badge_class}"><span class="dot"></span>{badge_text}</span>'
            f'</div>',
            unsafe_allow_html=True
        )

    if face_img is not None and st.session_state.last_emotion:
        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

        col_img, col_chart = st.columns([1, 1], gap="large")

        with col_img:
            with st.container(border=True):
                st.markdown('<span class="card-marker"></span>', unsafe_allow_html=True)
                st.markdown('<h3>🔍 Detected Face</h3>', unsafe_allow_html=True)
                st.image(face_img, use_container_width=True)

        with col_chart:
            with st.container(border=True):
                st.markdown('<span class="card-marker"></span>', unsafe_allow_html=True)
                st.markdown('<h3>📊 Emotion Probabilities</h3>', unsafe_allow_html=True)

                if st.session_state.last_confidence:
                    sorted_conf = sorted(
                        st.session_state.last_confidence.items(),
                        key=lambda x: x[1],
                        reverse=True
                    )

                    bars_html = []
                    for emo, prob in sorted_conf:
                        emoji = EMOTION_EMOJIS.get(emo, '❓')
                        color = EMOTION_COLORS.get(emo, '#a855f7')
                        width = max(prob * 100, 2)
                        bars_html.append(
                            f'<div class="conf-bar-container">'
                            f'<div class="conf-bar-label">'
                            f'<span>{emoji} {emo.capitalize()}</span>'
                            f'<span class="val">{prob:.1%}</span>'
                            f'</div>'
                            f'<div class="conf-bar-bg">'
                            f'<div class="conf-bar-fill" style="width:{width}%; background:{color}; color:{color};"></div>'
                            f'</div>'
                            f'</div>'
                        )
                    st.markdown(''.join(bars_html), unsafe_allow_html=True)

    if st.session_state.status == "playing" and st.session_state.play_message:
        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
        st.markdown(f'''
            <div class="now-playing">
                <span class="np-icon">🎵</span>
                <div>
                    <p class="np-text">{st.session_state.play_message}</p>
                    <p class="np-mood">Enjoy your mood-matched music!</p>
                </div>
            </div>
        ''', unsafe_allow_html=True)
        st.balloons()
    elif st.session_state.status == "error" and st.session_state.play_message:
        st.error(st.session_state.play_message)


def render_history_tab():
    if not st.session_state.history:
        with st.container(border=True):
            st.markdown('<span class="card-marker"></span>', unsafe_allow_html=True)
            st.markdown('<h3>📊 Session Emotion History</h3>', unsafe_allow_html=True)
            st.markdown(
                '<p style="color:#94a3b8;">No detections yet this session — head to the Detect tab.</p>',
                unsafe_allow_html=True,
            )
        return

    history = st.session_state.history
    counts = pd.Series(history).value_counts()
    total = len(history)
    top_mood = counts.idxmax()
    top_emoji = EMOTION_EMOJIS.get(top_mood, '❓')
    unique_moods = counts.shape[0]

    st.markdown(f'''
        <div class="stat-row">
            <div class="stat-tile">
                <span class="stat-emoji">🧾</span>
                <div class="stat-value">{total}</div>
                <div class="stat-label">Detections</div>
            </div>
            <div class="stat-tile">
                <span class="stat-emoji">{top_emoji}</span>
                <div class="stat-value" style="text-transform:capitalize;">{top_mood}</div>
                <div class="stat-label">Top Mood</div>
            </div>
            <div class="stat-tile">
                <span class="stat-emoji">🎭</span>
                <div class="stat-value">{unique_moods}</div>
                <div class="stat-label">Unique Moods</div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<span class="card-marker"></span>', unsafe_allow_html=True)
        st.markdown('<h3>📊 Mood Distribution</h3>', unsafe_allow_html=True)
        st.bar_chart(counts)

    with st.container(border=True):
        st.markdown('<span class="card-marker"></span>', unsafe_allow_html=True)
        st.markdown('<h3>🕓 Recent Detections</h3>', unsafe_allow_html=True)
        recent = list(reversed(history[-20:]))
        n = len(history)
        items_html = []
        for i, entry in enumerate(recent):
            emoji = EMOTION_EMOJIS.get(entry, '❓')
            color = EMOTION_COLORS.get(entry, '#a855f7')
            idx = n - i
            items_html.append(
                f'<div class="timeline-item" style="color:{color};">'
                f'<span class="ti-emoji">{emoji}</span>'
                f'<span class="ti-label">{entry}</span>'
                f'<span class="ti-index">#{idx}</span>'
                f'</div>'
            )
        st.markdown(f'<div class="timeline">{"".join(items_html)}</div>', unsafe_allow_html=True)


def render_playlists_tab():
    with st.container(border=True):
        st.markdown('<span class="card-marker"></span>', unsafe_allow_html=True)
        st.markdown('<h3>🎵 Mood Playlists</h3>', unsafe_allow_html=True)

        cards_html = []
        for emotion, emoji in EMOTION_EMOJIS.items():
            playlist_id = PLAYLIST_MAP.get(emotion, '')
            color = EMOTION_COLORS.get(emotion, '#a855f7')
            cards_html.append(
                f'<a class="playlist-card" style="color:{color};" '
                f'href="https://open.spotify.com/playlist/{playlist_id}" target="_blank">'
                f'<div class="pl-art">{emoji}</div>'
                f'<div class="pl-name">{emotion}</div>'
                f'<div class="pl-sub">Spotify Playlist</div>'
                f'<div class="pl-play">▶</div>'
                f'</a>'
            )
        st.markdown(f'<div class="playlist-grid">{"".join(cards_html)}</div>', unsafe_allow_html=True)


def render_settings_tab(sp):
    with st.container(border=True):
        st.markdown('<span class="card-marker"></span>', unsafe_allow_html=True)
        st.markdown('<h3>🎧 Spotify Account</h3>', unsafe_allow_html=True)
        try:
            user = sp.current_user()
            images = user.get('images') or []
            avatar = images[0]['url'] if images else None
            if avatar:
                st.markdown(
                    f'<div class="user-badge"><img src="{avatar}"/>'
                    f'<div><div class="user-name">{user.get("display_name", "Spotify User")}</div>'
                    f'<div class="user-sub">● Connected</div></div></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(f"Signed in as **{user.get('display_name', 'Spotify User')}**")
        except Exception as e:
            st.warning(f"Could not load account info: {e}")

        if st.button("🚪 Sign Out"):
            auth.sign_out()
            st.rerun()

    with st.container(border=True):
        st.markdown('<span class="card-marker"></span>', unsafe_allow_html=True)
        st.markdown('<h3>🔄 Session</h3>', unsafe_allow_html=True)
        if st.button("Reset Session"):
            st.session_state.last_emotion = None
            st.session_state.last_confidence = None
            st.session_state.status = "waiting"
            st.session_state.play_message = ""
            st.session_state.history = []
            st.rerun()
