# Groq Mixture of Agents (MOA) in TypeScript

This project implements a Mixture of Agents (MOA) approach using Groq's API to generate more comprehensive and nuanced responses to questions. It's inspired by the work done by together.ai on multi-agent systems.

## Prerequisites

- [Bun.js](https://bun.sh/) installed on your system
- A Groq API key (obtainable from [console.groq.com](https://console.groq.com))

## Installation

1. Clone this repository
2. Install dependencies:

```bash
bun install
```

3. Create a `.env` file in the root directory and add your Groq API key:

```
GROQ_API_KEY=your_api_key_here
```

## How it works

The MOA process uses multiple language models (agents) to generate a response, cycling through them to refine the output. Here's a simplified overview of the process:

1. The main question is sent to multiple "layer agents".
2. Each layer agent processes the question and generates a response.
3. These responses are combined and fed back into the system for further refinement.
4. After a specified number of cycles, a final response is generated.

Let's look at some key parts of the code:

### Configuration (moaConfig.ts)

```typescript
export const moaConfig: MOAConfig = {
  mainModel: "mixtral-8x7b-32768",
  cycles: 2,
  mainModelTemperature: 0.7,
  layerAgentConfig: {
    layer_agent_1: {
      systemPrompt:
        "Think through your response step by step. {helper_response}",
      modelName: "llama3-8b-8192",
      temperature: 0.5,
    },
    // ... other layer agents
  },
};
```

This configuration specifies the main model, number of cycles, and the configuration for each layer agent.

### MOA Service (moaService.ts)

The `runMOA` function orchestrates the process:

```typescript
export const runMOA = async (
  input: string,
  config: MOAConfig,
  onUpdate: (update: string) => void
): Promise<string> => {
  const runCycle = async (
    cycleCount: number,
    helperResponse: string
  ): Promise<string> => {
    if (cycleCount === 0) {
      // Generate final response
    }

    onUpdate(`Cycle ${config.cycles - cycleCount + 1}:`);
    const newHelperResponse = await runLayerAgents(
      input,
      helperResponse,
      config.layerAgentConfig
    );
    onUpdate(newHelperResponse);
    return runCycle(cycleCount - 1, newHelperResponse);
  };

  return runCycle(config.cycles, "");
};
```

This function runs the specified number of cycles, calling the layer agents in each cycle and refining the response.

## Running the server

To start the server:

```bash
bun run src/app.ts
```

Or in development mode with hot reloading:

```bash
bun run dev
```

## Making a request

You can use curl to send a question to the MOA system:

```bash
curl -X POST http://localhost:3000/moa/process \
-H "Content-Type: application/json" \
-d '{"question": "Explain the importance of low latency LLMs"}'
```

This will return a stream of responses, showing the output from each cycle and the final response.

## Why use MOA?

The Mixture of Agents approach can provide several benefits:

1. Diverse perspectives: By using multiple models with different prompts, you get a range of viewpoints on the question.
2. Iterative refinement: The cycling process allows for progressive improvement of the response.
3. Specialization: Different agents can be configured to focus on specific aspects of the question or response.

This project demonstrates how to implement such a system using Groq's API and TypeScript, providing a flexible framework for experimenting with multi-agent AI systems.
