from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from database import get_session
from services.role_authorizer import RoleAuthorizer
from services.role_handler import RoleHandler
from services.user_role_handler import UserRoleHandler

session = Annotated[Session, Depends(get_session)]

def get_role_handler(session: session) -> RoleHandler:
    return RoleHandler(session)

role_handler = Annotated[RoleHandler, Depends(get_role_handler)]

def get_user_role_handler(session: session, role_handler: role_handler):
    return UserRoleHandler(session, role_handler)

user_role_handler = Annotated[UserRoleHandler, Depends(get_user_role_handler)]

def get_autorizer(user_role_handler: user_role_handler, role_handler: role_handler):
    return RoleAuthorizer(user_role_handler, role_handler)

authorizer = Annotated[RoleAuthorizer, Depends(get_autorizer)]