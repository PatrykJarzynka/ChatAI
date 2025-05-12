
#RoleHandler

#add role
#delete role
#update role

from fastapi import HTTPException
from sqlmodel import Session, select

from enums.role import RoleEnum
from tables.role import Role


class RoleHandler:

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_role_by_id(self, role_id: int) -> Role:
        statement = select(Role).where(Role.id == role_id)
        role = self.session.exec(statement).first()
    
        if not role:
                 raise HTTPException(status_code=404, detail="Role with provided id doesn't exist")
            
        return role
        
    def get_role_by_role_enum(self, role_enum: RoleEnum) -> Role:
            statement = select(Role).where(Role.role == role_enum)
            role = self.session.exec(statement).first()

            if not role:
                 raise HTTPException(status_code=404, detail="Role with provided name doesn't exist")
            
            return role

        