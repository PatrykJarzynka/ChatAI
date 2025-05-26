from fastapi import HTTPException
from sqlmodel import Session, select

from enums.role import RoleEnum
from services.role_handler import RoleHandler
from tables.role import Role
from tables.user_role import UserRole

class UserRoleHandler:

    def __init__(self, session: Session, role_handler: RoleHandler) -> None:
        self.session = session
        self.role_handler = role_handler

    def get_user_record_by_id(self, user_id: int) -> UserRole:
        statement = select(UserRole).where(UserRole.user_id == user_id)
        user_role_record = self.session.exec(statement).first()
        
        if not user_role_record:
            raise HTTPException(status_code=404, detail="Record with provided user_id doesn't exist")
        
        return user_role_record

    def get_user_role(self, user_id: int) -> Role:
        user_record = self.get_user_record_by_id(user_id)
        return self.role_handler.get_role_by_id(user_record.role_id)

    def insert_or_update_user_role(self, user_id: int, role_enum: RoleEnum) -> None:
        role = self.role_handler.get_role_by_role_enum(role_enum)
        user_role_record = UserRole(role_id=role.id, user_id=user_id)
        self.session.merge(user_role_record)
        self.session.commit()

        

