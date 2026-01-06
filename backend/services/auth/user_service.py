from typing import Optional
from hashlib import sha256
import logging

from backend.models.user import User
from backend.repositories.auth.user_repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.logger = logging.getLogger(__name__)

    def register_user(self, email: str, password: str) -> int:
        hashed_password = self._hash_password(password)
        user_id = self.user_repository.create_user(email, hashed_password)
        self.logger.info("User registered with email: %s", email)
        return user_id

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user_data = self.user_repository.get_user_by_email(email)
        if user_data and self._check_password(password, user_data['password']):
            return User(**user_data)
        self.logger.warning("Failed login attempt for email: %s", email)
        return None

    def _hash_password(self, password: str) -> str:
        return sha256(password.encode()).hexdigest()

    def _check_password(self, password: str, hashed_password: str) -> bool:
        return sha256(password.encode()).hexdigest() == hashed_password