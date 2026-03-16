## AG2 Multi-Agent Research Assistant with Groq

[AG2](https://ag2.ai) (formerly AutoGen) is an open-source framework for building multi-agent AI applications. This tutorial demonstrates two AG2 agents collaborating on a web research task using Groq's fast inference and DuckDuckGo search.

### Overview

A **Researcher** agent uses DuckDuckGo to search the web for information, while a **Reviewer** agent evaluates the research quality and asks follow-up questions. The two agents chat back and forth until the Reviewer is satisfied with the findings.

This showcases:
- AG2's `ConversableAgent` with Groq via `api_type='groq'`
- Built-in `DuckDuckGoSearchTool` for live web search (no API key needed)
- Multi-agent conversation using `initiate_chat`

### Setup

Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set your Groq API key:

```bash
export GROQ_API_KEY=gsk_...
```

### Run

Open the notebook:

```bash
jupyter notebook ag2-multi-agent-research.ipynb
```

### Requirements

- Python 3.10+
- A [Groq API key](https://console.groq.com/keys)
- No additional API keys required (DuckDuckGo search is free)

### References

- [AG2 Documentation](https://docs.ag2.ai)
- [Groq Console](https://console.groq.com)
- [AG2 Tool Registration](https://docs.ag2.ai/docs/tutorial/tool-use)
