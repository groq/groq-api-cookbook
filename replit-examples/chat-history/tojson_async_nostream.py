import asyncio
import json
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
    client = AsyncGroq()

    try:
        while True:
            user_input = input("Chat with history: ")
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                break

            messages.append({"role": "user", "content": user_input})

            chat_completion = await client.chat.completions.create(
                messages=messages,
                model="mixtral-8x7b-32768",
                temperature=0.5,
                max_tokens=1024,
                top_p=1,
                stop=None,
                stream=False,
            )

            assistant_response = chat_completion.choices[0].message.content
            messages.append({"role": "assistant", "content": assistant_response})
            
            await save_history(messages)
            print(assistant_response + "\n")

    except KeyboardInterrupt:
        print("\nChat session interrupted.")
    finally:
        await save_history(messages)

if __name__ == "__main__":
    asyncio.run(main())