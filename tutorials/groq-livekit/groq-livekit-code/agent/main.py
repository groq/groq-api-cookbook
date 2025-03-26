from livekit.agents import JobContext, WorkerOptions, cli, JobProcess, AutoSubscribe
from livekit.agents.llm import (
    ChatContext,
    ChatMessage,
)
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import silero, groq

from dotenv import load_dotenv

load_dotenv()


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
        stt=groq.STT(),
        llm=groq.LLM(
            model="llama3-8b-8192",
            # tool_choice=""
        ),
        tts=groq.TTS(
            voice="Chip-PlayAI",
        ),
        chat_ctx=initial_ctx,
    )

    assistant.start(ctx.room)
    await assistant.say("Hi there, how are you doing today?", allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
