<h2 align="center">
 <br>
 <img src="images/Aixplain Logo.png" alt="aiXplain Logo" width="150">
 <br>
</h2>

# Travel Agent Powered by aiXplain

## Overview

This project demonstrates the capabilities of the aiXplain platform in creating a modular multi-agent. The Travel Agent combines advanced AI models, real-time data integration, and robust orchestration features to provide personalized and adaptive travel planning experiences.

Built on aiXplain, this platform showcases how developers can easily design, build, and deploy intelligent agents without requiring extensive AI/ML expertise.

## Why aiXplain?

aiXplain is a comprehensive platform designed for building, optimizing, and deploying multi-agent systems with ease. Key highlights include:

- **Wide Range of Models**: Access over 100 Large Language Models (LLMs) and 38,000+ AI tools from leading providers like Groq, OpenAI, and Google.
- **Single Access Key**: Simplify model integration with a single-key system and enjoy the best pricing across platforms.
- **Modular AI Agents**: Build standalone or multi-agent systems that are customizable and ready for real-world tasks.
- **Integrated Tooling**: Fine-tune models, benchmark performance, and integrate advanced debugging features effortlessly.
- **Enterprise-Ready**: Provides robust security, scalability, and compliance for professional deployments.

## Features Demonstrated in This Project
### 1. Agent Design and Orchestration
- **Scraper Utility Agent**: Gathers insights from travel blogs and review platforms.
- **Location Agent**: Offers personalized recommendations for nearby landmarks and activities.
- **Weather Agent**: Provides real-time weather updates and forecasts.

### 2. Team Agents
- Combines individual agents into a cohesive system, enabling them to work collaboratively for complex workflows.

### 3. Effortless Deployment
- Publish agents as APIs with a single click using aiXplain's streamlined interface.
- Integrate APIs into applications via OpenAI standards, Python, Swift, or cURL.


## How to Use aiXplain for Your Projects

### Install the aiXplain SDK

```python
pip install aixplain
```

### Obtain Your Access Key
Register on aiXplain and retrieve your access key from the [Integrations](https://platform.aixplain.com/account/integrations) page. 

```python
import os
os.environ["AIXPLAIN_API_KEY"] = "<YOUR_ACCESS_KEY>"
```

### Build Your Agent
Utilize `AgentFactory` to design agents with specific functionalities:

```python
from aixplain.factories import AgentFactory

scraper_agent = AgentFactory.create(
    name="Scraper Utility Agent",
    description="Gathers travel insights based on user preferences.",
    tools=[...],
    llm_id="..."
)
```

### Combine Agents into a Team
Create a multi-agent system for complex workflows:

```python
from aixplain.factories import TeamAgentFactory

team_agent = TeamAgentFactory.create(
    name="Travel Agent",
    description="A comprehensive travel planning system.",
    agents=[scraper_agent, location_agent, weather_agent]
)
```

### Run and Deploy
Test and deploy your agents to generate APIs for integration:

```python
result = team_agent.run("Plan a day trip to Boston")
print(result)
```
Deploy your agent when you are ready:

```python
team_agent.deploy()
```

## See it in action

<div style="position: relative; padding-bottom: 58.15831987075929%; height: 0;"><iframe src="https://www.loom.com/embed/127a7f6691514035bcf2877ccfcda1eb?sid=8c740ef3-59c4-49a3-8d78-0085059aba41" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

## Learn More
Explore aiXplain's capabilities: [aiXplain Platform](https://aixplain.com/)<br>
Access tutorials and guides: [aiXplain Documentation](https://www.google.com/url?q=https%3A%2F%2Fdocs.aixplain.com)<br>
Join the community: [aiXplain Discord](https://www.google.com/url?q=https%3A%2F%2Fhttps%3A%2F%2Fdiscord.com%2Finvite%2FT5dCmjRSYA)

Start building intelligent systems with aiXplain today and transform how you deploy AI solutions! 🚀🤖