# Real-Time Voice Agent with Groq + Agora

Build a production-ready voice agent using Groq for fast LLM inference and Agora's Conversational AI for real-time audio streaming.

## Overview

Voice agents are latency-sensitive—the gap between user speech and agent response directly impacts UX. This tutorial demonstrates a hybrid approach that reduced response latency by approximately 50%:

| Component | Provider | Why |
|-----------|----------|-----|
| LLM Inference | Groq | Fast inference reduces "thinking" time |
| Audio Streaming | Agora | Managed real-time infrastructure |
| Text-to-Speech | OpenAI | Groq TTS currently in beta |

## Architecture
```
┌─────────────────┐
│  User Browser   │
│ (Agora RTC SDK) │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Next.js API    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   Agora Conv.   │
│   AI Engine     │
└────────┬────────┘
         │
    ┌────┴────┐
    ↓         ↓
┌───────┐ ┌────────┐
│ Groq  │ │ OpenAI │
│ (LLM) │ │ (TTS)  │
└───────┘ └────────┘
```

## Prerequisites

- [Groq API Key](https://console.groq.com/)
- [Agora Account](https://console.agora.io/) with App ID, App Certificate, Customer ID, Customer Secret
- [OpenAI API Key](https://platform.openai.com/api-keys) for TTS
- Docker (recommended) or Node.js 20+

## Quick Start
```bash
git clone https://github.com/Alderson-dev/Coffee-Shop-AI-Voice-Agent.git
cd Coffee-Shop-AI-Voice-Agent
cp .env.example .env
# Add your API keys to .env
docker-compose up -d
```

Access the application at `http://localhost:3000`

## Key Implementation

The core integration configures Groq as a custom LLM provider within Agora's agent config:
```typescript
const agentConfig = {
  llm: {
    provider: "custom",
    url: "https://api.groq.com/openai/v1",
    model: "llama-3.3-70b-versatile",
    api_key: process.env.GROQ_API_KEY,
  },
  tts: {
    provider: "openai",
    model: "tts-1",
    voice: "alloy",
    api_key: process.env.OPENAI_API_KEY,
  },
  asr: {
    provider: "agora",
    language: "en-US",
  },
};
```

## Why Hybrid TTS?

Groq lists TTS support as a beta feature in Agora integrations. During testing, this wasn't enabled for my account. The hybrid approach (Groq LLM + OpenAI TTS) still delivers significant latency improvements where it matters most—the inference step.

## What's Included

The full repository includes:

- Next.js frontend with Agora RTC SDK integration
- API routes for agent lifecycle management
- Docker and docker-compose configuration
- Health check endpoints
- Caddy reverse proxy for HTTPS

## Full Source Code

**Repository:** [github.com/Alderson-dev/Coffee-Shop-AI-Voice-Agent](https://github.com/Alderson-dev/Coffee-Shop-AI-Voice-Agent)

## Resources

- [Groq API Documentation](https://console.groq.com/docs)
- [Agora Conversational AI Documentation](https://docs.agora.io/en/conversational-ai/)
- [Agora Conversational AI Quickstart](https://docs.agora.io/en/conversational-ai/get-started/quickstart)

## Author

[Mitchell Alderson](https://github.com/Alderson-dev) - [alderson.dev](https://alderson.dev)
