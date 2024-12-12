import asyncio
from groq import AsyncGroq



async def main() -> None:
  

    client = AsyncGroq()

    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
    ]

    while True:
        user_input = input("Chat with history: ")
        # append user input
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
        # append llm input
        messages.append({"role": "assistant", "content": assistant_response})

        print(assistant_response + "\n")

asyncio.run(main())