from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from containers import user_role_handler, authorizer
from enums.role import RoleEnum
from interfaces.user_data_dto import UserDataDTO
from interfaces.user_role_dto import UserRoleDTO

router = APIRouter()

@router.get('/role')
def get_user_role(userId: int, user_role_handler: user_role_handler) -> RoleEnum:
    return user_role_handler.get_user_role(userId).role
       
@router.post('/role/default')
def insert_user_default_role(body: UserDataDTO, user_role_handler: user_role_handler) -> None:
      user_role_handler.insert_or_update_user_role(body.user_id, RoleEnum.USER)

@router.post('/role/authorize')
def autorize_user_role(body: UserRoleDTO, authorizer: authorizer) -> bool:
    return authorizer.autorize_user(body.user_id, body.role)     


      
