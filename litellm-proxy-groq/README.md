# Use LiteLLM Proxy to Call Groq AI API

Use [LiteLLM Proxy](https://docs.litellm.ai/docs/simple_proxy) for:
- Calling 100+ LLMs Groq AI, OpenAI, Azure, Vertex, Bedrock/etc. in the OpenAI ChatCompletions & Completions format
- Track usage + set budgets with Virtual Keys

Using [Groq AI API with LiteLLM](https://docs.litellm.ai/docs/providers/groq)

## Sample Usage

### Step 1. Create a Config for LiteLLM proxy

LiteLLM Requires a config with all your models define - we can call this file `litellm_config.yaml`

[Detailed docs on how to setup litellm config - here](https://docs.litellm.ai/docs/proxy/configs)

```yaml
model_list:
  - model_name: groq-llama3 ### MODEL Alias ###
    litellm_params: # all params accepted by litellm.completion() - https://docs.litellm.ai/docs/completion/input
      model: groq/llama3-8b-8192 ### MODEL NAME sent to `litellm.completion()` ###
      api_key: "os.environ/GROQ_API_KEY" # does os.getenv("GROQ_API_KEY")

```

### Step 2. Start litellm proxy

```shell
docker run \
    -v $(pwd)/litellm_config.yaml:/app/config.yaml \
    -e GROQ_API_KEY=<your-groq-api-key>
    -p 4000:4000 \
    ghcr.io/berriai/litellm:main-latest \
    --config /app/config.yaml --detailed_debug
```

### Step 3. Test it! 

[Use with Langchain, LlamaIndex, Instructor, etc.](https://docs.litellm.ai/docs/proxy/user_keys)

```bash
import openai
client = openai.OpenAI(
    api_key="anything",
    base_url="http://0.0.0.0:4000"
)

response = client.chat.completions.create(
    model="groq-llama3",
    messages = [
        {
            "role": "user",
            "content": "this is a test request, write a short poem"
        }
    ]
)

print(response)
```

## Tool Calling 

```python
from openai import OpenAI
client = OpenAI(api_key="anything", base_url="http://0.0.0.0:4000") # set base_url to litellm proxy endpoint

tools = [
  {
    "type": "function",
    "function": {
      "name": "get_current_weather",
      "description": "Get the current weather in a given location",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "The city and state, e.g. San Francisco, CA",
          },
          "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
        },
        "required": ["location"],
      },
    }
  }
]
messages = [{"role": "user", "content": "What's the weather like in Boston today?"}]
completion = client.chat.completions.create(
  model="groq-llama3",
  messages=messages,
  tools=tools,
  tool_choice="auto"
)

print(completion)

```


## Supported Groq AI API Models

**ALL MODELS SUPPORTED**. 

Just add `groq/` to the beginning of the model name.

Example models: 
LiteLLM Supports 💥 ALL groq models
| Model Name         | Usge                                        |
|--------------------|---------------------------------------------------------|
| llama3-8b-8192     | `completion(model="groq/llama3-8b-8192", messages)`     | 
| llama3-70b-8192    | `completion(model="groq/llama3-70b-8192", messages)`    | 
| mixtral-8x7b-32768 | `completion(model="groq/mixtral-8x7b-32768", messages)` |
| gemma-7b-it        | `completion(model="groq/gemma-7b-it", messages)`        |  
| gemma-9b-it        | `completion(model="groq/gemma-9b-it", messages)`        |  
