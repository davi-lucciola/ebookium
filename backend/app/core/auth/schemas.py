from pydantic import EmailStr

from app.api.schemas.base import BaseSchema


class LoginIn(BaseSchema):
    email: EmailStr
    password: str
