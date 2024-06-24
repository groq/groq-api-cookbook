## How to use Langroid Multi-Agent Framework with Groq

[Langroid](https://github.com/langroid/langroid) is an
open-source Python framework that simplifies building LLM applications, 
using a Multi-Agent paradigm.

You can now use Langroid with Groq, by setting the model name to 
`groq/<model>`, e.g., `groq/llama3-70b-8192`.

To get started, create a virtual environment using Python 3.11 and Langroid:


```bash
python3 -m venv .venv
. ./.venv/bin/activate
pip install --upgrade langroid
````

Place your `GROQ_API_KEY` in a `.env` file in the root directory of this project.
If you don't have one, you can create an account on GroqCloud and 
generate one for free at https://console.groq.com. 
Your `.env` file should have a line that looks like the following:

```
GROQ_API_KEY=gsk_...
```
Or you can set explicitly set this key in your environment before 
running the scripts.

### Simple code examples using Langroid with a Groq-hosted LLM

Here is how you can specify a Groq-hosted LLM with Langroid, and directly 
"chat" with the LLM


```python
import langroid as lr
import langroid.language_models as lm

llm_config = lm.OpenAIGPTConfig(
    chat_model="groq/llama3-70b-8192",
    chat_context_length=8192,
)

llm = lm.OpenAIGPT(llm_config)

llm.chat("3+4=?").message
```

The `llm` does _not_ maintain conversation state, so you must invoke `chat()` with 
a sequence of user-assistant messages. Langroid has a convenient `ChatAgent` abstraction
that maintains this state for you:
```python
agent_config = lr.ChatAgentConfig(
    llm=llm_config,
    system_message="""Be nice but concise""",
)

agent = lr.ChatAgent(agent_config)
response = agent.llm_response("Capital of France?")
# follow-up question works since agent maintains conversation history
response = agent.llm_response("What about Congo?")
```

Finally, you can wrap an agent in a `Task` to run it in an interactive chat loop.
Here's all you need to make a basic chat-bot using Langroid:
```python
task = lr.Task(agent, interactive=True)
task.run()
```

An example script showing a 2-agent assistant is included in this folder.
The Langroid repo has numerous example scripts as well, and you can run them 
against a Groq-hosted LLM by changing `chat_model` to `groq/llama3-70b-8192` (as an 
example). Many of the scripts also take a command-line argument `-m` to specify the 
model, e.g. `-m groq/llama3-70b-8192`.
