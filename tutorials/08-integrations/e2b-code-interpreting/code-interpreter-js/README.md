# AI Code Execution with Groq

This AI data analyst can plot a linear regression chart based on CSV data. It uses [LLMs powered by Groq](https://wow.groq.com/wp-content/uploads/2023/11/Groq_LLMs_OnePager.pdf), and the [Code Interpreter SDK](https://github.com/e2b-dev/code-interpreter) by E2B for the code interpreting capabilities. The SDK quickly creates a secure cloud sandbox powered by [Firecracker](https://github.com/firecracker-microvm/firecracker). Inside this sandbox is a running Jupyter server that the LLM can use.

Read more about models powered by Groq [here](https://console.groq.com/docs/models).

The AI agent performs a data analysis task on an uploaded CSV file, executes the AI-generated code in the sandboxed environment by E2B, and returns a chart, saving it as a PNG file. The code is processing the data in the CSV file, cleaning the data, and performing the assigned analysis, which includes plotting a chart.

# How to start

## 1. Install dependencies

Ensure all dependencies are installed:

```
npm install
```

## 2. Set up environment variables

Create a `.env` file in the project root directory and add your API keys:

- Copy `.env.template` to `.env`
- Get the [E2B API KEY](https://e2b.dev/docs/getting-started/api-key)
- Get the [GROQ API KEY](https://console.groq.com/keys)

## 3. Choose your LLM

In the `index.ts` file, uncomment the model of your choice.

See the complete list of models powered by Groq [here](https://console.groq.com/docs/models).

## 4. Run the program

```
npm run start
```

The script performs the following steps:
    
- Loads the API keys from the environment variables.
- Uploads the CSV dataset to the E2B sandboxed cloud environment.
- Sends a prompt to the model to generate Python code for analyzing the dataset.
- Executes the generated Python code using the E2B Code Interpreter SDK.
- Saves any generated visualization as a PNG file.
  

After running the program, you should get the result of the data analysis task saved in an `image_1.png` file. You should see a plot like this:

![Example of the output](image_1.png)


# Connect with E2B & learn more
If you encounter any problems, please let us know at our [Discord](https://discord.com/invite/U7KEcGErtQ).

Check the [E2B documentation](https://e2b.dev/docs) to learn more about how to use the Code Interpreter SDK.