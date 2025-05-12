from enums.role import RoleEnum
from services.role_handler import RoleHandler
from services.user_role_handler import UserRoleHandler


class RoleAuthorizer:

    def __init__(self, user_role_handler: UserRoleHandler, role_handler: RoleHandler) -> None:
        self.user_role_table = user_role_handler
        self.role_table = role_handler

    def autorize_user(self, user_id:int, role_enum: RoleEnum) -> bool:
        user_record = self.user_role_table.get_user_record_by_id(user_id)
        role = self.role_table.get_role_by_id(user_record.role_id)
        
        return role.role == role_enum
