import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import { HomePage } from '@/components/home-page'

describe('HomePage', () => {
  it('renders the hero title and stack sections', () => {
    render(<HomePage />)

    expect(screen.getByRole('heading', { level: 1, name: 'Ebookium' })).toBeInTheDocument()
    expect(screen.getByRole('heading', { level: 2, name: "What's included" })).toBeInTheDocument()
    expect(screen.getByRole('heading', { level: 2, name: 'Quick start' })).toBeInTheDocument()
    expect(screen.getByText('TanStack Router')).toBeInTheDocument()
    expect(screen.getByText('FastAPI')).toBeInTheDocument()
  })

  it('renders the API documentation link', () => {
    render(<HomePage />)

    const apiLink = screen.getByRole('link', { name: 'API Documentation' })
    expect(apiLink).toHaveAttribute('href', '/api/docs')
    expect(apiLink).toHaveAttribute('target', '_blank')
  })
})
