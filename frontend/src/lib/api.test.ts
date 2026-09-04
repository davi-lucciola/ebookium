import { describe, expect, it } from 'vitest'

import { client } from '@/lib/api'

describe('api client', () => {
  it('exposes typed fetch methods', () => {
    expect(typeof client.GET).toBe('function')
    expect(typeof client.POST).toBe('function')
    expect(typeof client.DELETE).toBe('function')
  })
})
