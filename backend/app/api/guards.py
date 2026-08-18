from fastapi import Depends, HTTPException, Request, status
from fastapi.security import APIKeyCookie

from app.core.auth.dependencies import AuthService
from app.core.users.models import User
from app.infra.auth.cookies import ACCESS_COOKIE_NAME

access_cookie_scheme = APIKeyCookie(name=ACCESS_COOKIE_NAME, auto_error=False)


class AuthGuard:
    async def __call__(
        self,
        request: Request,
        auth_service: AuthService,
        _cookie: str | None = Depends(access_cookie_scheme),
    ) -> User:
        token = request.cookies.get(ACCESS_COOKIE_NAME)
        if token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Authentication required.',
            )

        return await auth_service.authenticate(token)


auth_guard = AuthGuard()
