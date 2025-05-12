from pydantic import BaseModel

from enums.role import RoleEnum


class UserRoleDTO(BaseModel):
    role: RoleEnum
    user_id: int