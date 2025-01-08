from fastapi import APIRouter, Depends
from app.routes.spotify_client import SpotifyClient

router = APIRouter()

@router.get("/auth-url")
def get_spotify_auth_url():
    """
    Provide the Spotify authentication URL for the user.
    """
    return {"auth_url": SpotifyClient.get_auth_url()}

@router.get("/user-data")
def get_user_data(auth_code: str):
    """
    Retrieve user's recent podcasts after authentication.
    """
    spotify = SpotifyClient(auth_code)
    podcasts = spotify.get_recent_podcasts()
    return {"recent_podcasts": podcasts}