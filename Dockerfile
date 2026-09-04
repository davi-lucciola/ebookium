FROM oven/bun:1 AS frontend-builder
WORKDIR /app

COPY package.json bun.lock ./
COPY frontend/package.json ./frontend/
RUN bun install --frozen-lockfile

COPY frontend ./frontend
RUN bun run --filter frontend build


FROM oven/bun:1 AS frontend-dev
WORKDIR /app

COPY package.json bun.lock ./
COPY frontend/package.json ./frontend/
RUN bun install --frozen-lockfile

EXPOSE 5173
CMD ["bun", "run", "--filter", "frontend", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]


FROM python:3.13-slim AS backend-dev
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY backend/pyproject.toml ./backend/
RUN uv sync --frozen --package ebookium

COPY backend/alembic.ini ./backend/alembic.ini
COPY backend/migrations ./backend/migrations
COPY backend/app ./backend/app
COPY --chmod=755 entrypoint.sh /entrypoint.sh

WORKDIR /app/backend
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]


FROM python:3.13-slim AS runtime
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY backend/pyproject.toml ./backend/
RUN uv sync --frozen --package ebookium --no-dev

COPY backend/alembic.ini ./backend/alembic.ini
COPY backend/migrations ./backend/migrations
COPY backend/app ./backend/app
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist
COPY --chmod=755 entrypoint.sh /entrypoint.sh

WORKDIR /app/backend
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
