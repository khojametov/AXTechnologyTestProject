from datetime import datetime, timedelta

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlmodel import select

from auth import schema
from config.db import Session
from config.settings import settings
from core.token import Token
from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_access_token_for_user(session: Session, email: str, password: str) -> str:
    user_query = select(User).where(User.email == email)
    user = session.exec(user_query).first()

    if not user or not user.check_password(password):
        raise HTTPException(status_code=401, detail="Unauthorized")

    now = datetime.utcnow()
    token = Token.generate_token_for_user(user, instantiation_time=now)
    return token


def register_user(session: Session, data: schema.UserRegisterSchema) -> User:
    if session.exec(select(1).where(User.email == data.email)).first():
        raise Exception("Customer with this email is already registered")

    user = User(email=data.email)
    user.set_password(data.password)

    session.add(user)
    session.commit()

    return user


async def create_access_token(data: dict):
    to_encode = data.copy()
    expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire_datetime = datetime.utcnow() + expire
    to_encode["exp"] = expire_datetime
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_admin_user(session: Session, *, email: str, password: str):
    if len(password) < 6:
        raise Exception("The password size must be more than 6")
    if session.exec(select(1).where(User.email == email)).first():
        raise Exception("User with this email already exists")

    user = User(email=email, is_admin=True)
    user.set_password(password)

    session.add(user)
    session.commit()

    return user
