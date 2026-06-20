# Use Groq with AFK coding-agent sessions

[AFK](https://afk.mooglest.com) is a browser-based command center for persistent coding-agent sessions. AFK supports Groq as a built-in LLM connection, so you can bring your Groq API key, choose a Groq model per session, and supervise agent work from the web UI.

Use this integration when you want Groq-hosted models in an AFK workflow for code changes, reviews, debugging, documentation updates, or longer-running agent tasks.

## Prerequisites

- A Groq API key from [console.groq.com](https://console.groq.com/)
- An AFK account at [afk.mooglest.com](https://afk.mooglest.com)
- An AFK daemon connected to the machine that has access to your project files

## Step 1. Create or sign in to AFK

Open [afk.mooglest.com](https://afk.mooglest.com) and create an account or sign in.

AFK runs from the browser UI while a local daemon gives sessions access to your development machine and project directories.

## Step 2. Install and connect an AFK daemon

In AFK:

1. Open **Account → API Keys**.
2. Create a daemon token.
3. Follow the install command shown in the app.
4. Confirm the daemon appears as connected in the browser.

## Step 3. Add Groq as an LLM connection

In AFK:

1. Open **Account → LLM**.
2. Click **Add connection**.
3. Choose **Groq**.
4. Paste your Groq API key.
5. Leave **Base URL** blank unless you are routing through a custom proxy or gateway.
6. Save or test the connection.

AFK uses Groq's default OpenAI-compatible endpoint automatically for the built-in Groq provider.

## Step 4. Start a session with a Groq model

Click **New session** in AFK, then:

1. Select the connected daemon and project directory.
2. Choose the Groq connection.
3. Select or type a Groq model name, for example:

   ```text
   llama-3.3-70b-versatile
   llama-3.1-8b-instant
   gemma2-9b-it
   ```

4. Choose a permission mode.
5. Enter the coding task and start the session.

AFK will route the session's model requests through Groq while the browser UI shows progress, tool usage, diffs, and session history.

## Optional: route through a proxy or gateway

If your team routes Groq traffic through an internal gateway, configure the Groq connection with that gateway's OpenAI-compatible Base URL.

For example:

```text
https://your-gateway.example.com/openai/v1
```

Keep the provider set to **Groq** unless your gateway requires a different OpenAI-compatible configuration.

## Troubleshooting

| Issue | Check |
|-------|-------|
| Connection test fails | Verify the Groq API key and confirm your network can reach Groq. |
| Model is missing | Manually type the Groq model name in AFK. Provider model discovery can lag behind newly released models. |
| Custom gateway errors | Confirm the Base URL includes the OpenAI-compatible `/v1` path expected by your gateway. |
| Session cannot access files | Confirm the selected AFK daemon is connected and has the project directory under an allowed root. |

## Resources

- [AFK](https://afk.mooglest.com)
- [AFK provider setup docs](https://docs.mooglest.com/providers)
- [Groq API docs](https://console.groq.com/docs/overview)
- [Groq models](https://console.groq.com/docs/models)
