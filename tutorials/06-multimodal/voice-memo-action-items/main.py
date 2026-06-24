"""
Turn a voice memo into structured action items with Groq.

A two-step, pure-Groq pipeline:
  1. Transcribe the audio with Whisper (whisper-large-v3-turbo).
  2. Extract a summary and structured action items from the transcript with a
     Groq LLM in JSON mode (llama-3.3-70b-versatile).

No GPU and no local models, just two API calls.

Setup:
    pip install -r requirements.txt
    export GROQ_API_KEY="your_key"   # free key: https://console.groq.com/keys

Run:
    python main.py path/to/voice-memo.mp3
"""

import argparse
import json
import os

from groq import Groq

TRANSCRIBE_MODEL = "whisper-large-v3-turbo"
EXTRACT_MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = (
    "You extract structured action items from a meeting or voice-memo transcript. "
    "Return ONLY JSON matching this shape:\n"
    '{"summary": string, '
    '"action_items": [{"task": string, "owner": string or null, '
    '"due": string or null, "priority": "high" | "medium" | "low"}]}\n'
    "Use null for an owner or due date that is not stated. Do not invent details."
)


def transcribe(client, path):
    """Step 1: audio -> text with Groq Whisper."""
    with open(path, "rb") as audio:
        result = client.audio.transcriptions.create(
            file=(os.path.basename(path), audio.read()),
            model=TRANSCRIBE_MODEL,
            response_format="verbose_json",
            temperature=0.0,
        )
    return (getattr(result, "text", "") or "").strip()


def extract_action_items(client, transcript):
    """Step 2: transcript -> structured JSON with a Groq LLM in JSON mode."""
    response = client.chat.completions.create(
        model=EXTRACT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": transcript},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    return json.loads(response.choices[0].message.content)


def main():
    parser = argparse.ArgumentParser(
        description="Turn a voice memo into structured action items with Groq."
    )
    parser.add_argument("audio", help="Path to an audio file (mp3, wav, m4a, ...).")
    args = parser.parse_args()

    if not os.environ.get("GROQ_API_KEY"):
        raise SystemExit("Set GROQ_API_KEY first (free key: https://console.groq.com/keys).")
    if not os.path.isfile(args.audio):
        raise SystemExit(f"Audio file not found: {args.audio}")

    client = Groq(api_key=os.environ["GROQ_API_KEY"])

    transcript = transcribe(client, args.audio)
    if not transcript:
        raise SystemExit("No speech detected in the audio.")
    print("Transcript:\n" + transcript + "\n")

    result = extract_action_items(client, transcript)
    print("Summary:", result.get("summary", ""))
    print("\nAction items:")
    for item in result.get("action_items", []):
        owner = item.get("owner") or "unassigned"
        due = item.get("due") or "no date"
        print(f"  [{item.get('priority', '?'):>6}] {item.get('task')}  ({owner}, {due})")


if __name__ == "__main__":
    main()
