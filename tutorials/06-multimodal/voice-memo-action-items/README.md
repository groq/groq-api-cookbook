# Turn a voice memo into structured action items with Groq

A flat transcript of a meeting or voice memo still leaves you with work to do:
someone has to read it and pull out who needs to do what, by when. This tutorial
automates that with a two-step, pure-Groq pipeline that takes an audio file and
returns clean, structured action items as JSON.

1. **Transcribe** the audio with Whisper (`whisper-large-v3-turbo`).
2. **Extract** a summary and structured action items from the transcript with a
   Groq LLM (`llama-3.3-70b-versatile`) in **JSON mode**.

Both steps run on Groq - no GPU, no local models, just two API calls.

## Why Groq

- **One provider, one client** for both speech-to-text and the language model.
- **JSON mode** (`response_format={"type": "json_object"}`) guarantees the
  extraction step returns valid, parseable JSON - no brittle string scraping.
- **Fast and serverless:** hosted Whisper plus a hosted LLM means the whole
  pipeline runs anywhere Python does.

## Prerequisites

```bash
pip install -r requirements.txt
export GROQ_API_KEY="your_key"   # free key: https://console.groq.com/keys
```

## Step 1 - Transcribe the audio

```python
import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

with open("voice-memo.mp3", "rb") as audio:
    result = client.audio.transcriptions.create(
        file=("voice-memo.mp3", audio.read()),
        model="whisper-large-v3-turbo",
        response_format="verbose_json",
    )

transcript = result.text
```

## Step 2 - Extract structured action items in JSON mode

Give the model a clear output shape and turn on JSON mode so the response is
always valid JSON:

```python
import json

SYSTEM_PROMPT = (
    "You extract structured action items from a meeting or voice-memo transcript. "
    "Return ONLY JSON matching this shape:\n"
    '{"summary": string, '
    '"action_items": [{"task": string, "owner": string or null, '
    '"due": string or null, "priority": "high" | "medium" | "low"}]}\n'
    "Use null for an owner or due date that is not stated. Do not invent details."
)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": transcript},
    ],
    response_format={"type": "json_object"},
    temperature=0,
)

data = json.loads(response.choices[0].message.content)
```

## Run it

```bash
python main.py path/to/voice-memo.mp3
```

For a short standup recording, the script prints the transcript and then the
structured result:

```
Summary: Team sync to discuss Q3 budget, vendor shipment, and landing page copy

Action items:
  [  high] Finalize Q3 budget  (Priya, Friday)
  [  high] Email vendor about delayed shipment  (Arjun, today)
  [medium] Update landing page copy  (unassigned, next week)
  [   low] Schedule follow-up call  (unassigned, Monday)
```

Because the second step returns JSON, you can drop the result straight into the
rest of your stack instead of parsing prose.

## Where to go next

- **Enforce a schema:** validate `data` with Pydantic, or use the
  [Instructor tutorial](/tutorials/05-structured-output/structured-output-instructor)
  in this cookbook to bind the output to typed objects.
- **Push it somewhere:** send each action item to a task tracker, a calendar, or
  a Slack message.
- **Longer recordings:** for long audio, transcribe in chunks first (see the
  [Audio Chunking tutorial](/tutorials/06-multimodal/audio-chunking)), then run
  the full transcript through Step 2.

## Files

- `main.py` - runnable CLI: audio in, transcript and structured action items out.
- `requirements.txt` - the single `groq` dependency.
