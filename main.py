
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp

app = FastAPI(title="ClipGenius AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    url: str

@app.get("/")
def home():
    return {"message": "ClipGenius AI Backend is running!"}

@app.get("/health")
def health():
    return {"status": "online"}

@app.post("/analyze")
def analyze_video(data: VideoRequest):
    url = data.url.strip()

    if "youtube.com/" not in url and "youtu.be/" not in url:
        raise HTTPException(status_code=400, detail="Valid YouTube URL required")

    options = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "socket_timeout": 30,
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)

        return {
            "success": True,
            "title": info.get("title"),
            "duration": info.get("duration"),
            "message": "Video information received successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
      
