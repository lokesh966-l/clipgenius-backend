
import os
import subprocess


def create_clip(video_path, start, end, output_path):
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    duration = end - start

    command = [
        "ffmpeg",
        "-y",
        "-ss", str(start),
        "-i", video_path,
        "-t", str(duration),
        "-vf",
        "scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-c:a", "aac",
        "-movflags", "+faststart",
        output_path
    ]

    subprocess.run(command, check=True)

    return output_path


def create_multiple_clips(video_path, moments):
    os.makedirs("clips", exist_ok=True)

    results = []

    for index, moment in enumerate(moments, start=1):
        output = f"clips/clip_{index}.mp4"

        create_clip(
            video_path,
            moment["start"],
            moment["end"],
            output
        )

        results.append(output)

    return results
  
