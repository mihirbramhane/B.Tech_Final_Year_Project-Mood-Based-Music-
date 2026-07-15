"""Render functions for each main-app tab."""

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

import auth
from functions import (
    detect_face,
    play_song,
    has_consecutive_repeats,
    EMOTION_EMOJIS,
    EMOTION_LABELS,
    PLAYLIST_MAP,
)


def render_detect_tab(sp):
    col_camera, col_result = st.columns([1.2, 1], gap="large")

    with col_camera:
        st.markdown('<div class="glass-card"><h3>📷 Camera</h3>', unsafe_allow_html=True)
        img_file_buffer = st.camera_input(
            "Point your face at the camera and take a snapshot",
            label_visibility="collapsed",
        )
        st.markdown('</div>', unsafe_allow_html=True)

    face_img = None
    if img_file_buffer is not None:
        image = Image.open(img_file_buffer)
        frame = np.array(image)

        face_img, emotion, confidence = detect_face(frame)

        if emotion is not None:
            st.session_state.last_emotion = emotion
            st.session_state.last_confidence = confidence
            st.session_state.status = "detecting"
            st.session_state.emotions.append(emotion)
            st.session_state.history.append(emotion)

            if len(st.session_state.emotions) >= 2 and st.session_state.emotions[-1] == st.session_state.emotions[-2]:
                st.session_state.detection_count += 1
            else:
                st.session_state.detection_count = 1

            threshold = st.session_state.detection_threshold
            reached, final_emotion = has_consecutive_repeats(st.session_state.emotions, threshold)
            if reached and final_emotion is not None:
                st.session_state.status = "playing"
                try:
                    success, message = play_song(sp, final_emotion)
                    st.session_state.play_message = message
                    if not success:
                        st.session_state.status = "error"
                except Exception as e:
                    st.session_state.status = "error"
                    st.session_state.play_message = f"Failed to play: {str(e)}"
                st.session_state.emotions = []
                st.session_state.detection_count = 0
        else:
            st.session_state.last_emotion = None
            st.session_state.last_confidence = None
            st.session_state.detection_count = 0

    with col_result:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        if st.session_state.last_emotion:
            emotion = st.session_state.last_emotion
            emoji = EMOTION_EMOJIS.get(emotion, '❓')
            conf = st.session_state.last_confidence.get(emotion, 0) if st.session_state.last_confidence else 0

            st.markdown(f'''
                <div class="emotion-display">
                    <span class="emotion-emoji">{emoji}</span>
                    <span class="emotion-label">{emotion}</span>
                    <p class="emotion-confidence">Confidence: {conf:.1%}</p>
                </div>
            ''', unsafe_allow_html=True)

            threshold = st.session_state.detection_threshold
            progress = min(st.session_state.detection_count / threshold, 1.0)
            progress_pct = int(progress * 100)
            st.markdown(f'''
                <p style="color:#94a3b8; font-size:0.85rem; margin-bottom:0.3rem;">
                    🎯 Detection Progress
                </p>
                <div class="progress-container">
                    <div class="progress-fill" style="width:{progress_pct}%;"></div>
                    <span class="progress-text">
                        {st.session_state.detection_count} / {threshold} consecutive
                    </span>
                </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown('''
                <div class="emotion-display">
                    <span class="emotion-emoji">🤔</span>
                    <span class="emotion-label" style="font-size:1.2rem;">Waiting...</span>
                    <p class="emotion-confidence">Take a photo to detect your mood</p>
                </div>
            ''', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        status = st.session_state.status
        badge_class, badge_text = {
            "waiting": ("status-waiting", "⏳ WAITING FOR INPUT"),
            "detecting": ("status-detecting", "🔍 DETECTING EMOTION"),
            "playing": ("status-playing", "🎵 PLAYING MUSIC"),
        }.get(status, ("status-error", "⚠️ ERROR"))

        st.markdown(
            f'<div style="text-align:center; margin: 0.5rem 0;">'
            f'<span class="status-badge {badge_class}">{badge_text}</span>'
            f'</div>',
            unsafe_allow_html=True
        )

    if face_img is not None and st.session_state.last_emotion:
        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

        col_img, col_chart = st.columns([1, 1], gap="large")

        with col_img:
            st.markdown('<div class="glass-card"><h3>🔍 Detected Face</h3>', unsafe_allow_html=True)
            st.image(face_img, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_chart:
            st.markdown('<div class="glass-card"><h3>📊 Emotion Probabilities</h3>', unsafe_allow_html=True)

            if st.session_state.last_confidence:
                sorted_conf = sorted(
                    st.session_state.last_confidence.items(),
                    key=lambda x: x[1],
                    reverse=True
                )
                colors = ["#a855f7", "#6366f1", "#06b6d4", "#22c55e", "#eab308", "#f97316", "#ef4444"]

                for i, (emo, prob) in enumerate(sorted_conf):
                    emoji = EMOTION_EMOJIS.get(emo, '❓')
                    color = colors[i % len(colors)]
                    width = max(prob * 100, 2)
                    st.markdown(f'''
                        <div class="conf-bar-container">
                            <div class="conf-bar-label">
                                <span>{emoji} {emo.capitalize()}</span>
                                <span>{prob:.1%}</span>
                            </div>
                            <div class="conf-bar-bg">
                                <div class="conf-bar-fill" style="width:{width}%; background:{color};"></div>
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

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
    st.markdown('<div class="glass-card"><h3>📊 Session Emotion History</h3>', unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown(
            '<p style="color:#94a3b8;">No detections yet this session — head to the Detect tab.</p>',
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)
        return

    counts = pd.Series(st.session_state.history).value_counts()
    st.bar_chart(counts)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card"><h3>🕓 Recent Detections</h3>', unsafe_allow_html=True)
    for entry in reversed(st.session_state.history[-20:]):
        emoji = EMOTION_EMOJIS.get(entry, '❓')
        st.markdown(f"{emoji} {entry.capitalize()}")
    st.markdown('</div>', unsafe_allow_html=True)


def render_playlists_tab():
    st.markdown('<div class="glass-card"><h3>🎵 Mood Playlists</h3>', unsafe_allow_html=True)
    for emotion, emoji in EMOTION_EMOJIS.items():
        playlist_id = PLAYLIST_MAP.get(emotion, '')
        st.markdown(
            f'<div class="playlist-item">'
            f'<span>{emoji}</span>'
            f'<span>{emotion.capitalize()}</span>'
            f'<a href="https://open.spotify.com/playlist/{playlist_id}" target="_blank" '
            f'style="margin-left:auto; color:#a855f7; text-decoration:none; font-size:0.85rem;">Open ↗</a>'
            f'</div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)


def render_settings_tab(sp):
    st.markdown('<div class="glass-card"><h3>🎯 Detection</h3>', unsafe_allow_html=True)
    st.session_state.detection_threshold = st.slider(
        "Detection Threshold",
        min_value=2, max_value=30, value=st.session_state.detection_threshold,
        help="Number of consecutive same-emotion detections required before playing a song.",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card"><h3>🎧 Spotify Account</h3>', unsafe_allow_html=True)
    try:
        user = sp.current_user()
        images = user.get('images') or []
        avatar = images[0]['url'] if images else None
        if avatar:
            st.markdown(
                f'<div class="user-badge"><img src="{avatar}"/>'
                f'<div><div class="user-name">{user.get("display_name", "Spotify User")}</div>'
                f'<div class="user-sub">Connected</div></div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(f"Signed in as **{user.get('display_name', 'Spotify User')}**")
    except Exception as e:
        st.warning(f"Could not load account info: {e}")

    if st.button("🚪 Sign Out"):
        auth.sign_out()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card"><h3>🔄 Session</h3>', unsafe_allow_html=True)
    if st.button("Reset Session"):
        st.session_state.emotions = []
        st.session_state.last_emotion = None
        st.session_state.last_confidence = None
        st.session_state.status = "waiting"
        st.session_state.play_message = ""
        st.session_state.detection_count = 0
        st.session_state.history = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
