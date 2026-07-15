"""
Per-session Spotify authentication.

Each visitor signs in with their own Spotify account via the standard OAuth
Authorization Code flow, done entirely in-app (no local helper server, no
shared token file). The resulting token lives only in that visitor's
st.session_state, so many people can be signed in to the same deployed app
at once without colliding with each other.
"""

import base64
import logging
import os
import pathlib
import secrets
import time
import urllib.parse

import requests
import streamlit as st

logger = logging.getLogger(__name__)

AUTHORIZE_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
SCOPES = "user-modify-playback-state user-read-playback-state user-read-private user-read-email"


def _secrets_file_present():
    """Avoid touching st.secrets entirely when no secrets.toml exists — accessing
    it in that case makes Streamlit render a visible warning box in the app."""
    candidates = [
        pathlib.Path(".streamlit/secrets.toml"),
        pathlib.Path.home() / ".streamlit" / "secrets.toml",
    ]
    return any(p.exists() for p in candidates)


def get_client_credentials():
    """Read Spotify app credentials from st.secrets (cloud) or env vars (.env locally)."""
    def _read(key):
        if _secrets_file_present():
            try:
                if key in st.secrets:
                    return st.secrets[key]
            except Exception:
                pass
        return os.getenv(key)

    client_id = _read("SPOTIFY_CLIENT_ID")
    client_secret = _read("SPOTIFY_CLIENT_SECRET")
    redirect_uri = _read("SPOTIFY_REDIRECT_URI")

    if not client_id or not client_secret or not redirect_uri:
        raise RuntimeError(
            "Missing Spotify credentials. Set SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, "
            "and SPOTIFY_REDIRECT_URI in .env (local) or st.secrets (deployed)."
        )
    return client_id, client_secret, redirect_uri


def build_authorize_url():
    """Build the Spotify consent-screen URL and stash a CSRF state token in the session."""
    client_id, _, redirect_uri = get_client_credentials()
    state = secrets.token_urlsafe(16)
    st.session_state.oauth_state = state

    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": SCOPES,
        "state": state,
        "show_dialog": "false",
    }
    return f"{AUTHORIZE_URL}?{urllib.parse.urlencode(params)}"


def _store_token(token_data):
    st.session_state.sp_token = {
        "access_token": token_data["access_token"],
        "refresh_token": token_data.get("refresh_token", st.session_state.get("sp_token", {}).get("refresh_token")),
        "expires_at": time.time() + token_data.get("expires_in", 3600),
    }


def _basic_auth_header(client_id, client_secret):
    raw = f"{client_id}:{client_secret}".encode("utf-8")
    return {"Authorization": f"Basic {base64.b64encode(raw).decode('utf-8')}"}


def handle_redirect():
    """
    Call once near the top of the app on every run. If Spotify just redirected
    back with an authorization code, exchange it for a token and store it in
    this visitor's session.
    """
    if is_authenticated():
        return

    query = st.query_params
    code = query.get("code")
    state = query.get("state")

    if not code:
        return

    if not state or state != st.session_state.get("oauth_state"):
        logger.warning("Spotify OAuth state mismatch; ignoring callback.")
        st.query_params.clear()
        return

    client_id, client_secret, redirect_uri = get_client_credentials()

    try:
        response = requests.post(
            TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
            },
            headers=_basic_auth_header(client_id, client_secret),
            timeout=10,
        )
        response.raise_for_status()
        _store_token(response.json())
        logger.info("Spotify sign-in succeeded for this session.")
    except Exception as e:
        logger.error("Spotify token exchange failed: %s", e)
        st.session_state.auth_error = f"Spotify sign-in failed: {e}"

    st.query_params.clear()
    st.rerun()


def _refresh_token():
    client_id, client_secret, _ = get_client_credentials()
    refresh_token = st.session_state.sp_token.get("refresh_token")
    if not refresh_token:
        return False

    try:
        response = requests.post(
            TOKEN_URL,
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
            headers=_basic_auth_header(client_id, client_secret),
            timeout=10,
        )
        response.raise_for_status()
        _store_token(response.json())
        return True
    except Exception as e:
        logger.error("Spotify token refresh failed: %s", e)
        return False


def is_authenticated():
    return "sp_token" in st.session_state and bool(st.session_state.sp_token.get("access_token"))


def get_spotify_client():
    """Return an authenticated spotipy.Spotify for this session, or None if not signed in."""
    if not is_authenticated():
        return None

    import spotipy

    token = st.session_state.sp_token
    if time.time() >= token["expires_at"] - 30:
        if not _refresh_token():
            sign_out()
            return None
        token = st.session_state.sp_token

    return spotipy.Spotify(auth=token["access_token"], requests_timeout=10)


def sign_out():
    st.session_state.pop("sp_token", None)
    st.session_state.pop("oauth_state", None)
