from fastapi import HTTPException
from sqlmodel import Session, select

from app_types.user_create_dto import UserCreateDTO
from db_models.user_model import User
from services.auth.hash_service import HashService


class UserService:

    def __init__(self, session: Session, hash_service: HashService):
        self.session = session
        self.hash_service = hash_service

    def save_user(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

    def create_user(self, user: UserCreateDTO):
        statement = select(User).where(User.email == user.email)
        existing_user = self.session.exec(statement).first()
        if existing_user:
            raise HTTPException(status_code=409, detail="Email already registered")

        hashed_password = self.hash_service.hash_password(user.password)
        new_user = User(full_name=user.full_name, email=user.email, password=hashed_password, chats=[])

        return new_user

    def authenticate_user(self, email: str, password: str):
        statement = select(User).where(User.email == email)
        existing_user = self.session.exec(statement).first()

        if not existing_user:
            return False
        if not self.hash_service.verify_password(password, existing_user.password):
            return False
        return existing_user

    def get_user_by_id(self, id: int):
        statement = select(User).where(User.id == id)
        existing_user = self.session.exec(statement).first()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        return existing_user
