# Ebookium Frontend

React + TypeScript + Vite frontend for the Ebookium full-stack template.

Install and run scripts from the **repo root** (`bun install`, `bun run dev`, …).

## Stack

- **React 19** with **TypeScript**
- **Bun** workspaces for install and scripts
- **Vite** for dev server and production builds
- **TanStack Router** — file-based routes in `src/app/`
- **shadcn/ui** + **Tailwind CSS v4** for UI components
- **Biome** for linting and formatting
- **Vitest** + **Testing Library** for unit tests
- **[openapi-fetch](https://openapi-ts.dev/openapi-fetch/)** HTTP client (types from `openapi.json`)

## Scripts

From the repo root:

```bash
bun run dev              # Start dev server (http://localhost:5173)
bun run build            # Type-check and build for production
bun run preview          # Preview production build
bun run lint             # Run Biome checks
bun run lint:fix         # Auto-fix lint issues
bun run test             # Run unit tests
bun run test:watch       # Run tests in watch mode
bun run openapi:json     # Fetch spec from the running API (localhost:8000)
bun run openapi:client   # Generate src/lib/api/schema.d.ts
```

Inside `frontend/` the same package scripts still work (`bun run dev`, `bun run test`, …).

## Project structure

```
openapi.json        # OpenAPI spec (source of truth for the HTTP client)
src/
  app/              # TanStack Router file-based routes
    __root.tsx      # Root layout
    index.tsx       # Home page (/)
  components/ui/    # shadcn/ui components
  lib/
    api.ts          # openapi-fetch client (credentials: include)
    api/schema.d.ts # Generated types (do not edit)
  test/             # Test setup
  routeTree.gen.ts  # Auto-generated route tree (do not edit)
```

## Development

The dev server proxies `/api` requests to the backend (default: `http://localhost:8000`).

```bash
bun install   # from repo root
bun run dev
```

## Testing

```bash
bun run test
```
