# Groq Chat Streamlit App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://groqdemo.streamlit.app/)

![Demo App Screenshot](/images/groq_demo.png)

This [Streamlit](https://streamlit.io/) app integrates with the [Groq API](https://groq.com/) to provide a chat interface where users can interact with advanced language models. It allows users to choose between two models for generating responses, enhancing the flexibility and user experience of the chat application.

It is blazing FAST, try it and see! 🏎️ 💨 💨 💨

**Check out the video tutorial 👇**

<a href="https://youtu.be/WQvinJGYk90">
  <img src="https://img.youtube.com/vi/WQvinJGYk90/hqdefault.jpg" alt="Watch the video" width="100%">
</a>

## Features

- **Model Selection**: Users can select between `mixtral-8x7b-32768` and `llama2-70b-4096` models to tailor the conversation according to the capabilities of each model.
- **Chat History**: The app maintains a session-based chat history, allowing for a continuous conversation flow during the app session.
- **Dynamic Response Generation**: Utilizes a generator function to stream responses from the Groq API, providing a seamless chat experience.
- **Error Handling**: Implements try-except blocks to gracefully handle potential errors during API calls.

## Requirements

- Streamlit
- Groq Python SDK
- Python 3.7+

## Setup and Installation

- **Install Dependencies**:

  ```bash
  pip install streamlit groq
  ```

- **Set Up Groq API Key**:

  Ensure you have an API key from Groq. This key should be stored securely using Streamlit's secrets management:

  ```toml
  # .streamlit/secrets.toml
  GROQ_API_KEY="your_api_key_here"
  ```

- **Run the App**:
  Navigate to the app's directory and run:

  ```bash
  streamlit run streamlit_app.py
  ```

## Usage

Upon launching the app, you are greeted with a title and a model selection dropdown.

After choosing a preferred model, you can start interacting with the chat interface by entering prompts.

The app displays both the user's questions and the AI's responses, facilitating a back-and-forth conversation.

## Customization

The app can be easily customized to include additional language models (as Groq adds more), alter the user interface, or extend the functionality to incorporate other types of interactions with the Groq API.

## Contributing

Contributions to enhance the app, fix bugs, or improve documentation are welcome.

Please feel free to fork the repository, make your changes, and submit a pull request.
