from fastapi import Depends
from sqlmodel import Session

from config.db import get_session
from core.exceptions import PermissionDeniedError, UnauthorizedError
from core.security import JWTBearer
from core.token import Token
from models import User


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(JWTBearer(scheme_name="Bearer")),
) -> User:
    try:
        user = Token.get_user_from_string(token, session)
    except Exception:
        raise UnauthorizedError

    return user


def get_admin_user(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise PermissionDeniedError

    return user
