from fastapi import APIRouter, Depends, Request, Response, status

from app.api.docs.responses import CONFLICT, UNAUTHORIZED, VALIDATION
from app.api.guards import auth_guard
from app.api.schemas import ApiResponse
from app.core.auth.dependencies import AuthService
from app.core.auth.schemas import LoginIn
from app.core.exceptions import AuthenticationError
from app.core.users.dependencies import UserService
from app.core.users.models import User
from app.core.users.schemas import UserIn, UserOut
from app.infra.auth import cookies

router = APIRouter(prefix='/api/auth', tags=['Auth'])


@router.post(
    '/user',
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[UserOut],
    summary='Sign up a new user',
    description='Public endpoint. The email must not already be registered.',
    responses={**CONFLICT, **VALIDATION},
)
async def create_user(user: UserIn, user_service: UserService):
    created_user = await user_service.create(user)
    return ApiResponse(message='User created successfully.', data=created_user)


@router.post(
    '/session',
    status_code=status.HTTP_200_OK,
    response_model=UserOut,
    summary='Log in and set session cookies',
    description=(
        'Exchanges email and password for httpOnly session cookies. '
        'Tokens are never returned in the JSON body.'
    ),
    responses={**UNAUTHORIZED, **VALIDATION},
)
async def create_session(
    body: LoginIn,
    response: Response,
    auth_service: AuthService,
):
    user = await auth_service.login(body.email, body.password)
    access_token, refresh_token = auth_service.issue_session(user)
    cookies.set_session(response, access_token, refresh_token)
    return user


@router.post(
    '/session/refresh',
    status_code=status.HTTP_200_OK,
    response_model=UserOut,
    summary='Rotate session cookies',
    description=(
        'Reads the refresh cookie, issues a new cookie pair, and returns the user.'
    ),
    responses={**UNAUTHORIZED},
)
async def refresh_session(
    request: Request,
    response: Response,
    auth_service: AuthService,
):
    raw_refresh = cookies.get_refresh(request)

    if raw_refresh is None:
        raise AuthenticationError('Authentication required.')

    user, access_token, refresh_token = await auth_service.rotate_session(raw_refresh)
    cookies.set_session(response, access_token, refresh_token)
    return user


@router.delete(
    '/session',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Log out and clear session cookies',
    description=(
        'Clears both session cookies. Works even if the access JWT is already expired.'
    ),
)
async def delete_session(response: Response):
    cookies.clear_session(response)


@router.get(
    '/user/me',
    status_code=status.HTTP_200_OK,
    response_model=UserOut,
    summary='Get the authenticated user',
    responses={**UNAUTHORIZED},
)
async def get_me(current_user: User = Depends(auth_guard)):
    return current_user
