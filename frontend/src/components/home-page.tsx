import { BookOpen, Database, Layers, Server } from 'lucide-react'

import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Separator } from '@/components/ui/separator'

const stackSections = [
  {
    icon: Layers,
    title: 'Frontend',
    description: 'Modern React SPA with type-safe routing and accessible UI primitives.',
    tags: ['React 19', 'Vite', 'TypeScript', 'TanStack Router', 'shadcn/ui'],
  },
  {
    icon: Server,
    title: 'Backend',
    description: 'Async API with structured modules, auth, and OpenAPI documentation.',
    tags: ['FastAPI', 'SQLAlchemy', 'Alembic', 'JWT Auth'],
  },
  {
    icon: Database,
    title: 'Database',
    description: 'Relational storage with migrations and typed repository layer.',
    tags: ['PostgreSQL 16', 'Alembic', 'psycopg'],
  },
  {
    icon: BookOpen,
    title: 'DevOps',
    description: 'Local development with hot reload and a single production image.',
    tags: ['Docker Compose', 'Multi-stage build', 'FastAPI static serving'],
  },
] as const

export function HomePage() {
  return (
    <div className="mx-auto flex min-h-svh max-w-5xl flex-col px-6 py-12 md:px-10 md:py-16">
      <header className="space-y-6 text-center">
        <Badge variant="secondary" className="mx-auto">
          Full-stack template
        </Badge>
        <div className="space-y-4">
          <h1 className="text-4xl font-semibold tracking-tight md:text-6xl">Ebookium</h1>
          <p className="text-muted-foreground mx-auto max-w-2xl text-lg leading-relaxed">
            A production-ready full-stack starter with a React frontend, FastAPI backend, PostgreSQL
            database, and Docker-based workflows — ready to extend for your next project.
          </p>
        </div>
        <div className="flex flex-wrap items-center justify-center gap-3">
          <Button asChild>
            <a href="/api/docs" target="_blank" rel="noreferrer">
              API Documentation
            </a>
          </Button>
          <Button variant="outline" asChild>
            <a href="#stack">Explore the stack</a>
          </Button>
        </div>
      </header>

      <Separator className="my-12" />

      <section id="stack" className="space-y-6">
        <div className="space-y-2 text-center">
          <h2 className="text-2xl font-semibold tracking-tight">What&apos;s included</h2>
          <p className="text-muted-foreground">
            Opinionated defaults across the entire stack, from UI to deployment.
          </p>
        </div>
        <div className="grid gap-6 md:grid-cols-2">
          {stackSections.map((section) => (
            <Card key={section.title} className="h-full">
              <CardHeader>
                <div className="mb-2 flex size-10 items-center justify-center rounded-lg border bg-muted">
                  <section.icon className="size-5" aria-hidden="true" />
                </div>
                <CardTitle>{section.title}</CardTitle>
                <CardDescription>{section.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {section.tags.map((tag) => (
                    <Badge key={tag} variant="outline">
                      {tag}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      <Separator className="my-12" />

      <section className="space-y-6">
        <div className="space-y-2 text-center">
          <h2 className="text-2xl font-semibold tracking-tight">Quick start</h2>
          <p className="text-muted-foreground">
            Run the backend and frontend locally, or use Docker Compose for the full stack.
          </p>
        </div>
        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>Backend</CardTitle>
              <CardDescription>FastAPI with uv and pytest</CardDescription>
            </CardHeader>
            <CardContent>
              <pre className="bg-muted overflow-x-auto rounded-lg p-4 font-mono text-sm leading-relaxed">
                {`cd backend
uv sync
uv run fastapi dev app/main.py
uv run pytest`}
              </pre>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Frontend</CardTitle>
              <CardDescription>React with Vite, Biome, and Vitest</CardDescription>
            </CardHeader>
            <CardContent>
              <pre className="bg-muted overflow-x-auto rounded-lg p-4 font-mono text-sm leading-relaxed">
                {`cd frontend
pnpm install
pnpm dev
pnpm test`}
              </pre>
            </CardContent>
          </Card>
        </div>
      </section>

      <footer className="text-muted-foreground mt-auto pt-12 text-center text-sm">
        Built with TanStack Router, shadcn/ui, Tailwind CSS, Biome, and Vitest.
      </footer>
    </div>
  )
}
