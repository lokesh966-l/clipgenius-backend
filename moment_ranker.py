
import re


KEYWORDS = {
    "excitement": [
        "wow", "amazing", "unbelievable", "oh my god",
        "no way", "incredible", "अरे", "वाह", "गजब"
    ],
    "funny": [
        "haha", "hahaha", "lol", "funny",
        "comedy", "joke", "मजाक", "हंसी"
    ],
    "action": [
        "attack", "fight", "kill", "win", "lose",
        "enemy", "clutch", "मार", "जीत", "हार"
    ]
}


def score_moment(text):
    text = text.lower()
    score = 0

    for words in KEYWORDS.values():
        for word in words:
            if word in text:
                score += 3

    if "!" in text:
        score += 2

    if "?" in text:
        score += 1

    if re.search(r"\b(no way|oh my god|what happened)\b", text):
        score += 3

    return score


def find_moments(segments, duration=45, limit=5):
    candidates = []

    if not segments:
        return []

    video_end = segments[-1]["end"]
    start = 0

    while start < video_end:
        end = min(start + duration, video_end)

        if end - start < 30:
            break

        selected = [
            s for s in segments
            if s["start"] < end and s["end"] > start
        ]

        text = " ".join(s["text"] for s in selected)
        score = score_moment(text)

        candidates.append({
            "start": round(start, 2),
            "end": round(end, 2),
            "score": score,
            "text": text
        })

        start += 15

    candidates.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return candidates[:limit]
  
