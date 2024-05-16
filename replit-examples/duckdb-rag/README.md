# DuckDB Query Retriever

A command line application that allows users to ask questions about their DuckDB data using the Groq API. The application uses pre-verified SQL queries and their descriptions stored in YAML files to find the most similar query to the user's question, execute it against the data, and return the results (if a prompt is not similar to a vetted query, no data will be returned).

## Features

- **Semantic Search**: The application uses semantic search to find the most similar pre-verified SQL query to the user's question.

- **Data Querying**: The application executes the selected SQL query on a DuckDB database and displays the result.

- **Data Summarization**: After executing a SQL query, the application uses the Groq API to summarize the resulting data in relation to the user's original question.

- **Customization**: Users can customize the SentenceTransformer model used for semantic search, the Groq model used for summarization, and the minimum similarity threshold for selecting a verified SQL query.

## Data

The application queries data from CSV files located in the [data](app.py#L96) folder:

- `employees.csv`: Contains employee data including their ID, full name, and email address.

- `purchases.csv`: Records purchase details including purchase ID, date, associated employee ID, amount, and product name.

## Verified Queries

The verified SQL queries and their descriptions are stored in YAML files located in the `verified-queries` folder. Descriptions are used to semantically map prompts to queries:

- `most-recent-purchases.yaml`: Returns the 5 most recent purchases

- `most-expensive-purchase.yaml`: Finds the most expensive purchases

- `number-of-teslas.yaml`: Counts the number of Teslas purchased

- `employees-without-purchases.yaml`: Gets employees without any recent purchases

## Functions

- `get_verified_queries_and_embeddings(directory_path, embedding_model)`: Reads YAML files from the specified directory, loads the verified SQL queries and their descriptions, and generates embeddings for the descriptions using the provided SentenceTransformer model.

- `get_verified_sql(embedding_model, user_question, verified_queries_dict, minimum_similarity)`: Generates an embedding for the user's question, calculates the cosine similarity between the question's embedding and the embeddings of the verified queries, and returns the SQL of the most similar query if its similarity is above the specified minimum similarity threshold.

- `chat_with_groq(client, prompt, model)`: Sends a chat message to the Groq API and returns the content of the response.

- `execute_duckdb_query(query)`: Executes the provided SQL query using DuckDB and returns the result as a DataFrame.

- `get_summarization(client, user_question, df, model, additional_context`: Generates a prompt that includes the user's question and the DataFrame result, sends the prompt to the Groq API for summarization, and returns the summarized response.

- `main()`: The main function of the application, which initializes the Groq client and the SentenceTransformer model, gets user input from the interface, retrieves and executes the most similar verified SQL query, and displays the result and its summarization.

## Usage

You can [fork and run this application on Replit](https://replit.com/@GroqCloud/DuckDB-SQL-RAG) or run it on the command line with `python main.py`

## Customizing with Your Own Data

This application is designed to be flexible and can be easily customized to work with your own data. If you want to use your own data, follow these steps:

1. **Replace the CSV files**: The application queries data from CSV files located in the `data` folder. Replace these files with your own CSV files.

2. **Modify the verified queries**: The verified SQL queries and their descriptions are stored in YAML files located in the `verified-queries` folder. Replace these files with your own verified SQL queries and descriptions.

By following these steps, you can tailor the DuckDB Query Retriever to your own data and use cases. Feel free to experiment and build off this repository to create your own powerful data querying applications.
