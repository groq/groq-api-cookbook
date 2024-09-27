# set JIGSAWSTACK_API_KEY in the secrets
import os
from jigsawstack import JigsawStack

jigsaw = JigsawStack(api_key=os.environ.get("JIGSAWSTACK_API_KEY"))

#  Run a prompt
params = {
    "prompt": "How to cook {dish}",  # The prompt for your use case
    "inputs": [{"key": "dish"}],  # dynamic vars that are in the brackets {}
    "return_prompt": [
        {"step": "name of the step", "details": "details of this step"}
    ],  # The structure of the JSON, in this case, an array of objects
    "input_values": {"dish": "pizza"},
    "prompt_guard": [
        "sexual_content",
        "defamation",
    ],  # Add this to include prompt guards against prompt injection from user inputs and a wide range of unsafe use cases.
}

result = jigsaw.prompt_engine.run_prompt_direct(params)

# Print the result
print(result)
