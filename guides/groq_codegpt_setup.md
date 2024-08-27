# Connecting Groq to CodeGPT on VSCode and Cursor
This guide explains how to use the [CodeGPT](https://codegpt.co/) AI Code Assistant extension available for the VSCode and Cursor IDEs with Large Language Models (LLMs) powered by [Groq](https://groq.com/). By the end of this guide, you'll have an AI Copilot that leverages Groq's lightning fast inference speed set up to enhance your productivity.

Let's get set up together with the steps below! 


### 1. Generate a Groq API Key
- Sign up for a free [GroqCloud account](https://console.groq.com/playground), generate a Groq API Key on our [console](https://console.groq.com/keys), and copy to your clipboard.

### 2. Install CodeGPT
- Open VSCode or Cursor and navigate to the "Extensions" marketplace and install the **CodeGPT: Chat & AI Agents** extension.

**Note:** The CodeGPT icon will appear on your sidebar.

### 3. Set Provider to Groq
- Open CodeGPT in VSCode or Cursor by clicking the icon and choose Groq as the provider under `PROVIDER`.

### 4. Select a Model Powered by Groq
- Under `MODEL`, select a model from the list of models available via Groq.

### 5. Set the Connection
- Click the `Set Connection` button that appears and paste your Groq API Key before clicking `Connect`. 


## Ready, Set, Code(GPT)!
Your IDE is now set up with CodeGPT and configured with LLMs powered by Groq for lightning-fast inference speed, which you can use to:

- **Generate comprehensive explanations for code file content:** Type `/Explain` in the CodeGPT input field, use `@` to select a file from your project directory, and press Enter. 
- **Generate documentation**: Type `/Document` to automatically generate documentation for all the code in a selected file.
- **Receive AI assistance via a chat interface:** Use the CodeGPT sidebar to open the chat interface and type a question or request coding help directly in the chat for AI-assisted answers, suggestions, and code snippets.
- **AI-powered code completions:** Start typing your code and CodeGPT powered by Groq will instantly suggest completions based on context that you can press `Tab` or `Enter` to accept.
- **Generate unit tests for your functions:** Highlight a function or method in your code and use the `/GenerateTest` command in the CodeGPT input field to generate unit tests.
- **Receive convenient explanations for code snippets:** Highlight a code snippet and right-click to select "Explain Code" from the CodeGPT menu to generate a detailed explanation for it.
- **Generate code snippets:** Describe the code you need in the CodeGPT input field, such as "Create a Python function to sort a list", and press Enter to generate your requested code snippet.
- **Translate code to different coding languages:** Paste your code into the CodeGPT input field and specify the target language (e.g. "Translate this Python code to JavaScript") for the Groq-powered LLM to translate your code to the target language.
- **Auto-generate in-line comments:** Highlight a block of code and select the "Generate Comments" option from the CodeGPT menu to insert comments for code readability.
- **Explore popular code snippets:** Use the `/ExploreSnippets` command to browse through a list of commonly used code snippets that you can then select and insert directly into your code.

As you can see (and will now experience), CodeGPT powered by Groq is like having a Senior Software Engineer right at your fingertips! For additional information about the complete list of features available, see [the CodeGPT documentation](https://docs.codegpt.co/docs/tutorial-features/chat_code_gpt). 