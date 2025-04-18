from fastapi import HTTPException
from sqlmodel import Session, select

from models.user_create_dto import UserCreateDTO
from db_models.user_model import User
from services.auth.hash_service import HashService
from models.tenant import Tenant


class UserService:

    def __init__(self, session: Session, hash_service: HashService):
        self.session = session
        self.hash_service = hash_service

    def save_user(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

    def create_user(self, user: UserCreateDTO) -> User:
        existing_user = self.is_user_with_provided_email_in_db(user.email)
        if existing_user:
            raise HTTPException(status_code=409, detail="Email already registered")
        
        if user.tenant == Tenant.GOOGLE or user.tenant == Tenant.MICROSOFT:
            if not user.tenant_id:
                raise HTTPException(status_code=500, detail="No user tenant_id")
            new_user = User(tenant_id=user.tenant_id, full_name=user.full_name, email=user.email, password=None, tenant=user.tenant, chats=[])
        elif user.tenant == Tenant.LOCAL:
            user_password = self.hash_service.hash_password(user.password)
            new_user = User(full_name=user.full_name, email=user.email, password=user_password, tenant=user.tenant, chats=[])
        
        return new_user

    def authenticate_local_user(self, email: str, password: str):
        statement = select(User).where(User.email == email)
        existing_user = self.session.exec(statement).first()

        if not existing_user:
            return False
        else: 
            if existing_user.tenant != Tenant.LOCAL:
                return False
            elif not self.hash_service.verify_password(password, existing_user.password):
                return False
            
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
    
    def get_user_by_tenant_id(self, tenant_id):
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
