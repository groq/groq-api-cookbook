# Agno + Groq MLB Game Recap Generator

This project demonstrates the concept of Mixture of Agents (MoA) using Agno Agents and the Groq API to generate comprehensive MLB game recaps.

## Overview

The Mixture of Agents approach leverages multiple AI agents, each equipped with different language models, to collaboratively complete a task. In this project, we use multiple MLB Writer agents utilizing different language models to independently generate game recap articles based on game data collected from other Agno Agents. An MLB Editor agent then synthesizes the best elements from each article to create a final, polished game recap.

## Setup

1. Create a virtual environment:
```bash
python -m venv agnoenv
```
2. Activate the virtual environment:
- On Unix or MacOS:
  ```
  source agnoenv/bin/activate
  ```
- On Windows:
  ```
  .\agnoenv\Scripts\activate
  ```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Set up your Groq API key as an environment variable:
```bash
export GROQ_API_KEY=<your-groq-api-key>
```

## Usage

Run the Jupyter notebook to see the Mixture of Agents in action:
Mixture-of-Agents-Agno-Groq.ipynb

The notebook demonstrates:
- Fetching MLB game data using specialized tools
- Generating game recaps using multiple AI agents with different language models
- Synthesizing a final recap using an editor agent

## Components

- MLB Researcher: Extracts game information from user questions
- MLB Batting Statistician: Analyzes player boxscore batting stats
- MLB Pitching Statistician: Analyzes player boxscore pitching stats
- MLB Writers (using llama3-8b-8192, gemma2-9b-it, and mixtral-8x7b-32768 models): Generate game recap articles
- MLB Editor: Synthesizes the best elements from multiple recaps

## Requirements

See `requirements.txt` for a full list of dependencies. Key packages include:
- agno
- groq
- pandas
- MLB-StatsAPI

## Further Information

- [Mixture of Agents (MoA) concept](https://arxiv.org/pdf/2406.04692)
- [Agno Agents](https://github.com/agno-agi/agno)
- [Groq API](https://console.groq.com/playground)
- [MLB-Stats API](https://github.com/toddrob99/MLB-StatsAPI)
- [Agno Documentation on tool use/function calling](https://docs.agno.com/introduction)