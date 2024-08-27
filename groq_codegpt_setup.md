# Groq CodeGPT Setup Guide
This guide explains how to use the CodeGPT extension in Visual Studio Code with large language models hosted on Groq's hardware. By the end of this guide, you'll have an AI-driven coding assistant set up to enhance your productivity, leveraging Groq's inference speed technology for faster performance.

## What is CodeGPT?
**CodeGPT** is a powerful extension for Visual Studio Code that acts as your pair-programming partner, helping you code more efficiently. It offers AI chat assistance, auto-completion, code explanation, error-checking, and much more. CodeGPT can utilize LLMs hosted on Groq's hardware to deliver a superior coding experience. With **CodeGPT Plus**, you can access expert AI agents that assist in writing better code, all within your code editor.

## How to Use CodeGPT in Visual Studio Code
### 1. Create a GroqCloud Account
- Sign up for a free [GroqCloud account](https://console.groq.com/playground) and generate a Groq API key on the [console](https://console.groq.com/keys)

### 2. Install CodeGPT
- Open Visual Studio Code and navigate to the "Extensions" marketplace and install the **CodeGPT** extension
- After installation, a CodeGPT icon should appear in your sidebar and command palette

### 3. Connect CodeGPT to Groq
- In CodeGPT, choose Groq as the provider for accessing LLMs, click 'Connect,' and enter your API Key.

### 4. Select a Groq Model
- Select an LLM from the list of models available through Groq in CodeGPT.



## What You Can Do with CodeGPT Using Groq
Once you have set up CodeGPT with Groq, you can take advantage of several powerful features directly within Visual Studio Code:
 [Discover more features of this extension](https://docs.codegpt.co/docs/tutorial-features/chat_code_gpt)

#### Explain a File
- Type `/Explain` in the CodeGPT input field and use `@` to select a file from your project directory.
- Press Enter, and the selected LLM will generate a comprehensive explanation of the file's content.

#### Document a File
- Type `/Document` to automatically generate documentation for all the code in a selected file.

#### AI Chat Assistance
- Use the CodeGPT sidebar to open the chat interface and type a question or request coding help directly in the chat.
- The LLM will provide answers, suggestions, or code snippets to assist you.

#### Code Completion
- Start typing your code, and CodeGPT will suggest completions based on context.
- Press `Tab` or `Enter` to accept a suggestion and insert it into your code.

#### Generate Unit Tests
- Highlight a function or method in your code.
- Use the `/GenerateTest` command in the CodeGPT input field.
- The LLM will create a unit test for the selected function or method.

#### Explain Code Snippets
- Highlight a code snippet and right-click to select "Explain Code" from the CodeGPT menu.
- The LLM will generate a detailed explanation of the highlighted code.

#### Generate Code Snippets
- Describe the code you need in the CodeGPT input field, such as "Create a Python function to sort a list."
- Press Enter, and the LLM will generate the requested code snippet.

#### Translate Code Between Languages
- Paste your code into the CodeGPT input field and specify the target language, e.g., "Translate this Python code to JavaScript."
- The LLM will translate your code into the desired programming language.

#### Auto-Generate Comments
- Highlight a block of code and select the "Generate Comments" option from the CodeGPT menu.
- The LLM will insert comments that explain the purpose and functionality of the code.

#### Explore Code Snippets
- Use the `/ExploreSnippets` command to browse through a list of commonly used code snippets.
- Select a snippet to insert it directly into your code.


## Additional Resources
- [Create an account at this link](https://codegpt.co)
- [Discover more features of this extension](https://docs.codegpt.co/docs/tutorial-features/chat_code_gpt)
