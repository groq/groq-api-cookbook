# Groq + Google Workspace MCP Integration

This tutorial demonstrates how to connect Groq's ultra-fast inference with Google Workspace (Gmail, Google Calendar, and Google Drive) using Model Context Protocol (MCP) connectors.

## Video Walkthrough

https://github.com/user-attachments/assets/0b3e6805-a5f9-4ac8-a9a0-bc0beaee8590

*Watch how to integrate Gmail, Calendar, and Drive with Groq's MCP connectors*

---

## What You'll Learn

- How to authenticate with Google Workspace using OAuth 2.0
- Setting up MCP connectors for Gmail, Calendar, and Drive
- Building AI agents that can:
  - Search and summarize emails
  - Check calendar schedules and events
  - Search and manage Google Drive documents
  - Find and analyze PDF files in Drive
  - Coordinate actions across multiple Google services

## Prerequisites

- **Groq API Key**: Get yours at [console.groq.com](https://console.groq.com/keys)
- **Google Workspace OAuth Token**: Obtain from [Google OAuth Playground](https://developers.google.com/oauthplayground/) with appropriate scopes
- Python 3.8+

## Required OAuth Scopes

To use the Google Workspace MCP connectors, you need to authorize your OAuth token with these **exact scopes**:

**From Gmail API v1:**
- `https://www.googleapis.com/auth/gmail.modify` - Read and modify Gmail messages

**From Google Calendar API v3:**
- `https://www.googleapis.com/auth/calendar.events` - Manage calendar events

**From Drive API v3:**
- `https://www.googleapis.com/auth/drive.readonly` - Download the content of Drive files

**From Google OAuth2 API v2:**
- `https://www.googleapis.com/auth/userinfo.email` - View your email address
- `https://www.googleapis.com/auth/userinfo.profile` - View your basic profile info

### How to Get OAuth Token

1. Visit [Google OAuth Playground](https://developers.google.com/oauthplayground/)
2. In Step 1, select **all five scopes** listed above
3. Click "Authorize APIs" and sign in
4. In Step 2, click "Exchange authorization code for tokens"
5. Copy the Access token (starts with `ya29.`)

**Note:** OAuth tokens expire after ~1 hour. Refresh as needed.

## Installation

```bash
pip install -r requirements.txt
```

## Testing with curl

If you prefer to test the connectors directly without Python, use these curl commands:

### Gmail Connector
```bash
curl -X POST https://api.groq.com/api/openai/v1/responses \
  -H "Authorization: Bearer YOUR_GROQ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-oss-20b",
    "tools": [{
      "type": "mcp",
      "server_label": "gmail",
      "connector_id": "connector_gmail",
      "authorization": "YOUR_GMAIL_OAUTH_TOKEN",
      "require_approval": "never"
    }],
    "input": "Show me my last 3 unread emails"
  }'
```

### Google Calendar Connector
```bash
curl -X POST https://api.groq.com/api/openai/v1/responses \
  -H "Authorization: Bearer YOUR_GROQ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-oss-20b",
    "tools": [{
      "type": "mcp",
      "server_label": "google_calendar",
      "connector_id": "connector_googlecalendar",
      "authorization": "YOUR_CALENDAR_OAUTH_TOKEN",
      "require_approval": "never"
    }],
    "input": "What 3 events do I have next on my primary google calendar"
  }'
```

### Google Drive Connector
```bash
curl -X POST https://api.groq.com/api/openai/v1/responses \
  -H "Authorization: Bearer YOUR_GROQ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-oss-20b",
    "tools": [{
      "type": "mcp",
      "server_label": "googledrive",
      "connector_id": "connector_googledrive",
      "authorization": "YOUR_DRIVE_OAUTH_TOKEN",
      "require_approval": "never"
    }],
    "input": "Search for PDF files in my Google Drive"
  }'
```

## Quick Start

1. Set up your environment variables:
```bash
export GROQ_API_KEY='your_groq_api_key'
export GSUITE_ACCESS_TOKEN='your_oauth_token'
```

2. Open the Jupyter notebook:
```bash
jupyter notebook mcp-google-workspace.ipynb
```

3. Follow the notebook to run various examples

## Features

### 1. Gmail Integration
- Search emails with natural language queries
- Summarize email threads
- Draft and send emails
- Manage labels and folders

### 2. Google Calendar Integration
- Check daily/weekly schedules
- Find meeting conflicts
- Analyze time usage patterns
- Create and update events

### 3. Google Drive Integration
- Search documents by content or metadata
- Find and filter PDF files specifically
- Find recently modified files
- Organize and categorize documents
- Export files in different formats

### 4. Multi-Service Workflows
- Cross-reference emails with calendar events
- Find meeting-related documents
- Build custom productivity automations

## Example Use Cases

- **Executive Assistant**: Triage emails, prepare for meetings, manage calendar
- **Email Management**: Auto-categorize, summarize, and prioritize messages
- **Meeting Intelligence**: Find relevant documents before calls
- **Document Discovery**: Natural language search across all your Drive files
- **PDF Analysis**: Search for and analyze PDF reports, invoices, and documents
- **Schedule Optimization**: Analyze calendar patterns and find optimal meeting times

## Resources

- **Groq Console**: [console.groq.com](https://console.groq.com)
- **Google Workspace APIs**: [developers.google.com/workspace](https://developers.google.com/workspace)
- **OAuth Playground**: [developers.google.com/oauthplayground](https://developers.google.com/oauthplayground/)

## Notes

- OAuth tokens expire after a certain period; you'll need to refresh them
- Be mindful of API rate limits for both Groq and Google Workspace
- Always use the minimum required OAuth scopes for your use case
- Test with read-only scopes first before using write permissions
