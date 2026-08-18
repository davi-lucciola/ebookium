from datetime import datetime

from pydantic import EmailStr

from app.api.schemas.base import BaseSchema


class UserIn(BaseSchema):
    name: str
    email: EmailStr
    password: str


class UserOut(BaseSchema):
    id: int
    name: str
    email: str
    is_active: bool
    created_at: datetime
