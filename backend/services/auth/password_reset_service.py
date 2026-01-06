from typing import Optional
import logging
import uuid

from backend.models.password_reset import PasswordReset
from backend.repositories.auth.password_reset_repository import PasswordResetRepository
from backend.repositories.auth.user_repository import UserRepository
from backend.models.user import User

class PasswordResetService:
    def __init__(self, password_reset_repository: PasswordResetRepository, user_repository: UserRepository):
        self.password_reset_repository = password_reset_repository
        self.user_repository = user_repository
        self.logger = logging.getLogger(__name__)

    def request_password_reset(self, email: str) -> Optional[str]:
        user_data = self.user_repository.get_user_by_email(email)
        if not user_data:
            self.logger.warning("Password reset requested for non-existent email: %s", email)
            return None
        user = User(**user_data)
        token = str(uuid.uuid4())
        expires_at = (datetime.utcnow() + timedelta(hours=24)).isoformat()
        self.password_reset_repository.create_password_reset(user.id, token, expires_at)
        self.logger.info("Password reset token created for email: %s", email)
        return token

    def reset_password(self, token: str, new_password: str) -> bool:
        reset_data = self.password_reset_repository.get_password_reset_by_token(token)
        if not reset_data:
            self.logger.warning("Invalid or expired password reset token: %s", token)
            return False

        password_reset = PasswordReset(**reset_data)
        if not password_reset.is_active():
            self.password_reset_repository.delete_password_reset(password_reset.id)
            self.logger.warning("Expired password reset token: %s", token)
            return False

        user = self.user_repository.get_user_by_id(password_reset.user_id)
        if not user:
            self.logger.error("User not found for password reset token: %s", token)
            return False

        self.user_repository.update_user_password(user['id'], self._hash_password(new_password))
        self.password_reset_repository.delete_password_reset(password_reset.id)
        self.logger.info("Password successfully reset for user: %s", user['email'])
        return True

    def _hash_password(self, password: str) -> str:
        return sha256(password.encode()).hexdigest()