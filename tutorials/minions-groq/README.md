# Minions with Groq API Cookbook for Multi-Hop Reasoning

## 1. Introduction to Minions

Minions is a framework developed by Stanford's [Hazy Research lab](https://hazyresearch.stanford.edu/blog/2025-02-24-minions) that enables efficient collaboration between small, local models running on your device and large, powerful models running in the cloud. By combining Minions with Groq's fast inference and cost-effectiveness, you get reduced costs, minimal latency, and high-quality results similar to using large models exclusively. We will be exploring Minions in general, and then investigating how it is specifically well-suited for multi-hop question-answering, a challenging type of question where frontier models still struggle.

## 2. Minion and MinionS Protocols

The framework offers two main protocols:

The Minion Protocol is a small, on-device or local model chatting with a cloud-based model to reach a solution without sending long context to the cloud, while the MinionS protocol is a cloud model decomposing the task into smaller subtasks that are executed in parallel by the local model before being aggregated by the local model. While Minion offers slightly lower performance, it is more cost-effective than MinionS. 
One should consider the complexity of the task when deciding between Minion and MinionS based on the trade-off between cost and performance.

## 3. What is Multi-Hop Reasoning?

### Traditional Approaches to Multi-Hop QA

Multi-hop reasoning refers to answering questions that require connecting multiple pieces of information across different sources or parts of a document. Traditionally, multi-hop QA has been approached through:

1. **Retrieval-Augmented Generation (RAG)**: Systems retrieve multiple relevant passages and then generate answers, but often struggle with complex reasoning chains.

2. **Pipeline Approaches**: Breaking questions into sub-questions, retrieving information for each, then combining results - but these systems are complex to build and maintain.

3. **Single Large Model Calls**: Using frontier models with large context windows to process all information at once - effective but extremely expensive and often inefficient.

### Examples of Multi-Hop Questions

Consider these examples that require multiple reasoning steps:
- "How did the 2008 housing crisis affect average retirement savings by 2010?"
- "Compare NVIDIA and Apple's stock performance during the AI boom of 2023"
- "How did Britain's and France's economic recovery differ in the Great Depression?"

#### Anatomy of a Multi-Hop Question

Let's break down how one would approach the question about Britain and France's economic recovery:

1. **First Hop**: Identify when the Great Depression occurred (approximate timeframe)

2. **Second Hop**: Gather information about Britain's economic recovery during this period

3. **Third Hop**: Gather information about France's economic recovery during this period

4. **Fourth Hop**: Compare the two countries' economic recovery

5. **Final Synthesis**: Draw conclusions about how each country recovered from and was affected by the Great Depression

This multi-step process requires gathering different pieces of information and connecting them in a logical sequence - exactly what makes multi-hop reasoning challenging.

### Current Limitations

Single-call approaches to multi-hop reasoning face several challenges:
- High tendency for models to hallucinate when connections aren't explicit
- High token costs when processing large documents
- Difficulty maintaining focus across multiple steps

## 4. Why MinionS is Suited for Multi-Hop Reasoning

The MinionS architecture of decomposing a query into tasks and synthesizing a final response is well-suited for multi-hop question-answering, as it helps form connections, identify separate pieces of information, and compare them effectively. 

### Current Implementation

Let us consider the multi-hop question in the example file we have provided: 
"How did Britain's and France's economic recovery differ in the Great Depression?"

Here is how MinionS would go ahead and answer this question: 

**1. Initial Task Decomposition:**
The remote model hosted on Groq typically will break the task into two parallel tasks, such as:
```python
Task 1: "Extract information about Britain's economic recovery during the Great Depression."
Task 2: "Extract information about France's economic recovery during the Great Depression."
```

**2. Parallel Local Processing:**
The local model will these tasks against the context document, returning structured outputs:
```json
{
    "explanation": "Britain devalued its currency early and experienced less severe impacts...",
    "citation": "Britain, Argentina and Brazil, all of which devalued their currencies early and returned to normal patterns of growth relatively rapidly...",
    "answer": "Britain's early currency devaluation helped it recover more quickly..."
}
```

**3. Expert Aggregation:**
Finally, the remote model on Groq synthesizes the parallel outputs from the local models into a final answer. This final answer effectively answers the multi-hop question, combining information from several parts of the context. 

## 5. Conclusion

By leveraging the Minions framework with Groq's fast inference capabilities, developers can build applications that handle complex multi-hop reasoning tasks efficiently and cost-effectively. The MinionS protocol in particular offers a powerful alternative to traditional approaches, maintaining near-frontier model quality while significantly reducing costs and running on local devices. 

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
```bash
export GROQ_API_KEY=YOUR_GROQ_API_KEY
```

## Example Code
Go ahead and run the example code: 
```bash
python groq_minions.py
```

## Additional Resources
- [Minions GitHub Repository](https://github.com/HazyResearch/minions)
- [Groq API Documentation](https://console.groq.com/docs)
- [Minions Research Paper](https://arxiv.org/abs/2402.15688)
