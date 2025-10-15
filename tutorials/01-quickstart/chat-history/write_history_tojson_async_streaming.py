import asyncio
import json
import os
from pathlib import Path
from groq import AsyncGroq

HISTORY_FILE = 'chat_history.json'

async def load_history():
    history_path = Path(HISTORY_FILE)
    if history_path.exists():
        try:
            with open(history_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return [{"role": "system", "content": "You are a helpful assistant."}]
    else:
        return [{"role": "system", "content": "You are a helpful assistant."}]

async def save_history(messages):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(messages, f, indent=2)

async def main() -> None:
    messages = await load_history()
    client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

    try:
        while True:
            user_input = input("Chat with history: ")
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                break

            messages.append({"role": "user", "content": user_input})

            stream = await client.chat.completions.create(
                messages=messages,
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                temperature=0.5,
                max_tokens=1024,
                top_p=1,
                stop=None,
                stream=True,
            )

            assistant_response = ""
            async for chunk in stream:
                delta_content = chunk.choices[0].delta.content
                if delta_content:
                    assistant_response += delta_content
                    print(delta_content, end="")

                if chunk.choices[0].finish_reason:
                    if chunk.x_groq is not None and chunk.x_groq.usage is not None:
                        print(f"\n\nUsage stats: {chunk.x_groq.usage}")
                    break

            messages.append({"role": "assistant", "content": assistant_response})
            await save_history(messages)
            print("\n")

    except KeyboardInterrupt:
        print("\nChat session interrupted.")
    finally:
        await save_history(messages)

if __name__ == "__main__":
    asyncio.run(main())