FROM node:22-slim AS frontend-builder
RUN corepack enable && corepack prepare pnpm@10.28.2 --activate
WORKDIR /app/frontend

COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY frontend/ ./
RUN pnpm build


FROM node:22-slim AS frontend-dev
RUN corepack enable && corepack prepare pnpm@10.28.2 --activate
WORKDIR /app/frontend

COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

EXPOSE 5173
CMD ["pnpm", "dev", "--host", "0.0.0.0", "--port", "5173"]


FROM python:3.13-slim AS backend-dev
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app/backend

COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --frozen

COPY backend/alembic.ini ./alembic.ini
COPY backend/migrations ./migrations
COPY backend/app ./app
COPY --chmod=755 entrypoint.sh /entrypoint.sh

ENV PATH="/app/backend/.venv/bin:$PATH"
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]


FROM python:3.13-slim AS runtime
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app/backend

COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --frozen --no-dev

COPY backend/alembic.ini ./alembic.ini
COPY backend/migrations ./migrations
COPY backend/app ./app
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist
COPY --chmod=755 entrypoint.sh /entrypoint.sh

ENV PATH="/app/backend/.venv/bin:$PATH"
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
