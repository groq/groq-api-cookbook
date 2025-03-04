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