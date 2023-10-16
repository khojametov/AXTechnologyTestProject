from fastapi import APIRouter, Depends
from starlette import status

from auth import schema, services
from config.db import Session, get_session
from core import responses
from core.exceptions import BadRequestError

router = APIRouter()


@router.post(
    "/login",
    responses=responses.UNAUTHORIZED | responses.PERMISSION_DENIED,
)
def login(form_data: schema.UserLoginSchema, session: Session = Depends(get_session)):
    """Login to as a user"""
    access_token = services.get_access_token_for_user(
        session, form_data.email, form_data.password
    )

    return {"access": access_token}


@router.post(
    "/register",
    responses=responses.BAD_REQUEST,
    status_code=status.HTTP_201_CREATED,
)
def register(
    form_data: schema.UserRegisterSchema, session: Session = Depends(get_session)
):
    """Register user"""
    try:
        services.register_user(session, form_data)
    except Exception:
        raise BadRequestError("User with this email already registered")

    return form_data
