## How to JigsawStack Prompt Engine Powered by Groq

[JigsawStack](https://jigsawstack.com)  is an AI SDK that is easy to plug and play into any backend to automate a lot of the heavy lifting away for tasks like scraping, OCR, translation, and using LLMs.

The JigsawStack Prompt Engine allows you to run the best LLM on every prompt at the fastest speed powered by Groq!


## Prerequisite 
- Create a JigsawStack account (if you don't have any)
- Retrieve your api key 


### Installation

```bash
pip install jigsawstack
```


## Usage

### Example 1: Create and run a prompt

- #### Create prompt
```python
from jigsawstack import JigsawStack

jigsaw = JigsawStack(api_key="your-api-key")

params = {
    "prompt": "How to cook {dish}", #The prompt for your use case
    "inputs": [{ "key": "dish" }], #dynamic vars that are in the brackets {}
    "return_prompt": "Return the result in a markdown format", #The structure of the JSON, in this case, an array of objects
}
result = jigsaw.prompt_engine.create(params)

print(result.prompt_engine_id) # prompt engine ID
```

- #### Run the prompt
```python
from jigsawstack import JigsawStack
jigsaw = JigsawStack(api_key="your-api-key")
resp = jigsaw.prompt_engine.run(
    {
        "id": result.prompt_engine_id, #The ID you got after creating the engine
        "input_values": {
            "dish": "Singaporean chicken rice", #They value for your dynamic field
        },
    }
)
```

### Example 2: Execute the prompt directly

```python
from jigsawstack import JigsawStack

jigsaw = JigsawStack(api_key="your-api-key")

params = {
    "prompt":"How to cook {dish}",
    "inputs": [
        {
            "key": "dish"
        },
    ],
    "input_values": {
        "dish": "Nigerian Jollof Rice"
    },
    "return_prompt": [{
         "step": "Name of this step",
        "details": "Details of this step",
    }],
}

result = jigsaw.prompt_engine.run_prompt_direct(params)
```



## Prompt Guard - Llama Guard 3 by Groq

The prompt engine comes with prompt guards to prevent prompt injection from user inputs and a wide range of unsafe use cases. This can be turned on automatically using the `prompt_guard` field.

```python
params = {
    "prompt": "Tell me a story about {about}",
    "inputs": [
        {
            "key": "about",
        },
    ],
    "input_values": {
        "about": "The Leaning Tower of Pisa"
    },
    "return_prompt": "Return the result in a markdown format",
    "prompt_guard": ["sexual_content", "defamation"] #Add this to use llama-guard
}
result = jigsaw.prompt_engine.run_prompt_direct(params)

print(result)
```


For more information on the Prompt Engine 