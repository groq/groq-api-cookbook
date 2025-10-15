<h2 align="center">
 <br>
 <img src="images/groq-logo.png" alt="Groq Logo" width="150">
 <br>
 <br>
Groq API Cookbook
  <br>
</h2>

<p align="center">
  <a href="#getting-started">Getting Started</a> •
  <a href="#tutorials">Tutorials</a> •
 <a href="#have-questions">Questions</a> •
 <a href="#find-a-bug">Bug Reporting</a> •
 <a href="#contributing-to-the-cookbook">Contributing</a>
</p>
<br>

## Getting started
This repository contains a collection of tutorials, sample code, and guidelines for accomplishing tasks with Groq API. To run these examples, you'll need a Groq API key that you can get for free by creating an account [here](https://console.groq.com/). Are you ready to cook? 🚀 

## Tutorials

### 01. Getting Started & Quickstart
- [Groq Quickstart Conversational Chatbot](/tutorials/01-quickstart/groq-quickstart-conversational-chatbot): Build your first conversational chatbot with Groq.
- [Chat History Management](/tutorials/01-quickstart/chat-history): Learn how to manage and persist chat history in your AI applications.
- [Batch Processing](/tutorials/01-quickstart/batch-processing): Process hundreds of requests asynchronously using Groq's batch APIs.

### 02. Tool Use (Function Calling)
- [eCommerce Function Calling](/tutorials/02-tool-use/function-calling-101-ecommerce): Learn how to use function calling with LLMs to create orders and get prices on products.
- [SQL Function Calling](/tutorials/02-tool-use/function-calling-sql): Learn how to use function calling with LLMs to run SQL queries.
- [Stock Market Function Calling (Tutorial)](/tutorials/02-tool-use/llama3-stock-market-function-calling): Learn how to use function calling with LLMs to parse stock market data.
- [Stock Market Function Calling (Replit)](/tutorials/02-tool-use/groqing-the-stock-market-function-calling-llama3): Replit-ready example for the above stock tutorial.
- [Parallel Tool Use](/tutorials/02-tool-use/parallel-tool-use): Learn how to equip your LLM to use multiple tools at the same time.
- [Text to SQL with JSON Mode](/tutorials/02-tool-use/text-to-sql-json-mode): Convert natural language to SQL queries using JSON mode.
- [Verified SQL Function Calling](/tutorials/02-tool-use/verified-sql-function-calling): Learn how to build verified and validated SQL queries with function calling.

### 03. Model Context Protocol (MCP)
- [Browser Use MCP](/tutorials/03-mcp/mcp-browseruse): Equip models via Groq API with Browser Use's tools to enable autonomous website browsing, information extraction, and web pages interaction.
- [BrowserBase MCP](/tutorials/03-mcp/mcp-browserbase): Equip models via Groq API with Browserbase's MCP server for web automation using natural language commands, including tools for web interaction and data extraction.
- [Firecrawl MCP](/tutorials/03-mcp/mcp-firecrawl): Equip GPT-OSS 120B via Groq API with enterprise-grade web scraping capabilities, intelligent data extraction, structured parsing, and deep web research.
- [Exa MCP](/tutorials/03-mcp/mcp-exa): Use Exa's web search and web crawling tools to get real-time information from the internet. Find relevant search results, extract data from websites, and run deep-research.
- [Tavily MCP with Groq](/tutorials/03-mcp/mcp-tavily): Build a real-time research agent with the Tavily MCP and Groq API.
- [HuggingFace MCP with Groq](/tutorials/03-mcp/mcp-huggingface): Retrieve real-time HuggingFace model data with the HuggingFace MCP and Groq API.
- [Parallel MCP with Groq](/tutorials/03-mcp/mcp-parallel): Real-time search with access to live data with the Parallel MCP and Groq API (along with a performance comparison against OpenAI).

### 04. Retrieval-Augmented Generation (RAG)
- [Benchmarking RAG with Langchain](/tutorials/04-rag/benchmarking-rag-langchain): Learn how to benchmark a RAG pipeline with LangChain.
- [Presidential Speeches RAG](/tutorials/04-rag/presidential-speeches-rag): Learn how to use RAG to find relevant presidential speeches from input text.
- [Presidential Speeches RAG with Pinecone](/tutorials/04-rag/presidential-speeches-rag-with-pinecone): Learn how to implement RAG using Pinecone as your vector database.
- [Whisper and RAG](/tutorials/04-rag/whisper-podcast-rag): Learn how to use a speech-to-text model and RAG to semantically search through podcast audio.
- [Chat with Website](/tutorials/04-rag/chat_with_website): Learn how to build a chatbot that can answer questions about website content using RAG.

### 05. Structured Output (JSON Mode)
- [JSON Mode with Health Data](/tutorials/05-structured-output/json-mode-social-determinants-of-health): Learn how to use JSON mode to generate structured health analytics from raw data.
- [Structured Output with Instructor](/tutorials/05-structured-output/structured-output-instructor): Learn how to use the Instructor library to create structured output with tools and objects.

### 06. Multimodal (Vision & Audio)
- [Batch Image Processing](/tutorials/06-multimodal/batch-analyze-images): Learn how to process and analyze thousands of images using Llama 4 Maverick's multimodal capabilities with [Groq Batch APIs](https://console.groq.com/docs/batch).
- [Multimodal Image Processing](/tutorials/06-multimodal/multimodal-image-processing): Process and analyze images using vision models.
- [Audio Chunking](/tutorials/06-multimodal/audio-chunking): Learn how to efficiently chunk and process audio files with Whisper, a speech-to-text model.
- [Instagram Reel Subtitler](/tutorials/06-multimodal/instagram-reel-subtitler): Learn how to automatically and instantly generate subtitles for Instagram reels using a speech-to-text model.

### 07. Agents & Multi-Agent Systems
- [Mixture of Agents](/tutorials/07-agents/mixture-of-agents): Learn how to create a mixture-of-agents system powered by Groq.
- [Game Recap with MoA](/tutorials/07-agents/agno-mixture-of-agents): Learn how to use a mixture-of-agents approach to generate comprehensive MLB game recaps.
- [CrewAI Mixture of Agents](/tutorials/07-agents/crewai-mixture-of-agents): Learn how to build a mixture of agents application with CrewAI.
- [CrewAI Agents (Replit)](/tutorials/07-agents/crewai-agents): Replit-ready CrewAI agent example.
- [Langroid LLM Agents](/tutorials/07-agents/langroid-llm-agents): Learn how to create a multi-agent system using Langroid and Groq.
- [Composio Newsletter Summarizer Agent](/tutorials/07-agents/composio-newsletter-summarizer-agent): Build an agent that summarizes newsletters using Composio and Groq.
- [aiXplain Agents](/tutorials/07-agents/aiXplain-agents): Build intelligent agents using aiXplain's platform with Groq.
- [Minions with Groq](/tutorials/07-agents/minions-groq): Create lightweight agent workers (minions) for distributed tasks.

### 08. Integrations & Frameworks
- [Gradio with Groq](/tutorials/08-integrations/groq-gradio): Learn how to build a full-stack application with Gradio powered by Groq.
- [Streamlit with Groq](/tutorials/08-integrations/groq_streamlit_demo): Learn how to build a full-stack chat application with Streamlit powered by Groq.
- [LangChain Conversational Chatbot](/tutorials/08-integrations/conversational-chatbot-langchain): Build conversational chatbots using LangChain and Groq.
- [LlamaIndex Conversational Chatbot](/tutorials/08-integrations/llamachat-conversational-chatbot-with-llamaIndex): Create chat applications using LlamaIndex with Groq.
- [Portkey with Groq](/tutorials/08-integrations/Portkey-with-Groq): Learn how to integrate Portkey for AI observability into Groq usage.
- [Portkey: OpenAI to Groq Migration](/tutorials/08-integrations/portkey-openai-to-groq): Learn how to seamlessly migrate from OpenAI to Groq using Portkey.
- [E2B Code Interpreting](/tutorials/08-integrations/e2b-code-interpreting): Learn how to integrate code execution for LLMs with the Code Interpreter SDK by E2B.
- [JigsawStack Prompt Engine](/tutorials/08-integrations/jigsawstack-prompt-engine): Learn how to automate your workflow and choose the best LLM for your prompts using JigsawStack's Prompt Engine powered by Groq.
- [JigsawStack Prompt Engine (Replit)](/tutorials/08-integrations/jigsawstack-prompt-engine-replit): Replit-ready JigsawStack example.
- [LiteLLM Proxy with Groq](/tutorials/08-integrations/litellm-proxy-groq): Learn how to call Groq API through the LiteLLM proxy.
- [Toolhouse with Groq](/tutorials/08-integrations/toolhouse-for-tool-use-with-groq-api): Learn how to use Toolhouse to create simple tool integrations with Groq.

### 09. Observability & Evaluation
- [OpenTelemetry with Groq](/tutorials/09-observability/opentelemetry-observability-groq): Learn how to integrate OpenTelemetry tracing and metrics for insights into Groq usage.
- [Arize Phoenix: Evaluate Groq Agents](/tutorials/09-observability/arize-phoenix-evaluate-groq-agent): Learn how to evaluate and monitor your Groq-powered agents using Arize Phoenix.

### 10. Guardrails & Safety
- [Content Filtering with Llama Guard](/tutorials/10-guardrails/llama-guard-safe-chatbot): Learn how to use Llama Guard to help prevent abuse and engagement with inappropriate content.
- [Image Moderation](/tutorials/10-guardrails/image_moderation.ipynb): Learn how to implement image moderation and content filtering for visual content.


## Have questions?
Join our [Developer Community Forum](https://community.groq.com/) where we discuss new features and news in the AI industry, share guidance, and collaborate.

## Find a bug?
Open an issue on GitHub [here](https://github.com/groq/groq-api-cookbook/issues). 

## Contributing to the Cookbook
The Groq API Cookbook is community-driven and we are always looking for contributions in the forms of ideas, fixes, improvements, or suggestions! We greatly appreciate the open-source community and are committed to helping our community get good resources.

If you're interested in contributing to our cookbook, please first check out our [contribution guidelines](https://github.com/groq/groq-api-cookbook/blob/main/CONTRIBUTING.md). We welcome high-quality guides and examples that will help our community and can't wait to see what you cook up! 🧑‍🍳

If there are guides or examples that you'd like to see in the future, feel free to make a suggestion [here](https://github.com/groq/groq-api-cookbook/issues).
