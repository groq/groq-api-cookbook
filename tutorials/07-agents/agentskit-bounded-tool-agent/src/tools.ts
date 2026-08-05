import { defineTool, type ToolDefinition } from '@agentskit/core'
import { deployments, isServiceName, services } from './incident-data.js'

function requireService(value: string) {
  if (!isServiceName(value)) {
    throw new Error(`Unknown service "${value}". Available services: ${Object.keys(services).join(', ')}`)
  }
  return value
}

export const getServiceHealth = defineTool({
  name: 'get_service_health',
  description: 'Return current health signals for one service in the synthetic deployment environment.',
  schema: {
    type: 'object',
    properties: {
      service: {
        type: 'string',
        enum: ['checkout', 'catalog'],
        description: 'Service to inspect.',
      },
    },
    required: ['service'],
    additionalProperties: false,
  } as const,
  execute({ service }) {
    const name = requireService(service)
    return JSON.stringify({ service: name, ...services[name] })
  },
})

export const listRecentDeployments = defineTool({
  name: 'list_recent_deployments',
  description: 'List the most recent deployments for one service in newest-first order.',
  schema: {
    type: 'object',
    properties: {
      service: {
        type: 'string',
        enum: ['checkout', 'catalog'],
        description: 'Service whose deployment history should be inspected.',
      },
    },
    required: ['service'],
    additionalProperties: false,
  } as const,
  execute({ service }) {
    const name = requireService(service)
    return JSON.stringify({ service: name, deployments: deployments[name] })
  },
})

export const incidentTools = [getServiceHealth, listRecentDeployments] as unknown as ToolDefinition[]
