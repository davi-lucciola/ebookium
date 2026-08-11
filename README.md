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
```

## Production build

```bash
cd frontend && pnpm build
cd ../backend && uv run fastapi run app/main.py
```

FastAPI then serves the built React app directly from `http://localhost:8000/`, with `/api/*` for the backend.

## Docker

```bash
docker build -t ebookium .
docker run -p 8000:8000 ebookium
```
