
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from pipeline import process_video

app = FastAPI(title="ClipGenius AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    video_path: str
    clips: int = 3
    duration: int = 45


@app.get("/")
def home():
    return {"message": "ClipGenius AI is running!"}


@app.get("/health")
def health():
    return {"status": "online"}


@app.post("/analyze")
def analyze_video(data: VideoRequest):

    try:
        result = process_video(
            video_path=data.video_path,
            clip_count=data.clips,
            duration=data.duration
        )

        return result

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
