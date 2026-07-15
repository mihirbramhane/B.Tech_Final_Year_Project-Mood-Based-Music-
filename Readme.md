# 🎧 Mood-Based Music Player

> **AI-powered emotion detection that reads your face and plays the perfect Spotify playlist.**

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13+-FF6F00?style=flat-square&logo=tensorflow&logoColor=white)
![Spotify](https://img.shields.io/badge/Spotify_API-1ED760?style=flat-square&logo=spotify&logoColor=white)

---

## 💡 Features

- 🔐 **In-App Spotify Sign-In** — Each visitor connects their own Spotify account via OAuth, right in the browser (no terminal step, no shared login)
- 👥 **Multi-User Ready** — Every visitor's session and Spotify token are isolated, so the app can be deployed publicly for anyone to use
- 🎭 **7 Emotion Detection** — Detects Happy, Sad, Aggressive, Surprise, Disgust, Fear, and Contempt
- 🎵 **Auto-Play Playlists** — Automatically plays a curated Spotify playlist matching your mood
- 📷 **Webcam Integration** — Real-time camera input via Streamlit's camera widget
- 📊 **Confidence Visualization** — See emotion probabilities as animated bar charts
- 🎯 **Streak Detection** — Configurable consecutive detection threshold before triggering playback
- 🗂️ **Tabbed Navigation** — Detect / History / Playlists / Settings, each its own tab
- 🌙 **Dark Glassmorphism UI** — Stunning dark theme with gradient accents and animations
- 📱 **Responsive Layout** — Works across different screen sizes

---

## 🚀 How It Works

```
📷 Camera Snapshot → 🔍 Face Detection (Haar Cascade) → 🧠 CNN Emotion Model → 🎯 Streak Check → 🎵 Spotify
```

1. **Capture** — Take a photo using the in-browser camera
2. **Detect** — Haar Cascade finds your face, crops and resizes it to 128×128
3. **Classify** — A pre-trained Keras CNN predicts your emotion across 7 classes
4. **Accumulate** — The app tracks consecutive same-emotion detections
5. **Play** — Once the threshold is met, Spotify opens and plays a mood-matched playlist

---

## 🎭 Emotions & Playlists

| Emotion | Emoji | Playlist Style |
|---------|-------|---------------|
| Happy | 😊 | Energetic / Upbeat Songs |
| Sad | 😢 | Emotional / Melodic Songs |
| Aggressive | 😠 | Hardcore / Rock |
| Fear | 😨 | Calming / Ambient |
| Surprise | 😲 | Random Mix |
| Disgust | 🤢 | Chill Vibes |
| Contempt | 😒 | Lo-fi Beats |

---

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| **Python 3.9+** | Core language |
| **Streamlit** | Web UI framework |
| **OpenCV** | Webcam capture & face detection (Haar Cascade) |
| **TensorFlow / Keras** | Deep learning emotion classification model |
| **Spotipy** | Spotify Web API client |
| **Pillow** | Image processing |
| **python-dotenv** | Secure credential management |

---

## 🖥️ Local Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/emotion-music-player.git
cd emotion-music-player
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Spotify API

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Copy your **Client ID** and **Client Secret**
4. Add `http://localhost:8501` as a Redirect URI (this must exactly match what you put in `.env`/secrets below)
5. Copy `.env.example` to `.env` and fill in your values:

```env
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:8501
```

### 4. Run the App

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`. Click **Connect with Spotify** on the sign-in screen — no separate script to run anymore.

---

## ☁️ Deploying Publicly

Since each visitor authenticates with their own Spotify account in their own browser session, this app is safe to deploy for multiple simultaneous users (e.g. on [Streamlit Community Cloud](https://streamlit.io/cloud)):

1. Push this repo to GitHub (the real `.env` / `.streamlit/secrets.toml` stay out of it — they're git-ignored).
2. Create a new Streamlit Cloud app pointing at `app.py`.
3. In the app's **Settings → Secrets**, paste the contents of `.streamlit/secrets.toml.example` filled in with your real `SPOTIFY_CLIENT_ID` / `SPOTIFY_CLIENT_SECRET`, and set `SPOTIFY_REDIRECT_URI` to your deployed app's HTTPS URL (e.g. `https://your-app.streamlit.app`).
4. Add that same HTTPS URL as a Redirect URI on the Spotify Developer Dashboard app (you can have both the localhost one and the deployed one registered at once).
5. Anyone who visits the deployed URL gets their own sign-in and Spotify session — nothing is shared between visitors.

Each visitor still needs their **own** Spotify Premium account and an active Spotify device (phone/desktop/web player) open for playback to start — that's a Spotify API requirement, not something this app can work around.

---

## 📁 Project Structure

```
Emotion_song_Final_GUI/
├── app.py                              # Streamlit entry point (sign-in gate + tab routing)
├── auth.py                             # Per-session Spotify OAuth (sign-in, token refresh, sign-out)
├── tabs.py                             # Detect / History / Playlists / Settings tab renderers
├── styles.py                           # Shared CSS (glassmorphism theme + sign-in screen)
├── functions.py                        # Core logic (face/emotion detection, Spotify playback actions)
├── emotion_model_1.h5                  # Pre-trained Keras CNN model (~22MB)
├── haarcascade_frontalface_default.xml  # OpenCV face detection cascade
├── GUI.py                              # Legacy Tkinter GUI (reference)
├── requirements.txt                    # Python dependencies
├── .env.example                        # Template for local Spotify credentials
├── .streamlit/secrets.toml.example     # Template for Streamlit Cloud secrets
├── .env                                # Your local Spotify credentials (not committed)
├── .gitignore                          # Git ignore rules
└── Readme.md                           # This file
```

---

## ⚠️ Requirements

- **Python 3.9+**
- **Spotify Premium** account (required for playback control)
- **Spotify Desktop App** installed and logged in
- **Webcam** access in your browser

---

## 📝 Notes

- The Tkinter GUI (`GUI.py`) is kept as a legacy reference. The primary interface is the Streamlit app.
- Each visitor signs in with their own Spotify account; the token lives only in their browser session (`st.session_state`), never on disk — safe for multiple concurrent users.
- The emotion model expects 128×128 RGB face images and outputs 7-class probabilities.
- The detection threshold (default: 5 consecutive same-emotion frames) can be adjusted on the Settings tab.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

<p align="center">
  Built with ❤️ using Python, TensorFlow, and the Spotify API
</p>
