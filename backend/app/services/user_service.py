from fastapi import HTTPException
from sqlmodel import Session, select

from models.local_user_data import LocalUserData
from tables.user import User
from services.auth.hash_service import HashService
from enums.tenant import Tenant


class UserService:

    def __init__(self, session: Session, hash_service: HashService):
        self.session = session
        self.hash_service = hash_service

    def save_user(self, user: User) -> None:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

    def hash_user_password(self, user_data: LocalUserData) -> LocalUserData:
        user_password = self.hash_service.hash_password(user_data.password)
        return LocalUserData(full_name=user_data.full_name, email=user_data.email, password=user_password)
        
    def authenticate_local_user(self, email: str, password: str) -> User | None:
        statement = select(User).where(User.email == email)
        existing_user = self.session.exec(statement).first()

        if not existing_user:
            return None
        else: 
            if existing_user.tenant != Tenant.LOCAL:
                return None
            elif not self.hash_service.verify_password(password, existing_user.password):
                return None
            
        return existing_user

    def get_user_by_id(self, id: int):
        statement = select(User).where(User.id == id)
        existing_user = self.session.exec(statement).first()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        return existing_user
    
    def get_user_by_email(self, email: str):
        statement = select(User).where(User.email == email)
        existing_user = self.session.exec(statement).first()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        return existing_user
    
    def get_user_by_tenant_id(self, tenant_id) -> User:
        statement = select(User).where(User.tenant_id == tenant_id)
        existing_user = self.session.exec(statement).first()

        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        return existing_user
    
    def is_user_with_provided_email_in_db(self, email: str) -> bool:
        statement = select(User).where(User.email == email)
        existing_user = self.session.exec(statement).first()
        
        return bool(existing_user)
    
    def is_tenant_user_in_db(self, tenant_id: str) -> bool:
         statement = select(User).where(User.tenant_id == tenant_id)
         existing_user = self.session.exec(statement).first()

         return bool(existing_user)
