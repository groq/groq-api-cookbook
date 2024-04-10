import os
import re
import logging
import sys
import pickle
import traceback
from time import sleep
from dotenv import load_dotenv
from openai import OpenAI
from agent_functions import agent_chat, extract_code, extract_research_topic, extract_task, generate_file_name, generate_summary, get_current_date_and_time, load_checkpoint, print_block, save_checkpoint
from code_execution_manager import CodeExecutionManager, format_error_message, run_tests, monitor_performance, optimize_code, format_code, pass_code_to_alex, send_status_update, generate_documentation
import datetime
import zlib
from voice_tools import VoiceTools
from crypto_wallet import CryptoWallet
from browser_tools import BrowserTools
from ollamarag import LlamaRAG


def main():
    max_iterations = 500
    checkpoint_file = "agentic_workflow_checkpoint.pkl"
    code_execution_manager = CodeExecutionManager()
    date_time = get_current_date_and_time()
    voice_tools = VoiceTools()
    browser_tools = BrowserTools()

    system_messages = {
        "mike": code_execution_manager.read_file("mike.txt"),
        "annie": code_execution_manager.read_file("annie.txt"),
        "bob": code_execution_manager.read_file("bob.txt"),
        "alex": code_execution_manager.read_file("alex.txt")
    }

    checkpoint_data, code = load_checkpoint(checkpoint_file)
    if checkpoint_data:
        memory = {key: value for key, value in zip(["mike", "annie", "bob", "alex"], checkpoint_data)}
    else:
        memory = {key: [] for key in ["mike", "annie", "bob", "alex"]}

    print_block("Agentic Workflow", character='*')
    print_block(f"Start Time: {date_time}")

    for i in range(1, max_iterations + 1):
        print_block(f"Iteration {i}")
        files = code_execution_manager.list_files_in_workspace()
        project_output_goal = f"Brainstorm profitable scripts and run them in the workspace. Make sure to remove all placeholders and add real-world logic. Say Research Topic: <topic> to get info from online about <topic>. Current time: {date_time}"

        for agent in ["mike", "annie", "bob", "alex"]:
            memory[agent].append({"role": "system", "content": f"Files in workspace: {files}"})
            memory[agent].append({"role": "system", "content": f"Iteration {i} started. Current time: {date_time}"})

        bob_input = f"[Python experts only, don't let them write subpar files.] Current time: {date_time}. You are Bob (money-minded micromanager), the boss of Mike, Annie, and Alex. Make sure no one sends code that reverts your progress, as code is directly extracted from all responses.\nHere is the current state of the project:\n\nProject Goal: {project_output_goal}\nCurrent code: {code}\nCurrent error: {current_error if 'current_error' in locals() else 'None'}\n\nPlease provide your input as Bob, including delegating tasks to Mike, Annie, and Alex based on their expertise and the project requirements. Provide context and examples to guide them in providing high-quality responses and code snippets that align with the project's goals and best practices. Encourage them to provide detailed explanations and rationale behind their code modifications and suggestions to facilitate better collaboration and knowledge sharing. If you require additional information or resources, you can use the BrowserTools class to research relevant topics and libraries. Current files in the workspace: {files}."

        bob_response = agent_chat(bob_input, system_messages["bob"], memory["bob"], "mixtral-8x7b-32768", 0.5)
        print(f"Bob's Response:\n{bob_response}")

        for agent in ["mike", "annie", "alex"]:
            agent_input = f"Current time: {date_time}. You are {agent.capitalize()}, an AI {'software architect and engineer' if agent == 'mike' else 'senior agentic workflow developer' if agent == 'annie' else 'DevOps Engineer'}. Here is your task from Bob:\n\nTask: {extract_task(bob_response, agent.capitalize())}\n\nCurrent code: {code}\nCurrent error: {current_error if 'current_error' in locals() else 'None'}\n\nPlease provide your response, including any necessary code modifications, suggestions, or additional information you may need to complete the task effectively."

            agent_response = agent_chat(agent_input, system_messages[agent], memory[agent], "mixtral-8x7b-32768", 0.7)
            print(f"{agent.capitalize()}'s Response:\n{agent_response}")

            # Perform research using BrowserTools if requested by the agent
            research_topic = extract_research_topic(agent_response)
            if research_topic:
                research_results = browser_tools.research_topic(research_topic)
                research_summary = "\n".join([f"Title: {result['title']}\nURL: {result['url']}\nContent: {result['content'][:1000]}..." for result in research_results])
                memory[agent].append({"role": "user", "content": f"Research results for topic '{research_topic}':\n{research_summary}"})

        # Check if Alex provided any code updates
        alex_code = extract_code(agent_response)
        if alex_code:
            code = alex_code
            current_error = code_execution_manager.test_code(code)[1]
            if current_error:
                memory["alex"].append({"role": "system", "content": f"Error in code: {current_error}. Code not saved."})
            else:
                file_name = generate_file_name(code)
                code_execution_manager.save_file(file_name, code)
                memory["alex"].append({"role": "system", "content": f"Code execution successful and error-free. Code saved in workspace as {file_name}."})

                print_block("Running Tests")
                test_results = run_tests(code)
                print_block(f"Test Results:\n{test_results}")

                print_block("Monitoring Performance")
                performance_data = monitor_performance(code)
                print_block(f"Performance Data:\n{performance_data}")

                print_block("Optimization Suggestions")
                optimization_suggestions = optimize_code(code)
                print_block(f"Optimization Suggestions:\n{optimization_suggestions}")

                print_block("Formatting Code")
                formatted_code = format_code(code)
                print_block(f"Formatted Code:\n{formatted_code}")

                print_block("Generating Documentation")
                documentation = generate_documentation(code)
                print_block(f"Generated Documentation:\n{documentation}")

                send_status_update(memory["mike"], memory["annie"], memory["alex"], f"Iteration {i} completed. Code updated and tested. Add more logic, remove all placeholders. Test results: {test_results}. Performance data: {performance_data}. Optimization suggestions: {optimization_suggestions}. Documentation: {documentation}. Code saved under file name: {file_name} in workspace. Code for {file_name} is:\n\n{code}")

        checkpoint_data = [memory[key] for key in ["mike", "annie", "bob", "alex"]] + [code]
        save_checkpoint(checkpoint_data, checkpoint_file, code)

    print_block("Agentic Workflow Completed", character='*')
    browser_tools.close()  # Close the browser


if __name__ == "__main__":
    main()
