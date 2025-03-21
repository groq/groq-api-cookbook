# Groq Batch Processing

This tutorial will guide you through the process of uploading and processing batch jobs using the Groq API. Follow these five steps to successfully handle batch requests.

## Step 1: Set Up Dependencies:
```
Before interacting with the Groq API, you need to install and import the required dependencies.

import os
from dotenv import load_dotenv
import requests # Install with: pip install requests
import time

# Load environment variables from .env file
load_dotenv()

# Access environment variables
api_key = os.getenv("GROQ_API_KEY")
```
Make sure you have a `.env` file containing your `GROQ_API_KEY`.

### Create a virtual environment
`python3 -m venv venv`

### Activate it
`source venv/bin/activate`

### Install the packages
`pip3 install groq requests python-dotenv`

# Step 2: Upload the JSONL File to Groq
```
def upload_file_to_groq(api_key, file_path):
    url = "https://api.groq.com/openai/v1/files"
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    files = {
        "file": ("batch_file.jsonl", open(file_path, "rb"))
    }
    
    data = {"purpose": "batch"}
    
    response = requests.post(url, headers=headers, files=files, data=data)
    return response.json()

file_path = "batch_input.jsonl"  # Path to your JSONL file
file_id = ""

try:
    result = upload_file_to_groq(api_key, file_path)
    file_id = result["id"]
    print("This is the file_id from Step 2: " + file_id)
except Exception as e:
    print(f"Error: {e}")
```

# Step 3: Create a Batch Object

Create a batch object using the uploaded file ID.

```
def create_batch(api_key, input_file_id):
    url = "https://api.groq.com/openai/v1/batches"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "input_file_id": input_file_id,
        "endpoint": "/v1/chat/completions",
        "completion_window": "24h"
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

batch_id = ""
try:
    result = create_batch(api_key, file_id)
    batch_id = result["id"]
    print("This is the Batch object id from Step 3: " + batch_id)
except Exception as e:
    print(f"Error: {e}")
```



# Step 4: Get the Batch Status

Monitor the batch job's status until it completes.

```
def get_batch_status(api_key, batch_id):
    url = f"https://api.groq.com/openai/v1/batches/{batch_id}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    return response.json()

output_file_id = ""
try:
    result = get_batch_status(api_key, batch_id)
    print("\nStep 4 results: ")
    
    count = 0
    while result["status"] != "completed" and count < 100:
        result = get_batch_status(api_key, batch_id)
        time.sleep(3)
        print("Your batch status is: " + result["status"])
        count += 1

    output_file_id = result.get("output_file_id")
    print("This is your output_file_id from Step 4: " + output_file_id)
except Exception as e:
    print(f"Error: {e}")
```


# Step 5: Retrieve Batch Results

Download and save the batch job results.

```
def download_file_content(api_key, output_file_id, output_file):
    url = f"https://api.groq.com/openai/v1/files/{output_file_id}/content"
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    response = requests.get(url, headers=headers)
    
    with open(output_file, 'wb') as f:
        f.write(response.content)
    
    return f"\nFile downloaded successfully to {output_file}"

output_file = "batch_output.jsonl"
try:
    result = download_file_content(api_key, output_file_id, output_file)
    print(result)
except Exception as e:
    print(f"Error: {e}")
```

Now you have successfully uploaded, processed, and retrieved batch job results using the Groq API!


## How to run it in your terminal:
`python3 main.py`


### Example output in terminal:
```
This is the file_id from Step 2: file_01jpthgx92e3ts09bma0bfchmt
This is the Batch object id from Step 3: batch_01jpthgxffe8ms4zqdkf1aejjp

Step 4 results: 
Your batch status is: validating
Your batch status is: in_progress
Your batch status is: completed
This is your output_file_id from Step 4: file_01jpthh1e3e739wba761nfgvj2

File downloaded successfully to batch_output.jsonl
```

Example input .jsonl file
```
{"custom_id": "request-2", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "llama-3.1-8b-instant", "messages": [{"role": "system", "content": "You are a helpful translation assistant. Translate the following into spanish."}, {"role": "user", "content": "Hello, how are you today?"}]}}
```

Example output .jsonl file
```
{"id":"batch_req_out_01jpra5p4ve4v8k14zkqn6agjm","custom_id":"request-2","response":{"status_code":200,"request_id":"req_01jpra5n2qef6s66k65v8sy51h","body":{"id":"chatcmpl-f822c700-75aa-4fa3-8f2c-3f65cca8a1d3","object":"chat.completion","created":1742425217,"model":"llama-3.1-8b-instant","choices":[{"index":0,"message":{"role":"assistant","content":"\"Hola, ¿cómo estás hoy\" or more commonly in informal settings: \"Hola, ¿qué onda hoy\". \n\nIf you want it to be a more formal conversation, you could use: \"Buenos días, ¿cómo está hoy?\""},"logprobs":null,"finish_reason":"stop"}],"usage":{"queue_time":1.0087154420000002,"prompt_tokens":55,"prompt_time":0.009901563,"completion_tokens":55,"completion_time":0.073333333,"total_tokens":110,"total_time":0.083234896},"system_fingerprint":"fp_076aab041c","x_groq":{"id":"req_01jpra5n2qef6s66k65v8sy51h"}}},"error":null}
```

View more detailed documentation on batch processing [here.](https://console.groq.com/docs/batch)