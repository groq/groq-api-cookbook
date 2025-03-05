# Minions with Groq API Cookbook

This cookbook demonstrates how to use the [Minions framework](https://github.com/HazyResearch/minions) with Groq's powerful LLM APIs. Minions is an innovative approach that combines local and cloud LLMs to reduce costs while maintaining high performance.

## What is Minions?

Minions is a framework developed by Stanford's Hazy Research lab that enables efficient collaboration between:
- Small, local models (running on your device)
- Large, powerful models (running in the cloud)
git 
By combining Minions with Groq's fast inference, you get the best of both worlds: reduced costs, minimal latency, and high-quality results similar to large models.

The framework offers two main protocols:

1. **Minion**: A single local model chats with a cloud model to reach a solution
   - 30.4x reduction in remote costs
   - Maintains 87% of cloud model performance
   - Significantly reduces end-to-end latency when using Groq's fast inference

2. **MinionS**: Cloud model decomposes the task into subtasks for parallel processing
   - 5.7x reduction in remote costs
   - Maintains 97.9% of cloud model performance
   - Parallel processing further accelerates complex tasks on consumer hardware

Essentially, Minion is significantly more cost-effective than MinionS, but also has lower performance. One should think about the complexity of the task and decide between Minion and MinionS based on the trade-off between cost and performance.

## Why Groq with Minions?

Groq's LPU (Language Processing Unit) technology delivers exceptionally fast inference times, making it an ideal choice for the Minions framework. When combined:

- **Blazing Speed**: Groq's sub-second response times minimize the latency impact of cloud calls
- **Consumer-Friendly**: Even modest consumer devices can run sophisticated AI workflows with the quality of large models.

## Prerequisites

1. Clone the repository:
```bash
git clone https://github.com/HazyResearch/minions.git 
cd minions
```

2. Create a virtual environment (optional):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the package and dependencies:
```bash
pip install -e .
```

4. Install Ollama and pull the Llama 3.2 model:
```bash
# Install Ollama from https://ollama.ai
ollama pull llama3.2
```

5. Get your Groq API key from [Groq Cloud](https://console.groq.com)

## Examples

This cookbook includes two examples:
1. Using the Minion protocol (`minion_example.py`)
2. Using the MinionS protocol (`minions_example.py`)

### Running the Examples

1. Set your Groq API key:
```bash
export GROQ_API_KEY='your-api-key-here'
```

2. Run either example:
```bash
python minion_example.py
# or
python minions_example.py
```

## Example Code

### Minion Example

```python
from minions.clients.ollama import OllamaClient
from minions.clients.groq import GroqClient
from minions.minion import Minion

local_client = OllamaClient(
    model_name="llama3.2",
)
    
remote_client = GroqClient(
    model_name="llama-3.3-70b-versatile",
)

# Instantiate the Minion object with both clients
minion = Minion(local_client, remote_client)

context = """
Patient John Doe is a 60-year-old male with a history of hypertension. In his latest checkup, his blood pressure was recorded at 160/100 mmHg, and he reported occasional chest discomfort during physical activity.
Recent laboratory results show that his LDL cholesterol level is elevated at 170 mg/dL, while his HDL remains within the normal range at 45 mg/dL. Other metabolic indicators, including fasting glucose and renal function, are unremarkable.
"""

task = "Based on the patient's blood pressure and LDL cholesterol readings in the context, evaluate whether these factors together suggest an increased risk for cardiovascular complications."

# Execute the minion protocol for up to two communication rounds
output = minion(
    task=task,
    context=[context],
    max_rounds=2
)

print(output["final_answer"])
```

### MinionS Example

```python
from minions.clients.ollama import OllamaClient
from minions.clients.groq import GroqClient
from minions.minions import Minions
from pydantic import BaseModel

class StructuredLocalOutput(BaseModel):
    explanation: str
    citation: str | None
    answer: str | None

local_client = OllamaClient(
    model_name="llama3.2",
    temperature=0.0,
    structured_output_schema=StructuredLocalOutput
)

remote_client = GroqClient(
    model_name="llama-3.3-70b-versatile",
)

# Instantiate the Minion object with both clients
minions = Minions(local_client, remote_client)

context = """
Patient John Doe is a 60-year-old male with a history of hypertension. In his latest checkup, his blood pressure was recorded at 160/100 mmHg, and he reported occasional chest discomfort during physical activity.
Recent laboratory results show that his LDL cholesterol level is elevated at 170 mg/dL, while his HDL remains within the normal range at 45 mg/dL. Other metabolic indicators, including fasting glucose and renal function, are unremarkable.
"""

task = "Based on the patient's blood pressure and LDL cholesterol readings in the context, evaluate whether these factors together suggest an increased risk for cardiovascular complications."

# Execute the minion protocol for up to two communication rounds
output = minions(
    task=task,
    doc_metadata="Medical Report",
    context=[context],
    max_rounds=2
)

print(output["final_answer"])
```

## Additional Resources
Check out these additional resources to learn more about Minions and the Groq API: 

- [Minions GitHub Repository](https://github.com/HazyResearch/minions)
- [Groq API Documentation](https://console.groq.com/docs)
- [Minions Research Paper](https://arxiv.org/abs/2402.15688)
