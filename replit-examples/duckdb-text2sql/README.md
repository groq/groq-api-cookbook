# DuckDB Text-to-SQL

A command line application that allows users to ask questions about their DuckDB data. The application uses the Groq API to generate SQL queries based on the user's questions and execute them on a DuckDB database.

## Features

- **Text-to-SQL**: The application uses natural language processing to convert user questions into SQL queries, making it easy for users to query their data without knowing SQL.

- **Error Handling**: If the AI generates an invalid SQL query, the application prompts the AI to correct its response, ensuring that the output is a valid DuckDB SQL query.

- **Data Summarization**: After executing a SQL query, the application uses the AI to summarize the resulting data in relation to the user's original question.

- **Customization**: Users can customize the AI model used, the maximum number of reflections (attempts to correct an invalid response), and the length of the conversational memory.

## Data

The application queries data from two CSV files located in the `data` folder:

- `employees.csv`: Contains employee data including their ID, full name, and email address.

- `purchases.csv`: Records purchase details including purchase ID, date, associated employee ID, amount, and product name.

## Prompts

The base prompt for the AI is stored in a text file in the `prompts` folder:

- `base_prompt.txt`

## Functions

- `chat_with_groq()`: Sends a prompt to the Groq API and returns the AI's response.
- `execute_duckdb_query()`: Executes a SQL query on a DuckDB database and returns the result.
- `get_json_output()`: Extracts and formats the SQL query or error message from the AI's response.
- `get_reflection()`: Prompts the AI to correct an invalid response.
- `get_summarization()`: Generates a prompt for the AI to summarize the data resulting from a SQL query.
- `main()`: The main function of the application, which handles user input and controls the flow of the application.

## Usage

You can [fork and run this application on Replit](https://replit.com/@GroqCloud/DuckDB-Text-to-SQL) or run it on the command line with `python main.py`

## Customizing with Your Own Data

This application is designed to be flexible and can be easily customized to work with your own data. If you want to use your own data, follow these steps:

1. **Replace the CSV files**: The application queries data from two CSV files located in the `data` folder: `employees.csv` and `purchases.csv`. Replace these files with your own CSV files.

2. **Modify the base prompt**: The base prompt for the AI, stored in the `prompts` folder as `base_prompt.txt`, contains specific information about the data metadata. Modify this prompt to match the structure and content of your own data. Make sure to accurately describe the tables, columns, and any specific rules or tips for querying your dataset.

By following these steps, you can tailor the DuckDB Query Generator to your own data and use cases. Feel free to experiment and build off this repository to create your own powerful data querying applications.
