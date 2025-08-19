"""
Step 1. Set up dependencies
"""

import os
from dotenv import load_dotenv
import requests  # pip install requests first!
import time

# Load environment variables from .env file
load_dotenv()

# Access environment variables
api_key = os.getenv("GROQ_API_KEY")


"""
Step 2. Upload the JSONL file to Groq
"""

def upload_file_to_groq(api_key, file_path):
    url = "https://api.groq.com/openai/v1/files"
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    # Prepare the file and form data
    files = {
        "file": ("batch_file.jsonl", open(file_path, "rb"))
    }
    
    data = {
        "purpose": "batch"
    }
    
    # Make the POST request
    response = requests.post(url, headers=headers, files=files, data=data)
    
    return response.json()

# Usage example
file_path = "batch_input.jsonl"  # Path to your JSONL file
file_id = ""  # will be used in the next step

try:
    result = upload_file_to_groq(api_key, file_path)
    file_id = result["id"]
    print("This is the file_id from Step 2: " + file_id)

except Exception as e:
    print(f"Error: {e}")



"""
Step 3. Make a batch object
"""

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

batch_id = ""  # will be used in the next step
try:
    result = create_batch(api_key, file_id)
    batch_id = result["id"]  # batch result id
    print("This is the Batch object id from Step 3: " + batch_id)

except Exception as e:
    print(f"Error: {e}")



"""
Step 4. Get the batch status
"""

def get_batch_status(api_key, batch_id):
    url = f"https://api.groq.com/openai/v1/batches/{batch_id}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    return response.json()

output_file_id = ""  # will be used in the next step
try:
    result = get_batch_status(api_key, batch_id)
    print("\nStep 4 results: ")
    
    count = 0

    # Corrected condition: use `result["status"]` instead of `result.status`
    while result["status"] != "completed" and count < 100:
        result = get_batch_status(api_key, batch_id)  # Update `result` inside the loop
        time.sleep(3)
        print("Your batch status is: " + result["status"])
        count += 1

    output_file_id = result.get("output_file_id")  # Use .get() to safely access keys
    print("This is your output_file_id from Step 4: " + output_file_id)
except Exception as e:
    print(f"Error: {e}")



"""
Step 5. Retrieve batch results
"""

def download_file_content(api_key, output_file_id, output_file):
    url = f"https://api.groq.com/openai/v1/files/{output_file_id}/content"
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    response = requests.get(url, headers=headers)
    
    # Write the content to a file
    with open(output_file, 'wb') as f:
        f.write(response.content)
    
    return f"\nFile downloaded successfully to {output_file}"

output_file = "batch_output.jsonl"  # replace with your own file of choice to download batch job contents to
try:
    result = download_file_content(api_key, output_file_id, output_file)
    print(result)
except Exception as e:
    print(f"Error: {e}")