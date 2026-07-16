# 🎧 Mood-Based Music Player

> **AI-Powered Emotion Detection → Instant Mood-Matched Spotify Playback**

A B.Tech Final Year Project that reads your facial emotion in real-time using a custom-trained CNN and instantly plays a Spotify playlist that matches your mood. No manual selection, no searching — just look at the camera and let AI curate your soundtrack. 🎵✨

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white" alt="Python 3.11"/>
  <img src="https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/TensorFlow-Keras-FF6F00?logo=tensorflow&logoColor=white" alt="TensorFlow"/>
  <img src="https://img.shields.io/badge/Spotify-API-1DB954?logo=spotify&logoColor=white" alt="Spotify"/>
  <img src="https://img.shields.io/badge/OpenCV-Haar%20Cascade-5C3EE8?logo=opencv&logoColor=white" alt="OpenCV"/>
  <img src="https://img.shields.io/badge/Deployed-Streamlit%20Cloud-success" alt="Deployed"/>
</p>

---

## 📖 Table of Contents

- [🌟 Overview](#-overview)
- [🎬 Demo](#-demo)
- [⚙️ How It Works](#️-how-it-works)
- [🛠️ Tech Stack](#️-tech-stack)
- [📁 Project Structure](#-project-structure)
- [😃 Supported Emotions](#-supported-emotions)
- [🚀 Getting Started](#-getting-started)
- [🔐 Spotify API Setup](#-spotify-api-setup)
- [☁️ Deployment](#️-deployment)
- [🎨 UI/UX Design](#-uiux-design)
- [🐛 Known Gotchas & Troubleshooting](#-known-gotchas--troubleshooting)
- [🗺️ Roadmap](#️-roadmap)
- [🙌 Contributing](#-contributing)
- [📄 License](#-license)
- [🙏 Acknowledgements](#-acknowledgements)

---

## 🌟 Overview

**Mood-Based Music Player** is a real-time facial emotion recognition web app that bridges computer vision and music streaming. Using a webcam snapshot, a trained CNN classifies your facial expression into one of **7 emotion categories**, and the app instantly triggers playback of a hand-curated Spotify playlist matching that mood — right inside your Spotify account.

Built as a full end-to-end AI product: **face detection → deep learning inference → OAuth-secured API integration → polished UI**, all wrapped in a single Streamlit application.

---

## 🎬 Demo

> 📸 *Take a photo → 🧠 AI detects your emotion → 🎶 Matching playlist plays instantly on Spotify*

| Step | Action |
|------|--------|
| 1️⃣ | Connect your Spotify account (secure OAuth, per-session) |
| 2️⃣ | Take a photo via webcam |
| 3️⃣ | CNN model classifies your facial emotion |
| 4️⃣ | App instantly plays a matching playlist on your connected Spotify device |
| 5️⃣ | View your emotion history, playlists, and session stats in-app |

---

## ⚙️ How It Works

```
📷 Webcam Capture
      ↓
🔍 OpenCV Haar Cascade → Face Detection
      ↓
🧠 TensorFlow/Keras CNN (128x128x3 input) → 7-Class Emotion Softmax
      ↓
🎯 Instant Classification (no consecutive-detection threshold — single-shot)
      ↓
🎵 Spotipy → Spotify Web API (OAuth) → Playlist Playback
      ↓
✅ Music plays on your active Spotify device
```

The detection pipeline is intentionally **instant** — one detected emotion immediately triggers playback, prioritizing responsiveness over multi-frame smoothing.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| 🖥️ **Frontend / UI** | [Streamlit](https://streamlit.io/) |
| 🧠 **Deep Learning** | TensorFlow / Keras (CNN, 128×128×3 → 7-class softmax) |
| 👁️ **Face Detection** | OpenCV Haar Cascade Classifier |
| 🎵 **Music Integration** | Spotipy (Spotify Web API, OAuth 2.0) |
| 🐍 **Language** | Python 3.11 (pinned — TensorFlow doesn't support 3.13+/3.14) |
| ☁️ **Deployment** | Streamlit Community Cloud |
| 🎨 **Styling** | Custom CSS — Glassmorphism, animated aurora gradients |
| 🔤 **Fonts** | Outfit (headings) + Inter (body) |

---

## 📁 Project Structure

```
B.Tech_Final_Year_Project-Mood-Based-Music-/
│
├── app.py                          # 🚪 Entry point — page config, session state,
│                                    #    Spotify OAuth gate, sidebar, tabs, footer
│
├── auth.py                         # 🔐 Spotify OAuth handling (per-session tokens)
│                                    #    ⚠️ Do not modify unless explicitly required
│
├── functions.py                    # ⚙️ Core logic — face detection, emotion
│                                    #    classification, Spotify playback,
│                                    #    EMOTION_EMOJIS / EMOTION_LABELS / PLAYLIST_MAP
│                                    #    ⚠️ Do not modify unless explicitly required
│
├── tabs.py                         # 🗂️ Renders 4 tabs: Detect, History,
│                                    #    Playlists, Settings + EMOTION_COLORS (UI)
│
├── styles.py                       # 🎨 All CSS as one injected string
│                                    #    (glassmorphism, gradients, animations)
│
├── GUI.py                          # 🗄️ Legacy Tkinter GUI — unused, never touch
│
├── emotion_model_1.h5              # 🧠 Trained CNN model weights
├── haarcascade_frontalface_default.xml   # 👁️ OpenCV face detection cascade
│
├── .python-version                 # 📌 Pinned to Python 3.11
└── requirements.txt                # 📦 Python dependencies
```

---

## 😃 Supported Emotions

The CNN classifies faces into **7 emotion categories**, each mapped to a distinct Spotify playlist:

| Emotion | Emoji |
|---------|-------|
| Happy | 😄 |
| Sad | 😢 |
| Aggressive | 😠 |
| Fear | 😨 |
| Disgust | 🤢 |
| Contempt | 😒 |
| Surprise | 😮 |

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python **3.11** (strictly — TensorFlow does not support 3.13+/3.14)
- A [Spotify Developer](https://developer.spotify.com/dashboard) account & app credentials
- A webcam-enabled device

### 📦 Installation

```bash
# 1️⃣ Clone the repository
git clone https://github.com/mihirbramhane/B.Tech_Final_Year_Project-Mood-Based-Music-.git
cd B.Tech_Final_Year_Project-Mood-Based-Music-

# 2️⃣ Ensure Python 3.11 is active
python --version

# 3️⃣ Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 4️⃣ Install dependencies
pip install -r requirements.txt

# 5️⃣ Run the app
streamlit run app.py
```

The app will open automatically at `http://localhost:8501` 🎉

---

## 🔐 Spotify API Setup

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and create a new app.
2. Set the **Redirect URI** to match your local/deployed app URL (this must match *exactly*, including trailing slashes).
3. Copy your **Client ID** and **Client Secret**.
4. Add them as environment variables / Streamlit secrets:

```toml
# .streamlit/secrets.toml
SPOTIFY_CLIENT_ID = "your_client_id_here"
SPOTIFY_CLIENT_SECRET = "your_client_secret_here"
SPOTIFY_REDIRECT_URI = "http://localhost:8501"
```

> ⚠️ **Note:** OAuth is handled **per-session** in `auth.py` — no shared tokens across users. Most "auth failures" trace back to **dashboard redirect URI mismatches**, not app code.

---

## ☁️ Deployment

Deployed on **Streamlit Community Cloud** — single deployment surface (deliberately, to avoid multi-platform deploy failures).

### Deployment Checklist ✅

- [ ] `.python-version` pinned to `3.11`
- [ ] `requirements.txt` up to date
- [ ] Spotify secrets configured in Streamlit Cloud's **Secrets** panel
- [ ] Redirect URI in Spotify Dashboard matches the deployed `*.streamlit.app` URL
- [ ] No unresolved git conflict markers in any `.py` file (see [Troubleshooting](#-known-gotchas--troubleshooting))
- [ ] `python -m py_compile app.py tabs.py styles.py` passes locally before pushing

---

## 🎨 UI/UX Design

The app features a **premium dark theme** built with hand-crafted CSS:

- 🌌 Glassmorphism cards with soft blur & translucency
- 🌈 Animated aurora gradient background
- 🔤 Outfit (headings) + Inter (body) typography pairing
- 🎵 Spotify-style playlist grid
- 🕐 Colored emotion timeline in History tab
- 💊 Pill-style tab navigation
- ✨ Glowing per-emotion accent colors

> 🛠️ **UI Contribution Rule:** Only `styles.py`, `tabs.py`, and `app.py` should be touched for UI/UX changes. Core logic files (`auth.py`, `functions.py`) and model assets are off-limits.

---

## 🐛 Known Gotchas & Troubleshooting

Hard-won lessons from building this in Streamlit — read before touching UI code 👇

<details>
<summary><b>1️⃣ st.markdown() calls do NOT nest</b></summary>

Each `st.markdown()` call is an isolated HTML fragment. Opening a `<div>` in one call and closing it in another produces a broken DOM.

**Fix:** Use `with st.container(border=True):` with a unique marker span as the first child, and scope CSS via:
```css
[data-testid="stVerticalBlockBorderWrapper"]:has(> div > div > div > div > div > p > span.card-marker)
```
The exact depth matters — a loose `:has(.card-marker)` will also match ancestor wrappers.
</details>

<details>
<summary><b>2️⃣ Raw heading tags break sibling content</b></summary>

`<h1>`–`<h6>` tags inside `st.markdown()` get converted into Streamlit's own heading widget, dropping any sibling content in that call. **Never** combine a marker span and a heading in one call — always split into two.
</details>

<details>
<summary><b>3️⃣ CSS custom properties get silently stripped</b></summary>

`style="--foo: bar;"` is silently removed by Streamlit's HTML sanitizer. Standard properties survive.

**Fix:** Use `style="color:{value};"` and reference it in CSS via `currentColor` instead of `var(--foo)`.
</details>

<details>
<summary><b>4️⃣ Multi-line f-strings break markdown parsing</b></summary>

Joining multi-line, indented triple-quoted f-strings creates blank-line gaps that CommonMark treats as indented code blocks — rendering literal HTML text instead of elements.

**Fix:** Build each fragment as a single-line string (no embedded `\n`) before joining.
</details>

<details>
<summary><b>5️⃣ Container testid collisions</b></summary>

`st.container(border=True)` and plain layout containers (columns, tab panels) share the same `data-testid="stVerticalBlockBorderWrapper"`, differing only by an unstable `st-emotion-cache-*` class. Use the marker+depth `:has()` technique instead of relying on that class.
</details>

<details>
<summary><b>6️⃣ Hot-reload is unreliable</b></summary>

Kill and fully restart `streamlit run` when testing — especially after editing an **imported module** (not just the entry script). Don't trust auto-rerun.
</details>

<details>
<summary><b>🔥 Git conflict markers breaking deployment</b></summary>

At one point, `tabs.py` was committed with **literal unresolved conflict markers** (`<<<<<<<`, `=======`, `>>>>>>>`), causing a `SyntaxError` on Streamlit Cloud.

**Fix — always run before pushing:**
```bash
grep -rn "^<<<<<<<\|^=======\|^>>>>>>>" *.py
```
If something inexplicably won't import, check this **before** assuming the bug is in your latest edit.
</details>

<details>
<summary><b>🧪 Testing UI without live Spotify OAuth</b></summary>

Since OAuth needs live credentials, build a **throwaway local harness script** that seeds fake `st.session_state` and calls `render_*` functions from `tabs.py` directly. Keep it in a scratch location — never commit it to the repo.
</details>

---

## 🗺️ Roadmap

- [ ] 📱 Redesigned mobile-native UI (bottom nav bar, sticky header, unified capture/result flow)
- [ ] 🎯 Consecutive-detection smoothing (optional toggle)
- [ ] 📊 Emotion analytics dashboard
- [ ] 🌍 Multi-language playlist support
- [ ] 🔊 Volume/mood intensity mapping
- [ ] 🧪 Model accuracy improvements / expanded training data

---

## 🙌 Contributing

This is currently a solo B.Tech final year project. Suggestions and feedback are welcome via GitHub Issues!

1. Fork the repo 🍴
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request 🚀

---

## 📄 License

This project is developed for academic purposes as part of a B.Tech Final Year Project.

---

## 🙏 Acknowledgements

- 🎵 [Spotify Web API](https://developer.spotify.com/documentation/web-api) & [Spotipy](https://spotipy.readthedocs.io/)
- 🧠 [TensorFlow](https://www.tensorflow.org/) / [Keras](https://keras.io/)
- 👁️ [OpenCV](https://opencv.org/) Haar Cascade Classifiers
- 🖥️ [Streamlit](https://streamlit.io/) Community Cloud
- ❤️ Built with passion for the B.Tech Final Year Project

---

<p align="center">
  Made with ❤️ using Streamlit, TensorFlow & Spotify API
</p>