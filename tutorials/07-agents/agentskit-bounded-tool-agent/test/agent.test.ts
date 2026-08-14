import type { AdapterFactory, AdapterRequest, StreamChunk } from '@agentskit/core'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { createGroqIncidentRuntime, createIncidentRuntime, MAX_STEPS } from '../src/agent.js'
import { getServiceHealth, listRecentDeployments } from '../src/tools.js'

function scriptedAdapter(requests: AdapterRequest[]): AdapterFactory {
  let call = 0

  return {
    createSource(request) {
      requests.push(request)
      const current = call++

      return {
        abort() {},
        async *stream(): AsyncIterableIterator<StreamChunk> {
          if (current === 0) {
            yield {
              type: 'tool_call',
              toolCall: {
                id: 'call-health-1',
                name: 'get_service_health',
                args: JSON.stringify({ service: 'checkout' }),
              },
            }
          } else if (current === 1) {
            yield {
              type: 'tool_call',
              toolCall: {
                id: 'call-deployments-1',
                name: 'list_recent_deployments',
                args: JSON.stringify({ service: 'checkout' }),
              },
            }
          } else {
            yield {
              type: 'text',
              content: 'Evidence points to deploy-8472; confidence is high. Safest next action: roll it back.',
            }
          }
          yield { type: 'done' }
        },
      }
    },
  }
}

describe('incident tools', () => {
  it('returns structured health and deployment data', async () => {
    const context = {
      messages: [],
      call: { id: 'test', name: 'test', args: {}, status: 'running' as const },
    }

    const health = JSON.parse(String(await getServiceHealth.execute?.({ service: 'checkout' }, context)))
    const recent = JSON.parse(String(await listRecentDeployments.execute?.({ service: 'checkout' }, context)))

    expect(health).toMatchObject({ service: 'checkout', status: 'degraded', errorRatePercent: 8.7 })
    expect(recent.deployments[0]).toMatchObject({ id: 'deploy-8472', version: '2026.08.04-2' })
  })
})

describe('bounded runtime', () => {
  it('preserves tool-call IDs and feeds structured results into the next step', async () => {
    const requests: AdapterRequest[] = []
    const result = await createIncidentRuntime(scriptedAdapter(requests)).run('Investigate checkout errors.')

    expect(result.steps).toBe(3)
    expect(result.steps).toBeLessThanOrEqual(MAX_STEPS)
    expect(result.toolCalls.map(({ id, name, status }) => ({ id, name, status }))).toEqual([
      { id: 'call-health-1', name: 'get_service_health', status: 'complete' },
      { id: 'call-deployments-1', name: 'list_recent_deployments', status: 'complete' },
    ])
    expect(requests[1].messages.some(message =>
      message.toolCalls?.some(toolCall => toolCall.id === 'call-health-1'),
    )).toBe(true)
    expect(requests[1].messages.some(message =>
      message.role === 'tool' && JSON.parse(message.content).status === 'degraded',
    )).toBe(true)
    expect(requests[1].messages.some(message =>
      message.role === 'tool' && message.toolCallId === 'call-health-1',
    )).toBe(true)
    expect(result.content).toContain('deploy-8472')
  })
})

describe('Groq wire format', () => {
  afterEach(() => vi.unstubAllGlobals())

  it('sends each structured result with its originating tool-call ID', async () => {
    const bodies: Array<Record<string, unknown>> = []
    const responses = [
      {
        choices: [{
          delta: {
            tool_calls: [{
              index: 0,
              id: 'call-health-1',
              function: { name: 'get_service_health', arguments: '{"service":"checkout"}' },
            }],
          },
        }],
      },
      {
        choices: [{
          delta: {
            tool_calls: [{
              index: 0,
              id: 'call-deployments-1',
              function: { name: 'list_recent_deployments', arguments: '{"service":"checkout"}' },
            }],
          },
        }],
      },
      { choices: [{ delta: { content: 'deploy-8472 is the likely cause; roll it back.' } }] },
    ]

    vi.stubGlobal('fetch', async (_input: string | URL | Request, init?: RequestInit) => {
      bodies.push(JSON.parse(String(init?.body)) as Record<string, unknown>)
      const response = responses.shift()
      return new Response(`data: ${JSON.stringify(response)}\n\ndata: [DONE]\n\n`, {
        headers: { 'content-type': 'text/event-stream' },
      })
    })

    const result = await createGroqIncidentRuntime('test-key').run('Investigate checkout errors.')
    const secondMessages = bodies[1].messages as Array<Record<string, unknown>>
    const thirdMessages = bodies[2].messages as Array<Record<string, unknown>>

    expect(secondMessages).toContainEqual(expect.objectContaining({
      role: 'tool',
      tool_call_id: 'call-health-1',
    }))
    expect(thirdMessages).toContainEqual(expect.objectContaining({
      role: 'tool',
      tool_call_id: 'call-deployments-1',
    }))
    expect(result.toolCalls).toHaveLength(2)
  })
})
