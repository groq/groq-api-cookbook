from groq import Groq



client = Groq()


messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]

while True:
    user_input = input("Chat with history: ")

    messages.append({"role": "user", "content": user_input})

    chat_completion = client.chat.completions.create(
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

    print(assistant_response + "\n")