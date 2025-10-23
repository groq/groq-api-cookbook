## E2B MCP Gateway

Run multiple isolated MCP servers together in a single [E2B](https://e2b.dev/) sandbox, powered by Groq's ultra-fast inference.

## What is E2B MCP Gateway?

[E2B's MCP Gateway](https://e2b.dev/docs/mcp) provides a unified interface to run multiple Model Context Protocol (MCP) servers inside isolated sandboxes. Instead of connecting to each MCP server separately, [E2B](https://e2b.dev/) creates a single gateway endpoint that routes requests to all configured MCPs—giving your AI access to 200+ tools through one connection.

## Key Features

- **Unified Gateway** - One endpoint for multiple MCP servers (Exa, Browserbase, Notion, etc.)
- **Isolated Sandboxes** - Each workflow runs in its own secure Linux environment
- **Combined Capabilities** - Mix search, browser automation, data storage, and more
- **Type-Safe** - Full TypeScript/Python SDK support
- **Fast Setup** - Configure multiple MCPs in seconds

## Quick Start

1. **Sign up for services**:
   - [E2B](https://e2b.dev/) - Get API key for sandbox management
   - [Browserbase](https://www.browserbase.com/) - Get API key + Project ID for browser automation
   - [Exa](https://dashboard.exa.ai/) - Get API key for web search
   - [Groq](https://console.groq.com/) - Get API key for LLM inference

All services have a free tier that is enough for this demo.

2. **Install dependencies**:
   ```bash
   pip install e2b openai
   ```

3. **Set environment variables**:
   ```bash
   export E2B_API_KEY='your_e2b_key'
   export BROWSERBASE_API_KEY='your_browserbase_key'
   export BROWSERBASE_PROJECT_ID='your_project_id'
   export EXA_API_KEY='your_exa_key'
   export GROQ_API_KEY='your_groq_key'
   ```

4. **Run the notebook** - Open `mcp-e2b.ipynb` to see it in action

## Common Use Cases

### Research & Verification
- Search for information with Exa
- Visit source websites with Browserbase to verify
- Extract and structure data for analysis

### Lead Generation
- Find companies with Exa
- Browse to their websites with Browserbase
- Extract contact info and pricing details

### Competitive Intelligence
- Search for competitors with Exa
- Monitor their sites with Browserbase
- Track changes over time

### Content Creation
- Research topics with Exa
- Screenshot examples with Browserbase
- Compile findings into reports

## Available Tools

### From Exa MCP
- **`web_search_exa`** - AI-powered web search for current information
- **`company_research`** - Research companies by crawling official websites
- **`crawling`** - Extract content from specific URLs
- **`linkedin_search`** - Search LinkedIn for companies and people
- **`deep_researcher_start`** - Start comprehensive research report
- **`deep_researcher_check`** - Get completed research results

### From Browserbase MCP
- **`browserbase_stagehand_navigate`** - Navigate to URLs
- **`browserbase_stagehand_act`** - Perform actions with natural language
- **`browserbase_stagehand_extract`** - Extract page content
- **`browserbase_stagehand_observe`** - Find interactive elements
- **`browserbase_screenshot`** - Capture page screenshots
- **`browserbase_session_create`** - Create browser sessions
- **`browserbase_session_close`** - Close browser sessions

## Why E2B + Groq?

**[E2B](https://e2b.dev/)'s Advantage**: Instead of managing separate connections to Exa's MCP, Browserbase's MCP, and others, [E2B](https://e2b.dev/) creates one gateway that hosts them all. Your AI agent can seamlessly use web search, browser automation, and any other MCP tool through a single endpoint.

**[Groq](https://groq.com/)'s Speed**: With up to 500+ tokens/second, [Groq](https://groq.com/) handles tool orchestration and response generation in milliseconds—making multi-step research workflows feel instant.

## Links

### E2B Resources
- **E2B Homepage**: [e2b.dev](https://e2b.dev/)
- **E2B MCP Gateway Docs**: [e2b.dev/docs/mcp](https://e2b.dev/docs/mcp)
- **E2B MCP Quickstart**: [e2b.dev/docs/mcp/quickstart](https://e2b.dev/docs/mcp/quickstart)
- **E2B Available MCP Servers**: [e2b.dev/docs/mcp/available-servers](https://e2b.dev/docs/mcp/available-servers)
- **E2B Custom Servers**: [e2b.dev/docs/mcp/custom-servers](https://e2b.dev/docs/mcp/custom-servers)
- **E2B GitHub**: [github.com/e2b-dev/e2b](https://github.com/e2b-dev/e2b)

### MCP Servers
- **Exa MCP Documentation**: [docs.exa.ai/reference/exa-mcp](https://docs.exa.ai/reference/exa-mcp)
- **Exa MCP GitHub**: [github.com/exa-labs/exa-mcp-server](https://github.com/exa-labs/exa-mcp-server)
- **Browserbase MCP Server**: [hub.docker.com/r/mcp/browserbase](https://hub.docker.com/r/mcp/browserbase)
- **Stagehand Documentation**: [docs.stagehand.dev](https://docs.stagehand.dev/)

### Groq & MCP
- **Groq API Documentation**: [console.groq.com/docs](https://console.groq.com/docs)
- **Groq Models**: [console.groq.com/docs/models](https://console.groq.com/docs/models)
- **Model Context Protocol**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **MCP Specification**: [spec.modelcontextprotocol.io](https://spec.modelcontextprotocol.io)

