# Build a bounded tool-calling agent with Groq and AgentsKit

Calling a model is only one part of an agent loop. A useful agent also has to expose tools, preserve tool-call identity across turns, return results to the model in the provider's expected format, stop predictably, and leave an inspectable record of what happened.

This TypeScript example uses Groq for inference and AgentsKit for that orchestration. It investigates a synthetic checkout incident with two small local tools and a hard four-step limit. No database, cloud account, or second API key is required.

## What the example demonstrates

- Groq tool calling through the `@agentskit/adapters` Groq adapter
- Type-inferred local tools defined with JSON Schema
- A bounded observe → tool → result loop with `maxSteps`
- Structured tool results and stable tool-call IDs across model turns
- An inspectable result containing the final answer, step count, tool calls, statuses, and duration
- Deterministic tests that do not call Groq or require credentials

The sample data is intentionally local and synthetic. The useful pattern is the boundary: replace the two tool bodies with calls to your metrics and deployment systems without changing the agent loop or binding the application to a provider-specific SDK.

## Prerequisites

- Node.js 20.6 or newer
- A [Groq API key](https://console.groq.com/keys)

## Run it

```bash
npm install
cp .env.example .env
# Add your Groq API key to .env
npm start
```

You can also provide a different incident prompt:

```bash
npm start -- "Investigate the checkout service and recommend a safe next action."
```

The default model is `openai/gpt-oss-120b`. Check Groq's [supported models](https://console.groq.com/docs/models) before pinning a model in a production application. You can override it in `.env` with `GROQ_MODEL`.

## How the loop is bounded

`src/agent.ts` creates one runtime with the Groq adapter, two explicit tools, and `maxSteps: 4`. Each step can ask Groq for a response, execute requested local tools, and feed their stringified JSON results into the next request. If the model responds without another tool call, the run ends earlier.

The system prompt makes the evidence boundary explicit: the agent must use tools before asserting facts, distinguish evidence from inference, and avoid inventing unavailable logs or services. In a real incident workflow, pair the step limit with tool-level authorization, timeouts, and operational approval gates appropriate to your environment.

## Inspect the result

The CLI prints the final triage followed by a compact run summary:

```json
{
  "model": "openai/gpt-oss-120b",
  "steps": 3,
  "toolCalls": [
    { "id": "...", "name": "get_service_health", "status": "complete" },
    { "id": "...", "name": "list_recent_deployments", "status": "complete" }
  ],
  "durationMs": 812
}
```

Tool-call IDs are not decoration. OpenAI-compatible APIs use them to associate each tool result with the assistant request that produced it. AgentsKit carries those IDs through the runtime and the Groq adapter maps the conversation to the compatible wire format.

## Validate without spending tokens

The tests use a scripted adapter, so they are deterministic and require no API key:

```bash
npm run typecheck
npm test
```

They verify the synthetic tools, the four-step ceiling, tool-call identity, structured result handoff, and the final run record.

## Project layout

```text
src/
  agent.ts          Groq adapter and bounded runtime
  incident-data.ts  Synthetic service and deployment records
  index.ts          Runnable CLI
  tools.ts          Typed local tools
test/
  agent.test.ts     Credential-free runtime tests
```

## Next steps

- Replace the synthetic records with read-only observability and deployment clients.
- Add argument validation and authorization before exposing tools to production data.
- Attach an AgentsKit observer to send runtime events to your observability backend.
- Keep provider selection at the adapter boundary so the rest of the agent remains portable.

Learn more in the [AgentsKit documentation](https://www.agentskit.io/docs) and Groq's [local tool-calling guide](https://console.groq.com/docs/tool-use/local-tool-calling).
