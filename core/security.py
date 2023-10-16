from typing import Optional

from fastapi import Request
from fastapi.security import HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param

from core.exceptions import UnauthorizedError


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request) -> str:  # type: ignore[override]
        authorization: Optional[str] = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)

        if not (authorization and scheme and credentials) or scheme.lower() != "bearer":
            raise UnauthorizedError("Invalid credentials")
        return credentials
