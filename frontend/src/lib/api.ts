import createClient from 'openapi-fetch'

import type { paths } from '@/lib/api/schema'

export const client = createClient<paths>({
  baseUrl: '/',
  credentials: 'include',
})
