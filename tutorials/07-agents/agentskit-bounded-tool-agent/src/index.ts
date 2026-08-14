import { createGroqIncidentRuntime, DEFAULT_MODEL } from './agent.js'

const apiKey = process.env.GROQ_API_KEY

if (!apiKey) {
  throw new Error('GROQ_API_KEY is required. Copy .env.example to .env, add your key, and run npm start.')
}

const model = process.env.GROQ_MODEL ?? DEFAULT_MODEL
const task = process.argv.slice(2).join(' ') || [
  'Checkout errors rose at 14:07 UTC.',
  'Investigate the checkout service, identify the most likely cause,',
  'state your confidence, and recommend the safest next action.',
].join(' ')

const runtime = createGroqIncidentRuntime(apiKey, model)
const result = await runtime.run(task)

console.log(result.content)
console.log('\nRun summary')
console.log(JSON.stringify({
  model,
  steps: result.steps,
  toolCalls: result.toolCalls.map(({ id, name, status }) => ({ id, name, status })),
  durationMs: result.durationMs,
}, null, 2))
