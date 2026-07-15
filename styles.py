"""Shared CSS for the Mood Music Player Streamlit app."""

CSS = """
<style>
    /* ---- Import Google Font ---- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ---- Global ---- */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a2e 40%, #16213e 100%);
        font-family: 'Inter', sans-serif;
    }

    /* ---- Hide default Streamlit elements ---- */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ---- Hero Title ---- */
    .hero-title {
        text-align: center;
        padding: 1.5rem 0 0.5rem;
        background: linear-gradient(90deg, #a855f7, #6366f1, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -1px;
        animation: glow 3s ease-in-out infinite alternate;
    }

    @keyframes glow {
        from { filter: drop-shadow(0 0 6px rgba(168, 85, 247, 0.3)); }
        to   { filter: drop-shadow(0 0 20px rgba(99, 102, 241, 0.5)); }
    }

    .hero-subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1.05rem;
        font-weight: 400;
        margin-bottom: 1.5rem;
        letter-spacing: 0.3px;
    }

    /* ---- Glass Cards ---- */
    .glass-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        border-color: rgba(168, 85, 247, 0.3);
        box-shadow: 0 8px 32px rgba(168, 85, 247, 0.08);
    }

    .glass-card h3 {
        color: #e2e8f0;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0 0 0.8rem;
    }

    /* ---- Emotion Display ---- */
    .emotion-display {
        text-align: center;
        padding: 2rem 1rem;
    }

    .emotion-emoji {
        font-size: 5rem;
        display: block;
        margin-bottom: 0.5rem;
        animation: bounce 2s ease infinite;
    }

    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    .emotion-label {
        font-size: 1.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 3px;
        background: linear-gradient(90deg, #a855f7, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .emotion-confidence {
        color: #94a3b8;
        font-size: 1rem;
        margin-top: 0.3rem;
    }

    /* ---- Progress Bar ---- */
    .progress-container {
        background: rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        overflow: hidden;
        height: 28px;
        margin: 0.8rem 0;
        position: relative;
    }

    .progress-fill {
        height: 100%;
        border-radius: 12px;
        background: linear-gradient(90deg, #a855f7, #6366f1, #06b6d4);
        transition: width 0.5s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .progress-text {
        position: absolute;
        width: 100%;
        text-align: center;
        color: white;
        font-size: 0.8rem;
        font-weight: 600;
        line-height: 28px;
        top: 0;
        text-shadow: 0 1px 3px rgba(0,0,0,0.5);
    }

    /* ---- Status Badge ---- */
    .status-badge {
        display: inline-block;
        padding: 0.4rem 1.2rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    .status-waiting {
        background: rgba(99, 102, 241, 0.15);
        color: #818cf8;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }

    .status-detecting {
        background: rgba(168, 85, 247, 0.15);
        color: #c084fc;
        border: 1px solid rgba(168, 85, 247, 0.3);
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }

    .status-playing {
        background: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }

    .status-error {
        background: rgba(239, 68, 68, 0.15);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    /* ---- Now Playing Card ---- */
    .now-playing {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(6, 182, 212, 0.08));
        border: 1px solid rgba(34, 197, 94, 0.2);
        border-radius: 16px;
        padding: 1.2rem 1.5rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .now-playing .np-icon {
        font-size: 2.5rem;
    }

    .now-playing .np-text {
        color: #e2e8f0;
        font-weight: 600;
        font-size: 1rem;
    }

    .now-playing .np-mood {
        color: #4ade80;
        font-size: 0.9rem;
    }

    /* ---- Sidebar Styling ---- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f0c29 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }

    .sidebar-title {
        color: #e2e8f0;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .sidebar-section {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    /* ---- Playlist Grid ---- */
    .playlist-item {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.5rem 0.8rem;
        border-radius: 10px;
        margin-bottom: 0.4rem;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.04);
        transition: all 0.2s ease;
        color: #cbd5e1;
        font-size: 0.9rem;
    }

    .playlist-item:hover {
        background: rgba(168, 85, 247, 0.1);
        border-color: rgba(168, 85, 247, 0.2);
    }

    /* ---- Confidence Bars ---- */
    .conf-bar-container {
        margin: 0.4rem 0;
    }

    .conf-bar-label {
        display: flex;
        justify-content: space-between;
        color: #94a3b8;
        font-size: 0.82rem;
        margin-bottom: 3px;
    }

    .conf-bar-bg {
        background: rgba(255, 255, 255, 0.06);
        border-radius: 6px;
        height: 10px;
        overflow: hidden;
    }

    .conf-bar-fill {
        height: 100%;
        border-radius: 6px;
        transition: width 0.5s ease;
    }

    /* ---- Divider ---- */
    .fancy-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(168, 85, 247, 0.3), transparent);
        margin: 1.5rem 0;
    }

    /* ---- Camera Input Styling ---- */
    [data-testid="stCameraInput"] {
        border-radius: 16px;
        overflow: hidden;
    }

    [data-testid="stCameraInput"] > div {
        border-radius: 16px;
        border: 2px solid rgba(168, 85, 247, 0.2) !important;
    }

    /* ---- Metric overrides ---- */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 1rem;
    }

    [data-testid="stMetricValue"] {
        color: #e2e8f0;
    }

    /* ---- Buttons ---- */
    .stButton > button {
        background: linear-gradient(135deg, #a855f7, #6366f1);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(168, 85, 247, 0.35);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* ---- Sign-in Screen ---- */
    .signin-wrap {
        max-width: 560px;
        margin: 3rem auto 0;
        text-align: center;
    }

    .signin-steps {
        display: flex;
        justify-content: center;
        gap: 1.2rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }

    .signin-step {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1.2rem 1rem;
        width: 130px;
    }

    .signin-step .step-emoji {
        font-size: 2rem;
        display: block;
        margin-bottom: 0.4rem;
    }

    .signin-step .step-label {
        color: #cbd5e1;
        font-size: 0.85rem;
        font-weight: 500;
    }

    .signin-arrow {
        color: #6366f1;
        font-size: 1.5rem;
        align-self: center;
    }

    .spotify-connect-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.6rem;
        background: #1DB954;
        color: white !important;
        text-decoration: none !important;
        font-weight: 700;
        font-size: 1.05rem;
        padding: 0.9rem 2rem;
        border-radius: 50px;
        margin-top: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(29, 185, 84, 0.35);
    }

    .spotify-connect-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 28px rgba(29, 185, 84, 0.5);
    }

    .user-badge {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 0.6rem 0.8rem;
        margin-bottom: 0.8rem;
    }

    .user-badge img {
        border-radius: 50%;
        width: 36px;
        height: 36px;
    }

    .user-badge .user-name {
        color: #e2e8f0;
        font-weight: 600;
        font-size: 0.9rem;
    }

    .user-badge .user-sub {
        color: #4ade80;
        font-size: 0.75rem;
    }
</style>
"""
