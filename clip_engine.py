
import os
import subprocess
import json
from faster_whisper import WhisperModel


class ClipGeniusEngine:

    def __init__(self):
        self.model = None

    def load_ai(self):
        if self.model is None:
            self.model = WhisperModel(
                "base",
                device="cpu",
                compute_type="int8"
            )
        return self.model

    def extract_audio(self, video_path):
        audio_path = "clipgenius_audio.wav"

        command = [
            "ffmpeg",
            "-y",
            "-i", video_path,
            "-vn",
            "-ac", "1",
            "-ar", "16000",
            audio_path
        ]

        subprocess.run(command, check=True)
        return audio_path

    def transcribe(self, audio_path):
        model = self.load_ai()

        segments, info = model.transcribe(
            audio_path,
            beam_size=5,
            vad_filter=True
        )

        transcript = []

        for segment in segments:
            transcript.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip()
            })

        return {
            "language": info.language,
            "segments": transcript
        }

    def analyze_video(self, video_path):
        audio_path = self.extract_audio(video_path)
        result = self.transcribe(audio_path)

        return {
            "success": True,
            "language": result["language"],
            "transcript": result["segments"]
        }


engine = ClipGeniusEngine()
