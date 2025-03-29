# @ Author: Bertan Berker
# @ Language: Python 3.11.9
# This script is an example of a tree of thought implementation for solving a reasoning task
# Given the prompt of a reasoning task, the script will generate a tree of thought and then
# solve the task by traversing the tree.

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


def call_llm(prompt):
        
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Explain the importance of fast language models",
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    return chat_completion.choices[0].message.content


def generate_thought(prompt, step_number=5):

    thought_prompt = f"""
        Given the reasoning problem: "{prompt}", generate {step_number} different 'Thought' options to proceed with the solution step by step.
        Each thought should be short, logical, and explore a different path.

        Format:
        Thought {step_number}.1: ...
        Thought {step_number}.2: ...
        Thought {step_number}.3: ...
    """
    
    thoughts_text = call_llm(thought_prompt)
    return thoughts_text


def evaluate_thought(prompt, thoughts, step_number=5):
    
    eval_prompt = f"""
        You're solving: "{prompt}"

    These are the options for Thought {step_number}:
    {thoughts}

    Evaluate each one briefly and select the most promising one for solving the problem.

    Format:
    - Evaluation: ...
    - Best Thought: Thought {step_number}.X
    """
    
    return call_llm(eval_prompt)

