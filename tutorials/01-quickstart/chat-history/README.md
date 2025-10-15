# A guide on implementing chat history in your Groq based LLM applications
This directory aims to provide a reference to those who wish to implement chat history in their LLM applications built on the groq platform.

## What's chat history ?
Chat history is a feature that helps your LLM remember previous queries and answers, this aids you in building applications with a larger sense of context and hence improving over all quality of outputs from the LLM.

## How is it implemented ?
Via simple json, the directory has 6 `.py` files, each with an example inspired by [ollama](https://ollama.com/) and the [groq-python SDK](https://github.com/groq/groq-python). You can either have session based history that the LLM forgets when the session is closed, or write to a `.json` file so that you can use the saved chat history across multiple sessions.

## Usage
You will need to store a valid Groq API Key as a secret to proceed with this example. You can generate one for free [here](https://console.groq.com/keys).

You can then set your api credentials and simple `python3 <filename>.py` to see how history works. \
E.g:
```
user: Why is the sky blue?
llm: The sky appears blue because molecules in Earth's atmosphere scatter shorter blue wavelengths of sunlight more than longer wavelengths like red.
user: What was my previous question?
llm: Your previous question was: 'Why is the sky blue?'
```
## What next?
Now that you know how chat history can be implemented, you can include this feature with RAG or multi-modal LLMs to solve real world problems!

### Note: The length of the chat history also depends on the context length of the LLM you're using