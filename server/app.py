from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import whisper
import yt_dlp
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="ConnectSphere API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Spotify client
spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
    )
)

# Initialize Whisper model
model = whisper.load_model("base")

class TranscriptionRequest(BaseModel):
    url: str

class TranscriptionResponse(BaseModel):
    transcript: str

async def download_audio(url: str) -> str:
    """Download audio from Spotify podcast episode."""
    try:
        # Extract episode ID from URL
        episode_id = url.split('/')[-1].split('?')[0]
        
        # Get episode details from Spotify API
        episode = spotify.episode(episode_id)
        
        # Configure yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'temp_audio.%(ext)s'
        }
        
        # Download audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        return 'temp_audio.mp3'
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error downloading audio: {str(e)}")

async def transcribe_audio(audio_path: str) -> str:
    """Transcribe audio file using Whisper."""
    try:
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error transcribing audio: {str(e)}")
    finally:
        # Clean up temporary audio file
        if os.path.exists(audio_path):
            os.remove(audio_path)

@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe(request: TranscriptionRequest):
    """
    Transcribe a Spotify podcast episode.
    
    - **url**: Spotify podcast episode URL
    """
    try:
        # Download audio
        audio_path = await download_audio(request.url)
        
        # Transcribe audio
        transcript = await transcribe_audio(audio_path)
        
        return {"transcript": transcript}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Server is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)