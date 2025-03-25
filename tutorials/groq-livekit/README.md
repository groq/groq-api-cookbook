# Groq with LiveKit Agents

This project demonstrates a voice-enabled AI assistant using Groq, LiveKit, and a voice-based interface for kitchen chef interactions.

Prerequisites
- Python 3.12
- pnpm (for frontend)
- API keys from Groq & Livekit

Environment setup:

Create a `.env file` in the `agent/` folder directory with the following variables:
```
LIVEKIT_URL=XXXXXX
LIVEKIT_API_KEY=XXXXXX
LIVEKIT_API_SECRET=XXXXXX
GROQ_API_KEY=XXXXXX
```

Create a `.env.local` file in the `client/web/` folder directory with:
```
# LiveKit API Configuration
LIVEKIT_API_KEY=YOUR_API_KEY
LIVEKIT_API_SECRET=YOUR_API_SECRET

# Public configuration
NEXT_PUBLIC_LIVEKIT_URL=wss://YOUR_LIVEKIT_URL
```

Valid API keys for Groq and other services

# Code

## Installation and Running the Project

### Backend Setup (Agent)

1. Navigate to the agent directory:
   ```bash
   cd agent
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the agent:
   ```bash
   python main.py dev
   ```

### Frontend Setup (Web Client)

1. Navigate to the web client directory:
   ```bash
   cd client/web
   ```

2. Install dependencies:
   ```bash
   pnpm install
   ```

3. Start the development server:
   ```bash
   pnpm dev
   ```

## Accessing the Application

Open a web browser and navigate to:
- `http://localhost:3000`


# Python Backend Code Walkthrough:
Takes place in `main.py`

### Import the required packages
```
from livekit.agents import JobContext, WorkerOptions, cli, JobProcess, AutoSubscribe
from livekit.agents.llm import (
    ChatContext,
    ChatMessage,
)
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import silero, groq

from dotenv import load_dotenv

load_dotenv()
```

### Setup the System Prompt & Choose the Speech-in, LLM, and Speech-out models
```

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    initial_ctx = ChatContext(
        messages=[
            ChatMessage(
                role="system",
                content="You are an assistant that answers kitchen chef questions. Be nice. Respond in full words and plain text, without styling words or special characters.",
            )
        ]
    )

    assistant = VoiceAssistant(
        vad=ctx.proc.userdata["vad"],
        stt=groq.STT(), # uses whisper
        llm=groq.LLM(
            model="llama3-8b-8192",
            # tool_choice="" # optional tool calling
        ),
        tts=groq.TTS(
            voice="Chip-PlayAI", # see all voices here: https://console.groq.com/playground?model=playai-tts
        ),
        chat_ctx=initial_ctx,
    )

    assistant.start(ctx.room)
    await assistant.say("Hi there, how are you doing today?", allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))

```

The full code files (frontend & backend) can be found within the `groq-livekit-code` folder.