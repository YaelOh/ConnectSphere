from fastapi import FastAPI
from app.routes.spotify import router as spotify_router
from app.routes.analysis import router as analysis_router

app = FastAPI(
    title="ConnectSphere",
    description="Analyze user podcast preferences and recommend related content.",
    version="1.0.0"
)

# Include routes
app.include_router(spotify_router, prefix="/api/spotify", tags=["Spotify"])
app.include_router(analysis_router, prefix="/api/analysis", tags=["Analysis"])

@app.get("/")
def root():
    return {"message": "Welcome to ConnectSphere! Authenticate with Spotify to start."}