from groq import Groq
import os


client = Groq(api_key=os.getenv("GROQ_API_KEY"))


messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]

while True:
    user_input = input("Chat with history: ")

    messages.append({"role": "user", "content": user_input})

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
    )


    assistant_response = chat_completion.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_response})

    print(assistant_response + "\n")