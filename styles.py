"""Shared CSS for the Mood Music Player Streamlit app."""

CSS = """
<style>
    /* ==============================================================
       Fonts
       ============================================================== */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700;800&display=swap');

    :root {
        --bg-1: #0a0a16;
        --bg-2: #131328;
        --bg-3: #181830;
        --purple: #a855f7;
        --indigo: #6366f1;
        --cyan: #06b6d4;
        --spotify: #1DB954;
        --spotify-dark: #169c46;
        --text-hi: #f1f5f9;
        --text-mid: #cbd5e1;
        --text-lo: #94a3b8;
        --text-faint: #64748b;
        --glass-bg: rgba(255, 255, 255, 0.045);
        --glass-border: rgba(255, 255, 255, 0.09);

        /* Emotion palette */
        --e-aggressive: #ef4444;
        --e-contempt:   #f97316;
        --e-disgust:    #22c55e;
        --e-fear:       #8b5cf6;
        --e-happy:      #eab308;
        --e-sad:        #3b82f6;
        --e-surprise:   #ec4899;
    }

    /* ==============================================================
       Global background + aurora effect
       ============================================================== */
    html, body {
        background: var(--bg-1);
    }

    .stApp {
        background: linear-gradient(160deg, var(--bg-1) 0%, var(--bg-2) 45%, var(--bg-3) 100%);
        font-family: 'Inter', sans-serif;
        position: relative;
        min-height: 100vh;
    }

    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        min-height: 100vh;
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer-events: none;
        background:
            radial-gradient(circle at 15% 20%, rgba(168, 85, 247, 0.20), transparent 42%),
            radial-gradient(circle at 85% 15%, rgba(6, 182, 212, 0.16), transparent 40%),
            radial-gradient(circle at 50% 90%, rgba(99, 102, 241, 0.16), transparent 45%),
            radial-gradient(circle at 90% 80%, rgba(29, 185, 84, 0.08), transparent 40%);
        animation: auroraDrift 20s ease-in-out infinite alternate;
    }

    @keyframes auroraDrift {
        0%   { transform: translate3d(0, 0, 0) scale(1); }
        50%  { transform: translate3d(1.5%, -2%, 0) scale(1.06); }
        100% { transform: translate3d(-2%, 1.5%, 0) scale(1); }
    }

    [data-testid="stAppViewContainer"] { position: relative; z-index: 1; }
    [data-testid="stHeader"] { background: transparent; }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Scrollbar */
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--purple), var(--indigo));
        border-radius: 10px;
    }

    /* ==============================================================
       Header / Hero
       ============================================================== */
    .app-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.7rem;
        padding: 1.6rem 0 0.2rem;
    }

    .app-logo-badge {
        width: 46px;
        height: 46px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        background: linear-gradient(135deg, rgba(168,85,247,0.25), rgba(6,182,212,0.2));
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 4px 24px rgba(168, 85, 247, 0.25);
    }

    .hero-title {
        text-align: center;
        padding: 0;
        font-family: 'Outfit', sans-serif;
        background: linear-gradient(90deg, #c084fc, #818cf8, #22d3ee, #818cf8, #c084fc);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.9rem;
        font-weight: 800;
        letter-spacing: -1.2px;
        animation: shimmerTitle 6s linear infinite;
        margin: 0;
    }

    @keyframes shimmerTitle {
        to { background-position: -200% center; }
    }

    .hero-subtitle {
        text-align: center;
        color: var(--text-lo);
        font-size: 1.05rem;
        font-weight: 400;
        margin: 0.3rem 0 1.6rem;
        letter-spacing: 0.3px;
    }

    /* ==============================================================
       Glass Cards
       ============================================================== */
    .card-marker { display: none; }

    .glass-card,
    [data-testid="stVerticalBlockBorderWrapper"]:has(.card-marker) {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 18px !important;
        padding: 1.5rem 1.6rem !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        margin-bottom: 1.1rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.18) !important;
        transition: transform 0.35s cubic-bezier(.2,.8,.2,1), border-color 0.35s ease, box-shadow 0.35s ease;
    }

    .glass-card::before,
    [data-testid="stVerticalBlockBorderWrapper"]:has(.card-marker)::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--purple), var(--cyan), transparent);
        opacity: 0.6;
    }

    .glass-card:hover,
    [data-testid="stVerticalBlockBorderWrapper"]:has(.card-marker):hover {
        transform: translateY(-3px);
        border-color: rgba(168, 85, 247, 0.35);
        box-shadow: 0 14px 40px rgba(168, 85, 247, 0.12);
    }

    .glass-card h3,
    [data-testid="stVerticalBlockBorderWrapper"]:has(.card-marker) h3 {
        color: var(--text-hi);
        font-family: 'Outfit', sans-serif;
        font-size: 1.12rem;
        font-weight: 600;
        margin: 0 0 1rem;
        letter-spacing: 0.2px;
    }

    /* ==============================================================
       Emotion Display
       ============================================================== */
    .emotion-display {
        text-align: center;
        padding: 1.8rem 1rem 1.2rem;
        --glow: var(--e-color, var(--purple));
    }

    .emotion-emoji {
        font-size: 5.2rem;
        display: inline-block;
        margin-bottom: 0.6rem;
        animation: floatBounce 2.6s ease-in-out infinite;
        filter: drop-shadow(0 0 22px var(--glow));
    }

    @keyframes floatBounce {
        0%, 100% { transform: translateY(0) scale(1); }
        50% { transform: translateY(-12px) scale(1.05); }
    }

    .emotion-label {
        display: block;
        font-family: 'Outfit', sans-serif;
        font-size: 1.9rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 3px;
        color: var(--glow);
        text-shadow: 0 0 30px color-mix(in srgb, var(--glow) 50%, transparent);
    }

    .emotion-confidence {
        color: var(--text-lo);
        font-size: 0.95rem;
        margin-top: 0.4rem;
        font-weight: 500;
    }

    .emotion-waiting-icon {
        font-size: 4.5rem;
        display: inline-block;
        opacity: 0.85;
        animation: gentleSway 3s ease-in-out infinite;
    }

    @keyframes gentleSway {
        0%, 100% { transform: rotate(-4deg); }
        50% { transform: rotate(4deg); }
    }

    /* ==============================================================
       Progress Bar
       ============================================================== */
    .progress-label-row {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        color: var(--text-lo);
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 0.4rem;
    }

    .progress-container {
        background: rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        overflow: hidden;
        height: 30px;
        margin: 0.3rem 0 0.8rem;
        position: relative;
        border: 1px solid rgba(255,255,255,0.05);
    }

    .progress-fill {
        height: 100%;
        border-radius: 12px;
        background: linear-gradient(90deg, var(--purple), var(--indigo), var(--cyan));
        background-size: 200% 100%;
        animation: progressShimmer 2.5s linear infinite;
        transition: width 0.6s cubic-bezier(.2,.8,.2,1);
    }

    @keyframes progressShimmer {
        to { background-position: -200% 0; }
    }

    .progress-text {
        position: absolute;
        width: 100%;
        text-align: center;
        color: white;
        font-size: 0.8rem;
        font-weight: 600;
        line-height: 30px;
        top: 0;
        text-shadow: 0 1px 3px rgba(0,0,0,0.5);
    }

    /* ==============================================================
       Status Badge
       ============================================================== */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.45rem 1.3rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    .status-badge .dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: currentColor;
        box-shadow: 0 0 8px currentColor;
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
    }

    .status-detecting .dot { animation: pulseDot 1.4s infinite; }

    @keyframes pulseDot {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(1.4); }
    }

    .status-playing {
        background: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }

    .status-playing .dot { animation: pulseDot 1.4s infinite; }

    .status-error {
        background: rgba(239, 68, 68, 0.15);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    /* ==============================================================
       Now Playing Card
       ============================================================== */
    .now-playing {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.12), rgba(6, 182, 212, 0.08));
        border: 1px solid rgba(34, 197, 94, 0.25);
        border-radius: 18px;
        padding: 1.3rem 1.6rem;
        display: flex;
        align-items: center;
        gap: 1.1rem;
        box-shadow: 0 8px 32px rgba(34, 197, 94, 0.1);
    }

    .now-playing .np-icon {
        font-size: 2.6rem;
        animation: vinylSpin 3s linear infinite;
    }

    @keyframes vinylSpin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    .now-playing .np-text {
        color: var(--text-hi);
        font-weight: 600;
        font-size: 1.02rem;
        font-family: 'Outfit', sans-serif;
    }

    .now-playing .np-mood {
        color: #4ade80;
        font-size: 0.9rem;
        margin-top: 0.15rem;
    }

    /* ==============================================================
       Sidebar
       ============================================================== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #14142c 0%, #0a0a16 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }

    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 0.8rem;
    }

    .sidebar-brand .badge-icon {
        width: 38px;
        height: 38px;
        border-radius: 11px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        background: linear-gradient(135deg, rgba(168,85,247,0.3), rgba(6,182,212,0.25));
        border: 1px solid rgba(255,255,255,0.12);
    }

    .sidebar-title {
        color: var(--text-hi);
        font-family: 'Outfit', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        margin: 0;
    }

    .sidebar-tagline {
        color: var(--text-faint);
        font-size: 0.75rem;
        margin: 0;
    }

    .sidebar-section {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    .sidebar-stat-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.35rem 0;
        color: var(--text-mid);
        font-size: 0.85rem;
    }

    .sidebar-stat-row .val {
        color: var(--text-hi);
        font-weight: 700;
        font-family: 'Outfit', sans-serif;
    }

    .sidebar-footer {
        color: var(--text-faint);
        font-size: 0.75rem;
        text-align: center;
        line-height: 1.5;
    }

    /* ==============================================================
       Playlist Grid (Spotify-style cards)
       ============================================================== */
    .playlist-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
        gap: 1rem;
    }

    .playlist-card {
        position: relative;
        border-radius: 16px;
        padding: 1.2rem 1.1rem 1.3rem;
        background: linear-gradient(160deg, color-mix(in srgb, var(--pl-color) 22%, #12121f), #0e0e1c 80%);
        border: 1px solid color-mix(in srgb, var(--pl-color) 35%, transparent);
        overflow: hidden;
        transition: transform 0.3s cubic-bezier(.2,.8,.2,1), box-shadow 0.3s ease;
        text-decoration: none !important;
        display: block;
    }

    .playlist-card:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 16px 36px color-mix(in srgb, var(--pl-color) 30%, transparent);
    }

    .playlist-card .pl-art {
        width: 100%;
        aspect-ratio: 1 / 1;
        border-radius: 12px;
        background: radial-gradient(circle at 30% 30%, color-mix(in srgb, var(--pl-color) 70%, white 10%), color-mix(in srgb, var(--pl-color) 40%, #000 30%));
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.6rem;
        margin-bottom: 0.9rem;
        box-shadow: inset 0 0 30px rgba(0,0,0,0.25);
    }

    .playlist-card .pl-name {
        color: var(--text-hi);
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0.2rem;
        text-transform: capitalize;
    }

    .playlist-card .pl-sub {
        color: var(--text-lo);
        font-size: 0.78rem;
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }

    .playlist-card .pl-play {
        position: absolute;
        right: 1rem;
        bottom: 1rem;
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: var(--spotify);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        color: #06210f;
        opacity: 0;
        transform: translateY(8px);
        transition: all 0.3s ease;
        box-shadow: 0 6px 18px rgba(29,185,84,0.4);
    }

    .playlist-card:hover .pl-play {
        opacity: 1;
        transform: translateY(0);
    }

    /* ==============================================================
       Confidence Bars
       ============================================================== */
    .conf-bar-container {
        margin: 0.55rem 0;
    }

    .conf-bar-label {
        display: flex;
        justify-content: space-between;
        color: var(--text-mid);
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 4px;
    }

    .conf-bar-label .val {
        font-weight: 700;
        color: var(--text-hi);
    }

    .conf-bar-bg {
        background: rgba(255, 255, 255, 0.06);
        border-radius: 7px;
        height: 11px;
        overflow: hidden;
    }

    .conf-bar-fill {
        height: 100%;
        border-radius: 7px;
        transition: width 0.6s cubic-bezier(.2,.8,.2,1);
        box-shadow: 0 0 12px -2px currentColor;
    }

    /* ==============================================================
       History: stat tiles + timeline
       ============================================================== */
    .stat-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 0.9rem;
        margin-bottom: 0.4rem;
    }

    .stat-tile {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px;
        padding: 1rem 1.1rem;
        text-align: center;
    }

    .stat-tile .stat-emoji { font-size: 1.6rem; display: block; margin-bottom: 0.3rem; }
    .stat-tile .stat-value {
        font-family: 'Outfit', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-hi);
        line-height: 1.1;
    }
    .stat-tile .stat-label {
        color: var(--text-faint);
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.2rem;
    }

    .timeline {
        position: relative;
        padding-left: 1.6rem;
    }

    .timeline::before {
        content: "";
        position: absolute;
        left: 7px;
        top: 6px;
        bottom: 6px;
        width: 2px;
        background: linear-gradient(180deg, var(--purple), transparent);
        opacity: 0.4;
    }

    .timeline-item {
        position: relative;
        display: flex;
        align-items: center;
        gap: 0.7rem;
        padding: 0.55rem 0.8rem;
        border-radius: 12px;
        margin-bottom: 0.4rem;
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.05);
        transition: background 0.25s ease, transform 0.25s ease;
    }

    .timeline-item:hover {
        background: rgba(255,255,255,0.05);
        transform: translateX(3px);
    }

    .timeline-item::before {
        content: "";
        position: absolute;
        left: -1.6rem;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: var(--dot-color, var(--purple));
        box-shadow: 0 0 10px var(--dot-color, var(--purple));
    }

    .timeline-item .ti-emoji { font-size: 1.3rem; }
    .timeline-item .ti-label {
        color: var(--text-hi);
        font-weight: 600;
        font-size: 0.92rem;
        text-transform: capitalize;
        flex: 1;
    }
    .timeline-item .ti-index {
        color: var(--text-faint);
        font-size: 0.75rem;
    }

    /* ==============================================================
       Divider
       ============================================================== */
    .fancy-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(168, 85, 247, 0.35), rgba(6,182,212,0.25), transparent);
        margin: 1.7rem 0;
        border: none;
    }

    /* ==============================================================
       Camera Input
       ============================================================== */
    [data-testid="stCameraInput"] {
        border-radius: 18px;
        overflow: hidden;
    }

    [data-testid="stCameraInput"] > div {
        border-radius: 18px;
        border: 2px solid rgba(168, 85, 247, 0.25) !important;
    }

    [data-testid="stCameraInput"] button {
        border-radius: 50px !important;
    }

    /* ==============================================================
       Streamlit widget overrides
       ============================================================== */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 1rem;
    }

    [data-testid="stMetricValue"] { color: var(--text-hi); }

    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: rgba(255,255,255,0.03);
        padding: 6px;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.07);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 11px;
        padding: 10px 20px;
        color: var(--text-lo);
        font-weight: 600;
        font-family: 'Outfit', sans-serif;
        transition: all 0.25s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: var(--text-hi);
        background: rgba(255,255,255,0.04);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--purple), var(--indigo)) !important;
        color: white !important;
        box-shadow: 0 4px 16px rgba(168, 85, 247, 0.35);
    }

    .stTabs [data-baseweb="tab-highlight"] { display: none; }

    [data-testid="stSlider"] [role="slider"] {
        box-shadow: 0 0 0 6px rgba(168, 85, 247, 0.18);
    }

    /* ---- Buttons ---- */
    .stButton > button {
        background: linear-gradient(135deg, var(--purple), var(--indigo));
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.65rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        font-family: 'Outfit', sans-serif;
        transition: all 0.3s ease;
        width: 100%;
        position: relative;
        overflow: hidden;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 28px rgba(168, 85, 247, 0.4);
    }

    .stButton > button:active { transform: translateY(0); }

    /* ==============================================================
       Sign-in Screen
       ============================================================== */
    .signin-wrap {
        max-width: 640px;
        margin: 2.5rem auto 0;
        text-align: center;
    }

    .signin-steps {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1rem;
        margin: 2.2rem 0;
        flex-wrap: wrap;
    }

    .signin-step {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 1.4rem 1.1rem;
        width: 140px;
        position: relative;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }

    .signin-step:hover {
        transform: translateY(-4px);
        border-color: rgba(168, 85, 247, 0.4);
    }

    .signin-step .step-num {
        position: absolute;
        top: -10px;
        left: -10px;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--purple), var(--indigo));
        color: white;
        font-size: 0.72rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 10px rgba(168,85,247,0.5);
    }

    .signin-step .step-emoji {
        font-size: 2.1rem;
        display: block;
        margin-bottom: 0.5rem;
        filter: drop-shadow(0 0 12px rgba(168,85,247,0.3));
    }

    .signin-step .step-label {
        color: var(--text-mid);
        font-size: 0.85rem;
        font-weight: 500;
    }

    .signin-arrow {
        color: var(--indigo);
        font-size: 1.4rem;
        align-self: center;
        opacity: 0.6;
    }

    .spotify-connect-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.7rem;
        background: linear-gradient(135deg, var(--spotify), var(--spotify-dark));
        color: white !important;
        text-decoration: none !important;
        font-weight: 700;
        font-family: 'Outfit', sans-serif;
        font-size: 1.08rem;
        padding: 1rem 2.3rem;
        border-radius: 50px;
        margin-top: 0.6rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 24px rgba(29, 185, 84, 0.4);
        animation: spotifyPulse 2.6s ease-in-out infinite;
    }

    @keyframes spotifyPulse {
        0%, 100% { box-shadow: 0 4px 24px rgba(29, 185, 84, 0.4); }
        50% { box-shadow: 0 4px 34px rgba(29, 185, 84, 0.65); }
    }

    .spotify-connect-btn:hover {
        transform: translateY(-3px) scale(1.03);
        box-shadow: 0 10px 36px rgba(29, 185, 84, 0.55);
        animation: none;
    }

    .signin-note {
        color: var(--text-faint);
        font-size: 0.85rem;
        margin-top: 1.6rem;
        line-height: 1.6;
    }

    .user-badge {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 0.7rem 0.9rem;
        margin-bottom: 0.8rem;
    }

    .user-badge img {
        border-radius: 50%;
        width: 40px;
        height: 40px;
        border: 2px solid rgba(29, 185, 84, 0.5);
    }

    .user-badge .user-name {
        color: var(--text-hi);
        font-weight: 600;
        font-size: 0.92rem;
        font-family: 'Outfit', sans-serif;
    }

    .user-badge .user-sub {
        color: #4ade80;
        font-size: 0.76rem;
    }

    /* ==============================================================
       App Footer
       ============================================================== */
    .app-footer {
        text-align: center;
        color: var(--text-faint);
        font-size: 0.82rem;
        padding: 1.2rem 0 0.6rem;
        display: flex;
        flex-direction: column;
        gap: 0.3rem;
        align-items: center;
    }

    .app-footer .foot-links {
        display: flex;
        gap: 1rem;
        color: var(--text-lo);
    }

    /* ==============================================================
       Responsive
       ============================================================== */
    @media (max-width: 768px) {
        .hero-title { font-size: 2rem; }
        .hero-subtitle { font-size: 0.9rem; }
        .signin-step { width: 100px; padding: 1rem 0.7rem; }
        .signin-arrow { display: none; }
        .emotion-emoji { font-size: 4rem; }
        .emotion-label { font-size: 1.4rem; letter-spacing: 2px; }
        .playlist-grid { grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); }
    }
</style>
"""
