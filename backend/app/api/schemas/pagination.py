import math
from typing import Self

from pydantic import ConfigDict, Field

from app.api.schemas.base import BaseSchema


class PaginationFilter(BaseSchema):
    page: int = Field(ge=1, default=1)
    page_size: int = Field(ge=1, default=10)


class PaginationResponse[T](BaseSchema):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    data: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int

    @classmethod
    def build(cls, data: list[T], total: int, filter: PaginationFilter) -> Self:
        return cls(
            data=data,
            total=total,
            page=filter.page,
            page_size=filter.page_size,
            total_pages=math.ceil(total / filter.page_size),
        )
