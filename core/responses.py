from pydantic import BaseModel

from common.types import APIResponseType


class ExceptionMessageSchema(BaseModel):
    detail: str


class InvalidTokenSchema(BaseModel):
    detail: str = "Token is invalid or expired"


class EmailNotVerifiedSchema(BaseModel):
    detail: str = "Token is invalid or expired"


UNAUTHORIZED: APIResponseType = {
    401: {"model": ExceptionMessageSchema, "description": "Unauthorized Error"}
}

PERMISSION_DENIED: APIResponseType = {
    403: {"model": ExceptionMessageSchema, "description": "Permission denied"}
}

EMAIL_NOT_VERIFIED: APIResponseType = {
    403: {"model": EmailNotVerifiedSchema, "description": "Email not verified"}
}

INVALID_TOKEN: APIResponseType = {
    400: {"model": InvalidTokenSchema, "description": "Invalid token"}
}
BAD_REQUEST: APIResponseType = {
    400: {"model": ExceptionMessageSchema, "description": "Bad Request"}
}

NOT_FOUND: APIResponseType = {
    404: {"model": ExceptionMessageSchema, "description": "Not found"},
}

INVALID_ADDRESS: APIResponseType = {
    422: {"model": ExceptionMessageSchema, "description": "Address is invalid"}
}

CRUD_RESPONSES: APIResponseType = UNAUTHORIZED | PERMISSION_DENIED | NOT_FOUND
