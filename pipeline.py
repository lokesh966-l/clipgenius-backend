
import os

from clip_engine import engine
from moment_ranker import find_moments
from video_clipper import create_multiple_clips
from caption_maker import make_srt


def process_video(video_path, clip_count=3, duration=45):

    if not os.path.exists(video_path):
        raise FileNotFoundError("Video file not found")

    # Step 1: AI analyzes audio
    analysis = engine.analyze_video(video_path)

    transcript = analysis["transcript"]

    # Step 2: Find interesting moments
    moments = find_moments(
        transcript,
        duration=duration,
        limit=clip_count
    )

    if not moments:
        return {
            "success": False,
            "message": "No suitable moments found"
        }

    # Step 3: Create vertical clips
    clips = create_multiple_clips(
        video_path,
        moments
    )

    # Step 4: Create captions for each clip
    caption_files = []

    for index, moment in enumerate(moments, start=1):

        clip_transcript = []

        for segment in transcript:
            if (
                segment["start"] >= moment["start"]
                and segment["end"] <= moment["end"]
            ):
                clip_transcript.append({
                    "start": segment["start"] - moment["start"],
                    "end": segment["end"] - moment["start"],
                    "text": segment["text"]
                })

        caption_path = f"clips/clip_{index}.srt"

        make_srt(
            clip_transcript,
            caption_path
        )

        caption_files.append(caption_path)

    return {
        "success": True,
        "language": analysis["language"],
        "clips": clips,
        "captions": caption_files,
        "moments": moments
    }
  
