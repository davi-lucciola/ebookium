"""Reusable error responses for controller `responses=`.

Routers are auto-discovered (`app.api.include_routes`), so there is no central
`include_router` to plug this into — each controller imports and composes what
its route can actually emit:

    responses={**UNAUTHORIZED, **NOT_FOUND, **VALIDATION}

There are only two error shapes in the API:

- `MessageResponse` (`{message}`) — 400, 401, 404, 409 and 500;
- `DetailResponse` (`{detail: [...]}`) — 422, exclusive to invalid schema.

Declaring 422 explicitly also replaces the `HTTPValidationError` FastAPI would
generate on its own, which does not match what this app returns.
"""

from typing import Any

from app.api.schemas import DetailResponse, MessageResponse

Responses = dict[int | str, dict[str, Any]]

BAD_REQUEST: Responses = {
    400: {
        'model': MessageResponse,
        'description': 'Business rule violation',
    },
}

UNAUTHORIZED: Responses = {
    401: {
        'model': MessageResponse,
        'description': 'Missing, expired or invalid access token',
    },
}

NOT_FOUND: Responses = {
    404: {
        'model': MessageResponse,
        'description': 'Resource not found',
    },
}

CONFLICT: Responses = {
    409: {
        'model': MessageResponse,
        'description': 'Resource already exists',
    },
}

VALIDATION: Responses = {
    422: {
        'model': DetailResponse[list[dict[str, Any]]],
        'description': 'Request does not match the expected schema',
    },
}

SERVER_ERROR: Responses = {
    500: {
        'model': MessageResponse,
        'description': 'Unexpected error',
    },
}
