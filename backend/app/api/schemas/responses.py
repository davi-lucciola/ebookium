from app.api.schemas.base import BaseSchema


class MessageResponse(BaseSchema):
    message: str


class DetailResponse[T](BaseSchema):
    detail: T


class ApiResponse[T](MessageResponse):
    data: T | None = None
