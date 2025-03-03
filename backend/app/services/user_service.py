from fastapi import HTTPException
from sqlmodel import Session, select

from app_types.user_create_dto import UserCreateDTO
from db_models.user_model import User
from services.auth.hash_service import HashService
from app_types.auth_provider import AuthProvider


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
        
        if user.provider == AuthProvider.GOOGLE:
            new_user = User(full_name=user.full_name, email=user.email, password=None, provider=user.provider, chats=[])
        elif user.provider == AuthProvider.LOCAL:
            user_password = self.hash_service.hash_password(user.password)
            new_user = User(full_name=user.full_name, email=user.email, password=user_password, provider=user.provider, chats=[])
        else:
            raise HTTPException(status_code=500, detail="No provider.")
        
        return new_user

    def authenticate_local_user(self, email: str, password: str):
        statement = select(User).where(User.email == email)
        existing_user = self.session.exec(statement).first()

        if not existing_user:
            return False
        else: 
            if existing_user.provider != AuthProvider.LOCAL:
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
    
    def is_user_with_provided_email_in_db(self, email: str) -> bool:
        statement = select(User).where(User.email == email)
        existing_user = self.session.exec(statement).first()
        
        return bool(existing_user)
