import datetime as dt
from typing import Annotated

from sqlalchemy import BigInteger, String, func
from sqlalchemy import DateTime as DT
from sqlalchemy.orm import DeclarativeBase, mapped_column


class BaseEntity(DeclarativeBase):
    pass


Long = Annotated[int, mapped_column(BigInteger())]
CreatedAt = Annotated[
    dt.datetime, mapped_column(DT(timezone=True), server_default=func.now())
]
UpdatedAt = Annotated[
    dt.datetime,
    mapped_column(DT(timezone=True), server_default=func.now(), onupdate=func.now()),
]
KeyStr = Annotated[str, mapped_column(String(255), unique=True, index=True)]
