import streamlit as st
import pandas as pd
import numpy as np
from groq import Groq
from pinecone import Pinecone

from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_pinecone import PineconeVectorStore


def get_relevant_excerpts(user_question, docsearch):
    """
    This function retrieves the most relevant excerpts from presidential speeches based on the user's question.

    Parameters:
    user_question (str): The question asked by the user.
    docsearch (PineconeVectorStore): The Pinecone vector store containing the presidential speeches.

    Returns:
    str: A string containing the most relevant excerpts from presidential speeches.
    """

    # Perform a similarity search on the Pinecone vector store using the user's question
    relevent_docs = docsearch.similarity_search(user_question)

    # Extract the page content from the top 3 most relevant documents and join them into a single string
    relevant_excerpts = '\n\n------------------------------------------------------\n\n'.join([doc.page_content for doc in relevent_docs[:3]])

    return relevant_excerpts


def presidential_speech_chat_completion(client, model, user_question, relevant_excerpts, additional_context):
    """
    This function generates a response to the user's question using a pre-trained model.

    Parameters:
    client (Groq): The Groq client used to interact with the pre-trained model.
    model (str): The name of the pre-trained model.
    user_question (str): The question asked by the user.
    relevant_excerpts (str): A string containing the most relevant excerpts from presidential speeches.
    additional_context (str): Additional context provided by the user.

    Returns:
    str: A string containing the response to the user's question.
    """

    # Define the system prompt
    system_prompt = '''
    You are a presidential historian. Given the user's question and relevant excerpts from 
    presidential speeches, answer the question by including direct quotes from presidential speeches. 
    When using a quote, site the speech that it was from (ignoring the chunk).
    '''

    # Add the additional context to the system prompt if it's not empty
    if additional_context != '':
        system_prompt += '''\n
        The user has provided this additional context:
        {additional_context}
        '''.format(additional_context=additional_context)

    # Generate a response to the user's question using the pre-trained model
    chat_completion = client.chat.completions.create(
        messages = [
            {
                "role": "system",
                "content":  system_prompt
            },
            {
                "role": "user",
                "content": "User Question: " + user_question + "\n\nRelevant Speech Exerpt(s):\n\n" + relevant_excerpts,
            }
        ],
        model = model
    )
    
    # Extract the response from the chat completion
    response = chat_completion.choices[0].message.content

    return response


def main():
    """
    This is the main function that runs the application. It initializes the Groq client and the SentenceTransformer model,
    gets user input from the Streamlit interface, retrieves relevant excerpts from presidential speeches based on the user's question,
    generates a response to the user's question using a pre-trained model, and displays the response.
    """

    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Initialize the Groq client
    groq_api_key = st.secrets["GROQ_API_KEY"]
    pinecone_api_key=st.secrets["PINECONE_API_KEY"]
    pinecone_index_name = "presidential-speeches"
    client = Groq(
        api_key=groq_api_key
    )

    pc = Pinecone(api_key = pinecone_api_key)
    docsearch = PineconeVectorStore(index_name=pinecone_index_name, embedding=embedding_function)

    # Display the Groq logo
    spacer, col = st.columns([5, 1])  
    with col:  
        st.image('groqcloud_darkmode.png')

    # Display the title and introduction of the application
    st.title("Presidential Speeches RAG")
    multiline_text = """
    Welcome! Ask questions about U.S. presidents, like "What were George Washington's views on democracy?" or "What did Abraham Lincoln say about national unity?". The app matches your question to relevant excerpts from presidential speeches and generates a response using a pre-trained model.
    """

    st.markdown(multiline_text, unsafe_allow_html=True)

    # Add customization options to the sidebar
    st.sidebar.title('Customization')
    additional_context = st.sidebar.text_input('Enter additional summarization context for the LLM here (i.e. write it in spanish):')
    model = st.sidebar.selectbox(
        'Choose a model',
        ['llama3-8b-8192', 'mixtral-8x7b-32768', 'gemma-7b-it']
    )

    # Get the user's question
    user_question = st.text_input("Ask a question about a US president:")

    if user_question:
        pinecone_index_name = "presidential-speeches"
        relevant_excerpts = get_relevant_excerpts(user_question, docsearch)
        response = presidential_speech_chat_completion(client, model, user_question, relevant_excerpts, additional_context)
        st.write(response)



if __name__ == "__main__":
    main()



