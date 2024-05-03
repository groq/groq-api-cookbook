### Langroid + Groq
[Langroid](https://github.com/langroid/langroid) is an
open-source Python framework that simplifies building LLM applications, 
using a Multi-Agent paradigm.

You can now use Langroid with Groq, by setting the model name to 
`groq/<model>`, e.g., `groq/llama3-70b-8192`.

To get started, create a virtual environment using Python 3.11: 


```bash
python3 -m venv .venv
. ./.venv/bin/activate
pip install --upgrade langroid
````
Place your `GROQ_API_KEY` in a `.env` file in the root directory of this project,
it should have a line that looks like:
```
GROQ_API_KEY=gsk_...
```
Or you can set explicitly set this key in your environment before 
running the scripts.

Below is a bare-bones code example.

```python
import langroid as lr
import langroid.language_models as lm

llm_config = lm.OpenAIGPTConfig(
    chat_model="groq/llama3-70b-8192",
    chat_context_length=8192,
)

llm = lm.OpenAIGPT(llm_config)

llm.chat("3+4=?").message

agent_config = lr.ChatAgentConfig(
    llm=llm_config,
    system_message="""Be nice but concise""",
)

agent = lr.ChatAgent(agent_config)
task = lr.Task(agent, interactive=True)
```

An example script showing a 2-agent assistant is included in this folder.
The langroid repo has numerous example scripts as well, and you can run them 
against a groq-hosted LLM by changing `chat_model` to `groq/llama3-70b-8192` (as an 
example). Many of the scripts also take a command-line argument `-m` to specify the 
model, e.g. `-m groq/llama3-70b-8192`.
