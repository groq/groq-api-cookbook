# Website Guru

Website Guru is a Streamlit application that allows you to interact with and ask questions about a given website using Large Language Models (LLMs). The app uses a combination of document loading, text splitting, vector storage, and retrieval chains to generate accurate responses based on the content of the specified website.

## Features

- Load and process web pages to extract information.
- Utilize advanced language models to answer questions about the content.
- Provide a user-friendly interface with Streamlit.

## Requirements

- Python 3.7 or higher
- Streamlit
- langchain
- langchain_groq
- langchain_community
- sentence-transformers
- faiss-cpu
- python-dotenv
- bs4

## Installation

1. Install the required Python packages:
	
	pip install -r requirements.txt

2. Create a .env file in the project directory and add your Groq API key:

	GROQ_API_KEY=your_groq_api_key

## Usage

1. Run the Streamlit app:

	streamlit run app.py

2. Open your web browser and go to http://localhost:8501.

3. Enter the website address you want to analyze and select LLM of your choice.

4. Type your question in the provided input box and click the "Submit" button.

## Project Structure

1. app.py: The main Streamlit application script.

2. requirements.txt: List of required Python packages.

3. .env: Environment file containing API keys (not included in the repository for security reasons).

## How It Works

1. Web Page Input: The user inputs a website address.

2. Model Selection: The user selects a language model to use.

3. Question Input: The user types a question related to the website content.

4. Document Processing:

	*) The app loads the website content. 

	*) The content is split into manageable chunks.

	*) Embeddings are created from the text chunks.

	*) The chunks are stored and queried using a vector store (FAISS)

5. Response Generation: The app generates a response using the selected language model and displays it to the user.

## Acknowledgements

1. Streamlit

2. LangChain

3. Hugging Face

4. FAISS
