from passlib.context import CryptContext


class HashService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, password, hashed_password) -> bool:
        return self.pwd_context.verify(password, hashed_password)
