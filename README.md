# ebookium

FastAPI backend + React (Vite/TypeScript) frontend, served together via FastAPI's `app.frontend()`.

## Backend

```bash
cd backend
uv sync
uv run fastapi dev app/main.py   # http://localhost:8000
```

Run tests:

```bash
cd backend
uv run pytest
```

## Frontend

```bash
cd frontend
pnpm install
pnpm dev   # http://localhost:5173, proxies /api to http://localhost:8000
pnpm test  # run frontend unit tests
```

## Production build

```bash
cd frontend && pnpm build
cd ../backend && uv run fastapi run app/main.py
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

Rebuild images when dependencies change (`pyproject.toml`, `uv.lock`, `package.json`, `pnpm-lock.yaml`). Source edits reload automatically.
