# Presidential Speeches RAG

This repository contains a command line application that allows users to ask questions about US presidents. The application uses a pre-trained model to find relevant excerpts from presidential speeches and generate responses to the user's questions.

## Features

- **Question-Answering System**: Users can ask questions about US presidents, and the application will generate responses based on relevant excerpts from presidential speeches.

- **Customization**: Users can provide additional context for the model and choose from a list of pre-trained models.

- **Similarity Search**: The application uses a Pinecone vector store to find the most relevant excerpts from presidential speeches based on the user's question.

## Code Overview

The main script of the application is [main.py](./main.py). Here's a brief overview of its main functions:

- `get_relevant_excerpts(user_question, docsearch)`: This function takes a user's question and a Pinecone vector store as input, performs a similarity search on the vector store using the user's question, and returns the most relevant excerpts from presidential speeches.

- `get_relevant_excerpts(user_question, docsearch)`: This function takes a user's question and a Pinecone vector store as input, performs a similarity search on the vector store using the user's question, and returns the most relevant excerpts from presidential speeches.

- `presidential_speech_chat_completion(client, model, user_question, relevant_excerpts, additional_context)`: This function takes a Groq client, a pre-trained model, a user's question, relevant excerpts from presidential speeches, and additional context as input. It generates a response to the user's question based on the relevant excerpts and the additional context

## Usage

You can [fork and run this application on Replit](https://replit.com/@GroqCloud/Presidential-Speeches-RAG) or run it on the command line with `python main.py`
