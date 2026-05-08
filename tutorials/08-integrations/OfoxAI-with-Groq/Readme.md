# OfoxAI with Groq

[OfoxAI](https://ofox.ai) is a unified API gateway that provides developers access to 100+ LLMs—including Groq-powered models—through a single OpenAI-compatible endpoint. This guide walks you through accessing Groq's ultra-fast inference through OfoxAI.

## Why OfoxAI + Groq?

- **Groq's speed**: Ultra-low latency inference for Llama, Gemma, Mixtral, and more
- **Unified access**: One API key for 100+ models across all major providers
- **OpenAI compatible**: Drop-in replacement, zero code changes needed
- **No monthly fees**: Pay per token, no subscriptions

## Quickstart

### 1. Get your OfoxAI API Key

Sign up at [ofox.ai](https://ofox.ai) and get your API key from the dashboard.

### 2. Make your first call

OfoxAI is fully OpenAI-compatible, so you can use the OpenAI SDK:

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_OFOXAI_API_KEY",
    base_url="https://api.ofox.ai/v1"
)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",  # Groq-hosted model
    messages=[{"role": "user", "content": "Hello! Tell me about Groq's inference speed."}]
)

print(response.choices[0].message.content)
```

### 3. Switch between models instantly

Access any Groq-hosted model—or any other provider—by simply changing the model name:

```python
# Llama 3.3 70B on Groq
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Gemma 2 9B on Groq
response = client.chat.completions.create(
    model="gemma2-9b-it",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Switch to GPT-4o with the same API key
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Available Groq Models on OfoxAI

| Model | Context Window |
|-------|---------------|
| llama-3.3-70b-versatile | 128K |
| llama-3.1-8b-instant | 128K |
| gemma2-9b-it | 8K |
| mixtral-8x7b-32768 | 32K |

View the full model list at [ofox.ai/models](https://ofox.ai/models).

## Using with cURL

```bash
curl https://api.ofox.ai/v1/chat/completions \
  -H "Authorization: Bearer YOUR_OFOXAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3.3-70b-versatile",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Additional Resources

- [OfoxAI Documentation](https://ofox.ai/docs)
- [OfoxAI Dashboard](https://ofox.ai)
- [Available Models](https://ofox.ai/models)
