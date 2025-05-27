import asyncio
import os
from groq import AsyncGroq

async def main() -> None:

    client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))


    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
    ]

    while True:
        user_input = input("Chat with history: ")

        messages.append({"role": "user", "content": user_input})

    
        stream = await client.chat.completions.create(
            messages=messages,
            model="meta-llama/llama-4-scout-17b-16e-instruct", # any llm from groq
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
                assert chunk.x_groq is not None
                assert chunk.x_groq.usage is not None
                print(f"\n\nUsage stats: {chunk.x_groq.usage}")

   
        messages.append({"role": "assistant", "content": assistant_response})
        print("\n")

asyncio.run(main())
