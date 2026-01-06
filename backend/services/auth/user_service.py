from typing import Optional
from hashlib import sha256
import logging

from backend.models.user import User
from backend.models.session import Session
from backend.repositories.auth.user_repository import UserRepository
from backend.repositories.auth.session_repository import SessionRepository

class UserService:
    def __init__(self, user_repository: UserRepository, session_repository: SessionRepository):
        self.user_repository = user_repository
        self.session_repository = session_repository
        self.logger = logging.getLogger(__name__)

    def register_user(self, email: str, password: str) -> int:
        hashed_password = self._hash_password(password)
        user_id = self.user_repository.create_user(email, hashed_password)
        self.logger.info("User registered with email: %s", email)
        return user_id

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user_data = self.user_repository.get_user_by_email(email)
        if user_data and self._check_password(password, user_data['password']):
            user = User(**user_data)
            if user.is_locked:
                self.logger.warning("Account locked for email: %s", email)
                return None
            user.reset_login_attempts()
            return user
        if user_data:
            user = User(**user_data)
            user.increment_login_attempts()
            self.user_repository.update_user_login_attempts(user.id, user.login_attempts)
            if user.login_attempts >= 5:
                user.lock_account()
                self.user_repository.lock_user_account(user.id)
                self.logger.warning("Account locked for email: %s due to multiple failed login attempts", email)
        self.logger.warning("Failed login attempt for email: %s", email)
        return None

    def create_session(self, user: User) -> Session:
        import uuid
        token = str(uuid.uuid4())
        expires_at = (datetime.utcnow() + timedelta(hours=1)).isoformat()
        session_id = self.session_repository.create_session(user.id, token, expires_at)
        self.logger.info("Session created for user: %s with token: %s", user.email, token)
        return Session(id=session_id, user_id=user.id, token=token, expires_at=expires_at)

    def _hash_password(self, password: str) -> str:
        return sha256(password.encode()).hexdigest()

    def _check_password(self, password: str, hashed_password: str) -> bool:
        return sha256(password.encode()).hexdigest() == hashed_password