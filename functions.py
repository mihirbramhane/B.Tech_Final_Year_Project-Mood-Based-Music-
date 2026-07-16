"""
Core functions for Emotion-Based Music Player.
Handles face detection, emotion classification, and Spotify playback.
"""

import os
import logging

import cv2
import numpy as np
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Load environment variables from .env file (local dev only; deployed
# instances use st.secrets — see auth.py)
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Emotion-to-Spotify playlist mapping
PLAYLIST_MAP = {
    'aggressive': '0N7bTAuO8ejUjW2YkyZfRB',
    'happy':      '4nd7oGDNgfM0rv28CQw9WQ',
    'sad':        '2sOMIgioNPngXojcOuR4tn',
    'contempt':   '0pXAFx2awezHXQ1ZsczR6L',
    'fear':       '7HB0Ko1WWxBf1X4U34MOkA',
    'surprise':   '7vatYrf39uVaZ8G2cVtEik',
    'disgust':    '1oGsi9NfPN67JasT5S8wgI',
}

# Emotion index labels (must match model training order)
EMOTION_LABELS = {
    0: 'aggressive',
    1: 'contempt',
    2: 'disgust',
    3: 'fear',
    4: 'happy',
    5: 'sad',
    6: 'surprise',
}

# Emoji mapping for UI
EMOTION_EMOJIS = {
    'aggressive': '😠',
    'contempt':   '😒',
    'disgust':    '🤢',
    'fear':       '😨',
    'happy':      '😊',
    'sad':        '😢',
    'surprise':   '😲',
}

# Resolve file paths relative to this script's directory
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_MODEL_PATH = os.path.join(_BASE_DIR, 'emotion_model_1.h5')
_CASCADE_PATH = os.path.join(_BASE_DIR, 'haarcascade_frontalface_default.xml')

# ---------------------------------------------------------------------------
# Model & Cascade Loading
# ---------------------------------------------------------------------------

_model = None
_face_cascade = None


def load_emotion_model():
    """Load the Keras emotion classification model (cached singleton)."""
    global _model
    if _model is None:
        try:
            from tensorflow.keras.models import load_model
            logger.info("Loading emotion model from %s ...", _MODEL_PATH)
            _model = load_model(_MODEL_PATH)
            logger.info("Emotion model loaded successfully.")
        except Exception as e:
            logger.error("Failed to load emotion model: %s", e)
            raise
    return _model


def load_face_cascade():
    """Load the Haar Cascade face detector (cached singleton)."""
    global _face_cascade
    if _face_cascade is None:
        # Try the bundled XML first, then fall back to OpenCV's built-in data
        candidates = [
            _CASCADE_PATH,
            os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml'),
        ]
        for path in candidates:
            if os.path.isfile(path):
                _face_cascade = cv2.CascadeClassifier(path)
                if not _face_cascade.empty():
                    logger.info("Haar Cascade loaded from %s", path)
                    return _face_cascade
                _face_cascade = None  # reset if it loaded but was empty

        raise FileNotFoundError(
            f"Haar Cascade not found. Tried: {candidates}"
        )
    return _face_cascade


# ---------------------------------------------------------------------------
# Face Detection & Emotion Classification
# ---------------------------------------------------------------------------

def detect_face(img):
    """
    Detect faces in the image and classify the dominant emotion.

    Args:
        img: RGB numpy array (H, W, 3)

    Returns:
        tuple: (annotated_image, emotion_label_or_None, confidence_scores_or_None)
               - annotated_image has rectangles and labels drawn on detected faces
               - emotion_label is a string like 'happy', or None if no face found
               - confidence_scores is a dict {emotion: probability} or None
    """
    model = load_emotion_model()
    face_cascade = load_face_cascade()

    face_img = img.copy()
    gray = cv2.cvtColor(face_img, cv2.COLOR_RGB2GRAY)

    face_rects = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,          # Increased from 1 to reduce false positives
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )

    if len(face_rects) == 0:
        return face_img, None, None

    # Use the first detected face for classification
    # NOTE: Haar Cascade returns (x, y, w, h) — NOT (x, y, h, w)
    x, y, w, h = face_rects[0]
    face = img[y:y + h, x:x + w]

    try:
        face_resized = cv2.resize(face, (128, 128))
        face_normalized = face_resized.astype('float32') / 255.0
        face_normalized = face_normalized.reshape(1, 128, 128, 3)
        predictions = model.predict(face_normalized, verbose=0)
        idx = predictions[0].argmax()
        emotion_label = EMOTION_LABELS[idx]

        # Build confidence dict
        confidence = {EMOTION_LABELS[i]: float(predictions[0][i]) for i in range(len(EMOTION_LABELS))}

    except Exception as e:
        logger.error("Emotion prediction failed: %s", e)
        return face_img, None, None

    # Draw rectangles and labels on ALL detected faces
    for (fx, fy, fw, fh) in face_rects:
        # Rectangle
        cv2.rectangle(face_img, (fx, fy), (fx + fw, fy + fh), (0, 255, 128), 2)
        # Label background
        label_text = f"{emotion_label} ({confidence[emotion_label]:.0%})"
        (text_w, text_h), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        cv2.rectangle(face_img, (fx, fy - text_h - 10), (fx + text_w + 6, fy), (0, 255, 128), -1)
        cv2.putText(face_img, label_text, (fx + 3, fy - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    return face_img, emotion_label, confidence


# ---------------------------------------------------------------------------
# Spotify Integration
#
# Authentication itself (OAuth sign-in, per-session token, refresh) lives in
# auth.py. Everything here operates on an already-authenticated `sp` client
# handed in by the caller (auth.get_spotify_client()).
# ---------------------------------------------------------------------------

def get_active_device(sp):
    """
    Find the first active Spotify device, or the first available one.

    Returns:
        str: device ID, or None if no devices found
    """
    try:
        devices = sp.devices()
        device_list = devices.get('devices', [])

        if not device_list:
            logger.warning("No Spotify devices found. Is Spotify open?")
            return None

        # Prefer the currently active device
        for device in device_list:
            if device.get('is_active'):
                logger.info("Using active device: %s (%s)", device['name'], device['id'])
                return device['id']

        # Fall back to the first available device
        first = device_list[0]
        logger.info("Using first available device: %s (%s)", first['name'], first['id'])
        return first['id']

    except Exception as e:
        logger.error("Failed to fetch Spotify devices: %s", e)
        return None


def play_song(sp, mood):
    """
    Play a Spotify playlist matching the given mood.

    Args:
        sp: authenticated spotipy.Spotify client for the current user
            (see auth.get_spotify_client())
        mood: emotion string (e.g., 'happy', 'sad', 'aggressive')

    Returns:
        tuple: (success: bool, message: str)
    """
    import time
    import streamlit as st

    if mood not in PLAYLIST_MAP:
        return False, f"Unknown mood: '{mood}'. Valid moods: {list(PLAYLIST_MAP.keys())}"

    if sp is None:
        return False, "Spotify not connected! Sign in with Spotify first."

    # Cooldown: prevent rapid API calls (15 seconds between plays)
    last_play_time = st.session_state.get("_last_play_time", 0)
    elapsed = time.time() - last_play_time
    cooldown = 15  # seconds

    if elapsed < cooldown:
        remaining = int(cooldown - elapsed)
        return True, (
            f"Already playing {EMOTION_EMOJIS.get(st.session_state.get('_last_play_mood', mood), '🎵')} "
            f"{st.session_state.get('_last_play_mood', mood)} playlist! "
            f"Take another snapshot in {remaining}s to change mood."
        )

    try:
        device_id = get_active_device(sp)

        if not device_id:
            return False, (
                "No Spotify device found. Open Spotify on your phone, desktop app, "
                "or web player, then try again."
            )

        # Start the playlist (transfer_playback first, then start)
        playlist_uri = f'spotify:playlist:{PLAYLIST_MAP[mood]}'

        try:
            sp.transfer_playback(device_id, force_play=True)
        except Exception:
            pass  # transfer may fail if already on that device, that's fine

        import time as _time
        _time.sleep(0.3)  # brief pause between API calls

        sp.start_playback(device_id=device_id, context_uri=playlist_uri)

        # Record cooldown timestamp
        st.session_state["_last_play_time"] = time.time()
        st.session_state["_last_play_mood"] = mood

        logger.info("Now playing '%s' playlist on device %s", mood, device_id)
        return True, f"Playing {EMOTION_EMOJIS.get(mood, '🎵')} {mood} playlist!"

    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "Too Many" in error_msg.lower() or "Max Retries" in error_msg:
            logger.warning("Spotify rate limited: %s", e)
            return False, (
                "⏳ Spotify rate limited — too many requests. "
                "Please wait 30 seconds before trying again."
            )
        logger.error("Spotify playback failed: %s", e)
        return False, f"Spotify error: {error_msg}"


# ---------------------------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------------------------

def has_consecutive_repeats(elements, target_count=25):
    """
    Check if the list contains `target_count` consecutive identical elements.

    Args:
        elements: list of emotion labels
        target_count: number of consecutive repeats required

    Returns:
        tuple: (found: bool, element: str or None)
    """
    if not elements:
        return False, None  # Fixed: was returning just `False`

    current_element = elements[0]
    count = 1

    for element in elements[1:]:
        if element is None:
            # Skip None entries (no face detected frames)
            current_element = None
            count = 0
            continue

        if element == current_element:
            count += 1
            if count >= target_count:
                return True, element
        else:
            current_element = element
            count = 1

    return False, None