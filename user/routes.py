from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from starlette import status

import crud
from config.db import Session, get_session
from core import responses
from core.deps import get_admin_user, get_current_user
from models import User
from user import schema

router = APIRouter()


@router.get(
    "/",
    responses=responses.UNAUTHORIZED | responses.PERMISSION_DENIED,
    response_model=Page[schema.ListUserSchema],
)
def list_users(
    session: Session = Depends(get_session), admin: User = Depends(get_admin_user)
):
    """Getting all users"""

    return paginate(crud.user.list(session))


@router.get(
    "/{id}", responses=responses.UNAUTHORIZED, response_model=schema.RetrieveUserSchema
)
def retrieve_user(
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """Getting user by id"""

    return crud.user.get(session, id)


@router.patch(
    "/{id}",
    responses=responses.UNAUTHORIZED,
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_user(
    data: schema.UpdateUserSchema,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """Update user by id"""

    crud.user.update(session, user, data.dict())


@router.delete(
    "/{id}", responses=responses.UNAUTHORIZED, status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(
    id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Delete user by id"""

    user = crud.user.get(session, id)
    crud.user.delete(session, user)
