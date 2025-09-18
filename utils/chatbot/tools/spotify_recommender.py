# utils/chatbot/spotify_recommender.py
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env before any usage
load_dotenv()

# --- Spotify API Credentials ---
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

SCOPE = "user-read-playback-state user-modify-playback-state"

# Official Spotify seed genres list (partial, extend as needed)
VALID_SPOTIFY_GENRES = {
    "acoustic",
    "afrobeat",
    "alt-rock",
    "ambient",
    "bluegrass",
    "blues",
    "bossanova",
    "brazil",
    "breakbeat",
    "british",
    "cantopop",
    "chicago-house",
    "classical",
    "country",
    "dance",
    "dancehall",
    "deep-house",
    "detroit-techno",
    "disco",
    "disney",
    "drum-and-bass",
    "dub",
    "dubstep",
    "edm",
    "electro",
    "electronic",
    "falsetto",
    "folk",
    "funk",
    "garage",
    "gospel",
    "goth",
    "grindcore",
    "groove",
    "grunge",
    "guitar",
    "happy",
    "hard-rock",
    "hardcore",
    "hardstyle",
    "heavy-metal",
    "hip-hop",
    "house",
    "idm",
    "indie",
    "indie-pop",
    "industrial",
    "iranian",
    "j-dance",
    "j-idol",
    "j-pop",
    "j-rock",
    "jazz",
    "k-pop",
    "kids",
    "latin",
    "latino",
    "malay",
    "mandopop",
    "metal",
    "metal-misc",
    "metalcore",
    "minimal-techno",
    "mpb",
    "new-age",
    "neo-soul",
    "new-release",
    "opera",
    "pagode",
    "party",
    "philippines-opm",
    "piano",
    "pop",
    "pop-film",
    "post-dubstep",
    "power-pop",
    "progressive-house",
    "psych-rock",
    "punk",
    "punk-rock",
    "r-n-b",
    "rainy-day",
    "reggae",
    "reggaeton",
    "road-trip",
    "rock",
    "rock-n-roll",
    "rockabilly",
    "romance",
    "sad",
    "salsa",
    "samba",
    "sertanejo",
    "show-tunes",
    "singer-songwriter",
    "ska",
    "sleep",
    "songwriter",
    "soul",
    "soundtracks",
    "spanish",
    "study",
    "summer",
    "swedish",
    "synth-pop",
    "tango",
    "techno",
    "trance",
    "trip-hop",
    "turkish",
    "work-out",
    "world-music",
}


def get_spotify_oauth():
    """Initializes and returns a SpotifyOAuth object."""
    if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET or not SPOTIPY_REDIRECT_URI:
        st.error(
            "Spotify API credentials not found. Please set SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, and SPOTIPY_REDIRECT_URI in your .env file."
        )
        return None
    return SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE,
        cache_path=".spotify_cache",
    )


def authenticate_spotify():
    """Handles Spotify authentication flow for Streamlit."""
    sp_oauth = get_spotify_oauth()
    if not sp_oauth:
        return None

    token_info = sp_oauth.get_cached_token()
    if token_info:
        st.session_state["spotify_token_info"] = token_info
        return spotipy.Spotify(auth=token_info["access_token"])

    auth_url = sp_oauth.get_authorize_url()
    st.sidebar.markdown(
        f"[Click here to log in to Spotify]({auth_url})", unsafe_allow_html=True
    )
    st.info(
        "After logging in, copy the URL from your browser's address bar and paste it below."
    )

    redirect_response = st.text_input(
        "Paste the full redirect URL from your browser here:"
    )
    if redirect_response:
        try:
            code = sp_oauth.parse_response_code(redirect_response)
            token_info = sp_oauth.get_access_token(code)
            st.session_state["spotify_token_info"] = token_info
            st.success("Successfully logged into Spotify!")
            st.rerun()
        except Exception as e:
            st.error(f"Error getting Spotify token: {e}")
    return None


def get_spotify_client():
    """Returns an authenticated Spotipy client if available in session state, refreshes as needed."""
    if (
        "spotify_token_info" in st.session_state
        and st.session_state["spotify_token_info"]
    ):
        token_info = st.session_state["spotify_token_info"]
        sp_oauth = get_spotify_oauth()
        if not sp_oauth:
            return None
        if sp_oauth.is_token_expired(token_info):
            st.warning("Spotify token expired. Re-authenticating...")
            try:
                token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
            except Exception as e:
                st.error(f"Failed to refresh Spotify token: {e}")
                return None
            st.session_state["spotify_token_info"] = token_info
        return spotipy.Spotify(auth=token_info["access_token"])
    return None


def get_recommendations(sp_client, mood="calming", limit=5):
    """
    Fetches music recommendations based on mood.
    Moods map to Spotify genres/audio features.
    """
    if not sp_client:
        st.error("Spotify client not authenticated.")
        return []

    if mood == "calming":
        requested_genres = ["ambient", "chill", "classical", "jazz"]
        target_acousticness = 0.8
        target_energy = 0.3
        target_valence = 0.5
    elif mood == "energetic":
        # Corrected "workout" to "work-out"
        requested_genres = ["pop", "dance", "rock", "funk", "work-out"]
        target_acousticness = 0.2
        target_energy = 0.8
        target_valence = 0.7
    elif mood == "focused":
        requested_genres = ["ambient", "chill", "classical"]
        target_acousticness = 0.7
        target_energy = 0.4
        target_valence = 0.4
    else:
        requested_genres = ["pop"]
        target_acousticness = None
        target_energy = None
        target_valence = None

    # Validate and limit to max 5 genres
    seed_genres = [g for g in requested_genres if g in VALID_SPOTIFY_GENRES][:5]

    try:
        recommendations = sp_client.recommendations(
            seed_genres=seed_genres,
            limit=limit,
            target_acousticness=target_acousticness,
            target_energy=target_energy,
            target_valence=target_valence,
        )
        return recommendations["tracks"]
    except spotipy.exceptions.SpotifyException as e:
        st.error(f"Spotify API error: {e}")
        if "No recommendations available" in str(e):
            st.warning(
                "Could not find recommendations for the selected mood/genres. Try a different mood or fewer genre seeds."
            )
        return []
    except Exception as e:
        st.error(f"An unexpected error occurred while fetching recommendations: {e}")
        return []


def play_track(sp_client, track_uri):
    """Attempts to play a specific track on the user's active Spotify device."""
    if not sp_client:
        st.error("Spotify client not authenticated.")
        return False
    try:
        sp_client.start_playback(uris=[track_uri])
        st.success(f"Playing {track_uri.split(':')[-1]}! (Check your Spotify app)")
        return True
    except spotipy.exceptions.SpotifyException as e:
        if "Player command failed: Restriction violated" in str(
            e
        ) or "No active device found" in str(e):
            st.warning(
                "Please ensure Spotify is open and playing on an active device to control playback."
            )
        else:
            st.error(f"Error playing track: {e}")
        return False
    except Exception as e:
        st.error(f"An unexpected error occurred while attempting to play music: {e}")
        return False


def spotify_music_tool():
    """Streamlit UI for Spotify music recommendations."""
    st.markdown("## 🎶 Music for Your Mood")

    sp = get_spotify_client()

    if not sp:
        st.info("Connect to Spotify to get music recommendations.")
        authenticate_spotify()
        return

    st.success("Connected to Spotify!")

    mood_choice = st.selectbox(
        "What kind of music are you in the mood for?",
        ["calming", "energetic", "focused"],
    )

    if st.button(f"Get {mood_choice.capitalize()} Music"):
        st.session_state["spotify_recommendations"] = get_recommendations(
            sp, mood=mood_choice, limit=5
        )

    if (
        "spotify_recommendations" in st.session_state
        and st.session_state["spotify_recommendations"]
    ):
        st.write("Here are some recommendations:")
        for i, track in enumerate(st.session_state["spotify_recommendations"]):
            col1, col2 = st.columns([0.7, 0.3])
            with col1:
                st.markdown(f"**{track['name']}** by {track['artists'][0]['name']}")
            with col2:
                if st.button("Play", key=f"play_button_{track['id']}"):
                    play_track(sp, track["uri"])
            if track.get("album") and track["album"].get("images"):
                album_art_url = track["album"]["images"][0]["url"]
                st.image(album_art_url, width=100)
            st.markdown(f"[Listen on Spotify]({track['external_urls']['spotify']})")
            st.markdown("---")
