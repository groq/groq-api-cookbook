# Tree of Thought Reasoning with Groq API

A dynamic Tree-of-Thought (ToT) implementation using the [Groq API](https://console.groq.com/docs). This project demonstrates how large language models like LLaMA 3 can reason more effectively by exploring multiple paths of thought, evaluating them, and selecting the best one.

> Built as an open-source contribution to the [Groq API Cookbook](https://github.com/groq/groq-api-cookbook)

---

## What It Does

- Accepts **any reasoning problem** from the user
- Builds a **Tree of Thought** using:
  - **Breadth-First Search (BFS)** or
  - **Depth-First Search (DFS)**
- Uses **Groq + LLaMA 3** to:
  - Generate multiple thoughts per step
  - Evaluate and score each reasoning path
- Picks the most effective solution path
- **Visualizes** the reasoning tree
  - Highlights the best path

---

## 🛠 How to Use

### Install Dependencies

```bash
pip install -r requirements.txt
```
### Set Up Your `.env` File

Create a `.env` file in the root directory with your Groq API key:

```env
GROQ_API_KEY=your-groq-api-key-here
```

### Run the Script

```bash
python BFS_tree_of_thought.py
python DFS_tree_of_thought.py
```

You'll be prompted to:
- Enter your reasoning problem
- Choose BFS or DFS
- View the best path and full tree visualization

---

## Jupyter Notebook Support & Possible API implementation

This project is also notebook-friendly! You can use the "Tree_of_Thought_Reasoning.ipynb" script for interactive experimentation.

Or you can build a frontend and connect it with a simple Flask API (API.py) that utilizes the tree of thought reasoning for answer generation. This Flask API powers the reasoning engine for the app using a Tree of Thought approach. It receives user prompts at /api/chat, builds a reasoning tree via depth-first search (DFS), scores all possible reasoning paths, and returns the best summarized output. It also includes full CORS support for local frontend communication.

---

## Features

- ✅ Dynamic reasoning tree generation
- 🔄 BFS and DFS traversal modes
- 🧠 Thought generation + scoring with LLM
- 🌱 Branch pruning with top-N child limit
- 📊 Visualization using Graphviz

---

## About Tree of Thought

> Tree of Thought (ToT) is a prompting strategy that guides LLMs to reason more effectively by exploring multiple intermediate thoughts (like a tree), evaluating them, and selecting the best path. This method improves logical reasoning, math, problem-solving, and planning tasks.

Learn more in the [Tree of Thought paper](https://arxiv.org/abs/2305.10601).

---

## Contributing

Pull requests and forks are welcome! Open an issue for bugs, questions, or feature ideas.

---

## Contact:
Author: Bertan Berker

LinkedIn: https://www.linkedin.com/in/bertan-berker/