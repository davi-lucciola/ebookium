# ebookium

FastAPI backend + React (Vite/TypeScript) frontend, served together via FastAPI's `app.frontend()`.

The repo is a Bun + uv workspace. Install once at the root, then use the root scripts.

```bash
bun install
uv sync
```

## Development

```bash
bun run dev:api   # http://localhost:8000
bun run dev       # http://localhost:5173, proxies /api to http://localhost:8000
# or both:
bun run dev:all
```

## Scripts

Frontend scripts are mirrored at the root. Backend [taskipy](backend/pyproject.toml) tasks are proxied as `<task>:api`.

| Script | What it runs |
|---|---|
| `bun run dev` | Vite dev server |
| `bun run dev:api` | FastAPI (`task dev`) |
| `bun run dev:all` | backend + frontend together |
| `bun run build` / `preview` | frontend production build / preview |
| `bun run lint` / `lint:fix` / `format` | Biome |
| `bun run lint:api` / `format:api` | Ruff |
| `bun run test` / `test:watch` | frontend Vitest |
| `bun run test:api` / `test_unit:api` / `test_integration:api` | pytest |
| `bun run migrate:api` / `migrate_create:api` | Alembic |
| `bun run openapi:json` | fetch `/openapi.json` from the running API into `frontend/openapi.json` |
| `bun run openapi:client` | generate TypeScript types from the spec |

## OpenAPI client

[`frontend/openapi.json`](frontend/openapi.json) is the source of truth. The frontend uses [openapi-fetch](https://openapi-ts.dev/openapi-fetch/) with types from [openapi-typescript](https://openapi-ts.dev/).

```bash
bun run dev:api          # API must be running
bun run openapi:json     # fetch http://localhost:8000/openapi.json
bun run openapi:client   # generate src/lib/api/schema.d.ts
```

Import the typed client from `@/lib/api` (cookies are sent with `credentials: 'include'`).

## Production build

```bash
bun run build
uv run --directory backend fastapi run app/main.py
```

FastAPI then serves the built React app directly from `http://localhost:8000/`, with `/api/*` for the backend.

## Docker

### Production

```bash
docker build -t ebookium .
docker run -p 8000:8000 ebookium
```

### Development (hot reload)

```bash
docker compose up --build
```

- Frontend (HMR): http://localhost:5173
- Backend API docs: http://localhost:8000/api/docs
- Postgres data: `./data/postgres/`

Rebuild images when dependencies change (`pyproject.toml`, `uv.lock`, `package.json`, `bun.lock`). Source edits reload automatically.
