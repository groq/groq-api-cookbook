# @ Author: Bertan Berker
# @ Language: Python 3.11.9
# This script is an example of a tree of thought implementation for solving a reasoning task
# using Depth-First Search (DFS) instead of Breadth-First Search (BFS).

import os
from dotenv import load_dotenv
from groq import Groq
load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# ThoughtNode class is used to represent a node in the tree of thought
# It contains the thought, the parent node, and the children nodes
# The thought is the content of the node
# The parent node is the node that comes before this node
# The children nodes are the nodes that come after this node
class ThoughtNode:
    def __init__(self, thought, parent=None):
        self.thought = thought              
        self.parent = parent                
        self.children = []                  
    
    def add_child(self, child_node):
        self.children.append(child_node)


# call_llm function is used to call the LLM
# :param prompt: The prompt to send to the LLM
# :return: The response from the LLM
def call_llm(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "You are a world class reasoning expert. You are given a reasoning problem to solve. This is your problem:" + prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content


# generate_thought function is used to generate thoughts for the next step
# :param prompt: The prompt to send to the LLM
# :param step_number: The number of thoughts to generate
# :return: The thoughts from the LLM
def generate_thought(prompt, step_number):
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


# dfs_expand function is used to expand the tree of thought
# :param node: The current node
# :param current_depth: The current depth of the tree
# :param max_depth: The maximum depth of the tree
# :param thoughts_per_step: The number of thoughts to generate for each step
# :return: None
def dfs_expand(node, current_depth, max_depth, thoughts_per_step):
    if current_depth >= max_depth:
        return

    print(f"\nExpanding (depth {current_depth}):\n→ {node.thought}")
    thoughts_text = generate_thought(node.thought, step_number=thoughts_per_step)
    print(f"\nGenerated Thoughts:\n{thoughts_text}")

    for line in thoughts_text.splitlines():
        if line.strip().startswith(f"Thought {thoughts_per_step}."):
            thought_content = line.split(":", 1)[-1].strip()
            child_node = ThoughtNode(thought=thought_content, parent=node)
            node.add_child(child_node)
            # DFS: go deep immediately
            dfs_expand(child_node, current_depth + 1, max_depth, thoughts_per_step)


# dfs_reasoning_solver_full_tree function is used to solve the reasoning problem
# :param user_prompt: The prompt to send to the LLM
# :param max_depth: The maximum depth of the tree
# :param thoughts_per_step: The number of thoughts to generate for each step
# :return: The root node of the tree
def dfs_reasoning_solver_full_tree(user_prompt, max_depth=5, thoughts_per_step=3):
    root = ThoughtNode(thought=user_prompt)
    dfs_expand(root, current_depth=0, max_depth=max_depth, thoughts_per_step=thoughts_per_step)
    return root


# get_all_paths_from_root function is used to get all paths from the root to the leaves
# :param node: The root node of the tree
# :return: All paths from the root to the leaves
def get_all_paths_from_root(node):
    if not node.children:
        return [[node.thought]]
    paths = []
    for child in node.children:
        for subpath in get_all_paths_from_root(child):
            paths.append([node.thought] + subpath)
    return paths


# score_reasoning_path function is used to score a reasoning path
# :param path: The path to score
# :param original_prompt: The original prompt to send to the LLM
# :return: The score of the path
def score_reasoning_path(path, original_prompt):
    joined_reasoning = "\n".join([f"Step {i+1}: {step}" for i, step in enumerate(path)])
    prompt = f"""
        You're evaluating a reasoning path for the problem: "{original_prompt}"

        Here is one possible reasoning path:
        {joined_reasoning}

        Please rate the overall quality and effectiveness of this reasoning path on a scale from 1 to 100.
        Just respond with a number between 1 and 100.
    """
    score_str = call_llm(prompt).strip()
    try:
        return int(score_str)
    except ValueError:
        return 0


# summarize_best_path function is used to summarize the best path
# :param prompt: The original prompt to send to the LLM
# :param path: The best path to summarize
# :return: The summarized path
def summarize_best_path(prompt, path):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Given the prompt: {prompt}, summarize the best reasoning path as precisely and simply as possible \
                    and give the final answer. The reasoning path is: {path}.",
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    reasoning_prompt = input("Enter a reasoning problem: ")
    root = dfs_reasoning_solver_full_tree(reasoning_prompt, max_depth=3, thoughts_per_step=3)

    all_paths = get_all_paths_from_root(root)
    print(f"\nFound {len(all_paths)} reasoning paths.\n")

    for i, path in enumerate(all_paths, start=1):
        print(f"Path {i}:")
        for j, step in enumerate(path, start=1):
            print(f"  Step {j}: {step}")
        print("---------------")

    best_score = -1
    best_path = None

    print("\nScoring all reasoning paths...\n")

    for i, path in enumerate(all_paths, start=1):
        score = score_reasoning_path(path, reasoning_prompt)
        print(f"Path {i}: Scored {score}/100")
        if score > best_score:
            best_score = score
            best_path = path

    print("\nBest Reasoning Path:")
    for i, step in enumerate(best_path, 1):
        print(f"Step {i}: {step}")
    print(f"\nFinal Score: {best_score}/100")

    print("\nThe solution is...")
    print(summarize_best_path(reasoning_prompt, best_path))