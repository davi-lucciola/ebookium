from typing import Annotated

from fastapi import Depends

from app.core.auth.services import AuthService as AuthServiceImpl
from app.core.users.dependencies import UserService


def get_auth_service(user_service: UserService) -> AuthServiceImpl:
    return AuthServiceImpl(user_service=user_service)


AuthService = Annotated[AuthServiceImpl, Depends(get_auth_service)]
