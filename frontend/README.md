# Ebookium Frontend

React + TypeScript + Vite frontend for the Ebookium full-stack template.

## Stack

- **React 19** with **TypeScript**
- **Vite** for dev server and production builds
- **TanStack Router** — file-based routes in `src/app/`
- **shadcn/ui** + **Tailwind CSS v4** for UI components
- **Biome** for linting and formatting
- **Vitest** + **Testing Library** for unit tests

## Scripts

```bash
pnpm dev          # Start dev server (http://localhost:5173)
pnpm build        # Type-check and build for production
pnpm preview      # Preview production build
pnpm lint         # Run Biome checks
pnpm lint:fix     # Auto-fix lint issues
pnpm format       # Format code with Biome
pnpm test         # Run unit tests
pnpm test:watch   # Run tests in watch mode
```

## Project structure

```
src/
  app/              # TanStack Router file-based routes
    __root.tsx      # Root layout
    index.tsx       # Home page (/)
  components/ui/    # shadcn/ui components
  lib/              # Shared utilities
  test/             # Test setup
  routeTree.gen.ts  # Auto-generated route tree (do not edit)
```

## Development

The dev server proxies `/api` requests to the backend (default: `http://localhost:8000`).

```bash
pnpm install
pnpm dev
```

## Testing

```bash
pnpm test
```
