import requests
import os

class SpotifyClient:
    AUTH_URL = "https://accounts.spotify.com/authorize"
    TOKEN_URL = "https://accounts.spotify.com/api/token"
    API_URL = "https://api.spotify.com/v1"

    def __init__(self, auth_code=None):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.auth_code = auth_code
        self.access_token = self.get_access_token() if auth_code else None

    def get_access_token(self):
        """
        Exchanges the authorization code for an access token.
        """
        data = {
            "grant_type": "authorization_code",
            "code": self.auth_code,
            "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"),
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = requests.post(self.TOKEN_URL, data=data)
        response.raise_for_status()
        return response.json()["access_token"]

    def get_recent_podcasts(self):
        """
        Fetches the user's recently played podcasts.
        """
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(f"{self.API_URL}/me/player/recently-played?type=show", headers=headers)
        response.raise_for_status()
        return response.json().get("items", [])

    @staticmethod
    def get_auth_url():
        """
        Generates the Spotify authentication URL.
        """
        return (
            f"{SpotifyClient.AUTH_URL}?client_id={os.getenv('SPOTIFY_CLIENT_ID')}"
            f"&response_type=code&redirect_uri={os.getenv('SPOTIFY_REDIRECT_URI')}&scope=user-read-recently-played"
        )