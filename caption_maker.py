
import os


def make_srt(transcript, output_path="captions.srt"):
    def timestamp(seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds - int(seconds)) * 1000)

        return (
            f"{hours:02}:{minutes:02}:"
            f"{secs:02},{milliseconds:03}"
        )

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        for index, segment in enumerate(transcript, start=1):
            file.write(f"{index}\n")
            file.write(
                f"{timestamp(segment['start'])} --> "
                f"{timestamp(segment['end'])}\n"
            )
            file.write(segment["text"] + "\n\n")

    return output_path
  
