export const services = {
  checkout: {
    status: 'degraded',
    errorRatePercent: 8.7,
    p95LatencyMs: 1840,
    startedAt: '2026-08-04T14:07:00Z',
  },
  catalog: {
    status: 'healthy',
    errorRatePercent: 0.2,
    p95LatencyMs: 190,
    startedAt: null,
  },
} as const

export const deployments = {
  checkout: [
    {
      id: 'deploy-8472',
      version: '2026.08.04-2',
      deployedAt: '2026-08-04T14:02:00Z',
      change: 'Enabled the new payment-provider retry policy',
    },
    {
      id: 'deploy-8468',
      version: '2026.08.04-1',
      deployedAt: '2026-08-04T11:30:00Z',
      change: 'Updated checkout page copy',
    },
  ],
  catalog: [
    {
      id: 'deploy-8460',
      version: '2026.08.03-3',
      deployedAt: '2026-08-03T19:10:00Z',
      change: 'Refreshed search index mappings',
    },
  ],
} as const

export type ServiceName = keyof typeof services

export function isServiceName(value: string): value is ServiceName {
  return value in services
}
