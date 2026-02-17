from typing import List, Dict

def format_transcript(segments: List[Dict]) -> str:
    lines = []
    for seg in segments:
        speaker = (seg.get("speaker") or "Unknown").strip()
        text = (seg.get("text") or "").strip()
        if not text or text == "...":
            continue
        lines.append(f"{speaker}: {text}")
    return "\n".join(lines)
