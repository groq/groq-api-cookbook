import json
from dotenv import load_dotenv
from openai import OpenAI
import datetime
import os
import logging
import re
import pickle
import zlib
from time import sleep
from browser_tools import BrowserTools
from code_execution_manager import CodeExecutionManager
from crypto_wallet import CryptoWallet
from task_manager import TaskManager
import spacy
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage, AIMessage
load_dotenv()

api_keys = {
    "groq": os.getenv("GROQ_API_KEY"),
    "openai": os.getenv("OPENAI_API_KEY"),
}
client = {
    "groq_client": OpenAI(base_url="https://api.groq.com/openai/v1", api_key=api_keys["groq"]),
    "openai_client": OpenAI(base_url="https://api.openai.com/v1", api_key=api_keys["openai"]),
}

logging.basicConfig(filename='agentic_workflow.log', level=logging.INFO)

def get_current_date_and_time():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S.%f')




def agent_chat(user_input, system_message, memory, model, temperature, max_retries=5, retry_delay=10, agent_name=None):
    browser_tools = BrowserTools()
    code_execution_manager = CodeExecutionManager()
    
    nlp = spacy.load("en_core_web_sm")
    task_manager = TaskManager(nlp)

    messages = [
        SystemMessage(content=system_message),
        *[AIMessage(content=msg["content"]) if msg["role"] == "assistant" else HumanMessage(content=msg["content"]) for msg in memory[-5:]],
        HumanMessage(content=user_input)
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "search_google",
                "description": "Search Google for relevant information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query",
                        }
                    },
                    "required": ["query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "scrape_page",
                "description": "Scrape a web page for relevant information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "The URL of the web page to scrape",
                        }
                    },
                    "required": ["url"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "test_code",
                "description": "Test the provided code",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "The code to test",
                        }
                    },
                    "required": ["code"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "optimize_code",
                "description": "Optimize the provided code",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "The code to optimize",
                        }
                    },
                    "required": ["code"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "extract_tasks",
                "description": "Extract tasks from the provided text",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The text to extract tasks from",
                        }
                    },
                    "required": ["text"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "update_task_status",
                "description": "Update the status of a task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task": {
                            "type": "object",
                            "description": "The task to update",
                        },
                        "status": {
                            "type": "string",
                            "description": "The new status of the task",
                        }
                    },
                    "required": ["task", "status"],
                },
            },
        },
    ]

    chat = ChatGroq(temperature=temperature, model_name=model)
    prompt = ChatPromptTemplate.from_messages(messages)

    chain = prompt | chat

    retry_count = 0
    while retry_count < max_retries:
        try:
            print(f"\n🚀 Iteration {retry_count + 1} - Engaging {agent_name if agent_name else 'AI Agent'} 🚀")
            print(f"🧠 System Message: {system_message}")
            print(f"👤 User Input: {user_input}")

            chat_completion = chain.invoke({"text": user_input})
            response_message = chat_completion.content

            print(f"\n🤖 {agent_name if agent_name else 'AI Agent'}'s Response:")
            print(f"{response_message}\n")

            tool_calls = []
            try:
                tool_calls = json.loads(response_message).get("tool_calls", [])
            except json.JSONDecodeError:
                pass

            if tool_calls:
                available_functions = {
                    "search_google": browser_tools.search_google,
                    "scrape_page": browser_tools.scrape_page,
                    "test_code": code_execution_manager.test_code,
                    "optimize_code": code_execution_manager.optimize_code,
                    "extract_tasks": task_manager.extract_tasks,
                    "update_task_status": task_manager.update_task_status,
                }
                messages.append(AIMessage(content=response_message))
                
                for tool_call in tool_calls:
                    function_name = tool_call["function"]["name"]
                    function_to_call = available_functions[function_name]
                    function_args = tool_call["function"]["arguments"]
                    
                    print(f"🛠️ Executing tool: {function_name}")
                    print(f"📥 Tool arguments: {function_args}")

                    function_response = function_to_call(**function_args)

                    print(f"📤 Tool response: {function_response}")

                    messages.append(
                        {
                            "tool_call_id": tool_call["id"],
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                        }
                    )
                
                second_response = chain.invoke({"text": user_input})
                response_content = second_response.content

                print(f"\n🤖 {agent_name if agent_name else 'AI Agent'}'s Updated Response:")
                print(f"{response_content}\n")

            else:
                response_content = response_message
            
            truncated_response = response_content[:1000]
            memory.append({"role": "assistant", "content": truncated_response})
            memory.append({"role": "user", "content": user_input})

            sleep(10)
            return response_content

        except Exception as e:
            retry_count += 1
            if retry_count < max_retries:
                print(f"❌ Error encountered: {str(e)}")
                print(f"🔄 Retrying in {retry_delay} seconds... (Attempt {retry_count}/{max_retries})")
                sleep(retry_delay)
            else:
                print(f"❌ Max retries exceeded. Raising the exception.")
                raise e
def extract_code(text):
    try:
        code_block_pattern = re.compile(r'```python(.*?)```', re.DOTALL)
        code_blocks = code_block_pattern.findall(text)
        return code_blocks[0].strip() if code_blocks else None
    except Exception as e:
        #logging.error(f"Error extracting code: {format_error_message(e)}")
        return None
def generate_file_name(code):
    try:

        messages = [
            {"role": "system", "content": f" you only respond with an appropriate file name for the code you are given. Dont provide any other information."},
            
            {"role": "user", "content": f" Please provide a suitable file name for the following code:\n\n{code} \n\nFile Name:"}
        ]        
        
        file_name = client["groq_client"].chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=messages,
                max_tokens=20,
                temperature=0,
            )

        
        file_name = file_name.choices[0].message.content
        sleep(10)
        return file_name
    except Exception as e:
        #logging.error(f" {format_error_message(e)}")
        return None
def save_checkpoint(checkpoint_data, checkpoint_file, code):
    try:
        compressed_data = compress_data(checkpoint_data)
        with open(checkpoint_file, 'wb') as f:
            pickle.dump(compressed_data, f)

        if code:
            file_name = generate_file_name(code)
            code_file_path = os.path.join("workspace", f"{file_name}.py")
            with open(code_file_path, 'w') as code_file:
                code_file.write(code)
    except Exception as e:
        #logging.error(f"Error saving checkpoint: {format_error_message(e)}")
        pass

def load_checkpoint(checkpoint_file):
    try:
        with open(checkpoint_file, 'rb') as f:
            compressed_data = pickle.load(f)
            checkpoint_data = decompress_data(compressed_data)
            code = checkpoint_data[-1] if checkpoint_data else ""
            return checkpoint_data, code
    except FileNotFoundError:
        return None, ""
    except Exception as e:
        #logging.error(f"Error loading checkpoint: {format_error_message(e)}")
        return None, ""

def compress_data(data):
    compressed_data = zlib.compress(pickle.dumps(data))
    return compressed_data

def decompress_data(compressed_data):
    decompressed_data = pickle.loads(zlib.decompress(compressed_data))
    return decompressed_data

def print_block(text, width=80, character='='):
    lines = text.split('\n')
    max_line_length = max(len(line) for line in lines)
    padding = (width - max_line_length) // 2

    print(character * width)
    for line in lines:
        print(character + ' ' * padding + line.center(max_line_length) + ' ' * padding + character)
    print(character * width)




def generate_summary(response, agent_name):
    try:
        summary_prompt = f"Please provide a concise summary of {agent_name}'s response in 100 words or less:\n\n{response}"
        messages = [
            {"role": "system", "content": "you make summaries of the responses of the agents in 100 words or less. You will embody them as you are them when talking, when summarizing use first person."},
            
            {"role": "user", "content": summary_prompt}
        ]        
        
        summary_completion = client["groq_client"].chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=messages,
                max_tokens=32768,
                temperature=0,
            )

        
        summary = summary_completion.choices[0].message.content
        sleep(10)
        return summary
    except Exception as e:
        #logging.error(f"Error generating summary for {agent_name}: {format_error_message(e)}")
        return None
def extract_task(response, agent_name):
    task_pattern = re.compile(fr'Tasks for {agent_name}:\n1\. (.*?)\n2\.')
    match = task_pattern.search(response)
    return match.group(1) if match else ""

def extract_research_topic(response):
    research_pattern = re.compile(r'Research topic: (.*)')
    match = research_pattern.search(response)
    return match.group(1) if match else ""