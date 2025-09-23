## Browserbase MCP Server

AI-powered browser automation via Model Context Protocol, built on [Browserbase](https://www.browserbase.com/) and [Stagehand](https://docs.stagehand.dev/).


## Key Features

- **Natural language control** for clicks, typing, navigation
- **Data extraction** from arbitrary pages
- **Multi-session support** for parallel workflows
- **Screenshots and cookies** for debugging and auth

## Quick Start

1) **Install**: Use the hosted MCP server at `https://server.smithery.ai/@browserbasehq/mcp-browserbase/mcp` or run locally.
2) **Authenticate**: Add your Browserbase API key in MCP config. Get it from the [Browserbase Dashboard](https://www.browserbase.com/overview).
3) **Automate**: Use natural language to drive the browser.

## Common Use Cases

- **Scrape/collect data** across sites
- **Test user flows** and cross-browser behavior
- **Automate forms and reporting** for routine workflows

## Session Modes

Supports single-session (sequential) and multi-session (parallel) automation.

## Available Tools

The Browserbase MCP server provides comprehensive browser automation tools. Here are the key categories:

### Core Browser Automation Tools

- **`browserbase_stagehand_navigate`** - Navigate to any URL
- **`browserbase_stagehand_act`** - Perform actions using natural language (e.g., "click the login button")
- **`browserbase_stagehand_extract`** - Extract all text content from the current page
- **`browserbase_stagehand_observe`** - Find actionable elements on the page
- **`browserbase_screenshot`** - Capture PNG screenshots
- **`browserbase_stagehand_get_url`** - Get current page URL
- **`browserbase_stagehand_get_all_urls`** - Get URLs of all active sessions

### Session Management

**Single Session (Traditional)**
- **`browserbase_session_create`** - Create/reuse a browser session
- **`browserbase_session_close`** - Close the current session

**Multi-Session (Advanced)**
- **`multi_browserbase_stagehand_session_create`** - Create independent sessions
- **`multi_browserbase_stagehand_session_list`** - List all active sessions
- **`multi_browserbase_stagehand_session_close`** - Close specific sessions

All core automation tools have session-specific variants (e.g., `multi_browserbase_stagehand_navigate_session`) for multi-session workflows.

### Multi-Session Use Cases

- **Parallel Data Collection** - Scrape multiple sites simultaneously
- **A/B Testing** - Compare user flows across sessions
- **Cross-Site Operations** - Coordinate actions across websites
- **Backup Sessions** - Keep fallback sessions ready

## Links

- **Complete Tools Reference**: [docs.browserbase.com/integrations/mcp/tools](https://docs.browserbase.com/integrations/mcp/tools)
- **Browserbase MCP Server**: [smithery.ai/server/@browserbasehq/mcp-browserbase](https://smithery.ai/server/@browserbasehq/mcp-browserbase)
- **Stagehand Docs**: [docs.stagehand.dev](https://docs.stagehand.dev/)
- **Browserbase Dashboard**: [browserbase.com/overview](https://www.browserbase.com/overview)
- **Model Context Protocol (MCP)**: [anthropic.com](https://www.anthropic.com/news/model-context-protocol)