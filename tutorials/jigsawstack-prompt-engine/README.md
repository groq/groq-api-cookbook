## How to JigsawStack Prompt Engine Powered by Groq

## Overview

[JigsawStack](https://jigsawstack.com) is a powerful AI SDK designed to integrate into any backend, automating tasks such as web scraping, Optical Character Recognition (OCR), translation, and more, using custom fine-tuned models. By plugging JigsawStack into your existing application infrastructure, you can offload the heavy lifting and focus on building.

The JigsawStack Prompt Engine is a feature that allows you to not only leverage Large Language Models (LLMs) but automatically choose the best LLM for every one of your prompts, delivering lightning-fast results powered by [Groq](https://groq.com/).


## Features

The JigsawStack Prompt Engine comes with a range of features out-of-the-box that make it easy to work with LLMS:

🌐 Prompt caching for repeated prompt runs

💬 Automatic prompt optimization for improved performance

📄 Response schema validation for accuracy and consistency

🔁 Reusable prompts to streamline your workflow

🧠 Multi-agent LLM from 50+ models for flexibility depending on your apps

🚫 No virtual rate limits, tokens, and GPU management


## Prerequisite 
- Create a JigsawStack [account](https://jigsawstack.com) (Get started for free)
- Retrieve your api [key](https://jigsawstack.com/dashboard)


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



## Recommendation

- For prompts that are used repeatedly, it is recommended to first create the prompt, then run it using its prompt ID to enable optimization.

- Run Prompt Direct is ideal for one-time use.

For more information on the Prompt Engine engine see [documentation](https://docs.jigsawstack.com/examples/ai/prompt-engine)