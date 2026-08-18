from sqlalchemy.orm import Mapped, mapped_column

from app.infra.db import BaseEntity, CreatedAt, KeyStr, Long, UpdatedAt


class User(BaseEntity):
    __tablename__ = 'users'

    id: Mapped[Long] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    email: Mapped[KeyStr]
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)

    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    def __init__(
        self,
        name: str,
        email: str,
        password: str,
        is_active: bool = True,
    ):
        self.name = name
        self.email = email
        self.password = password
        self.is_active = is_active
