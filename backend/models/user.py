from datetime import datetime
from typing import Optional

class User:
    id: int
    email: str
    password: str
    login_attempts: int
    is_locked: bool
    created_at: datetime
    updated_at: datetime

    def __init__(self, id: int, email: str, password: str, login_attempts: int = 0, is_locked: bool = False, created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None) -> None:
        self.id = id
        self.email = email
        self.password = password
        self.login_attempts = login_attempts
        self.is_locked = is_locked
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def increment_login_attempts(self) -> None:
        self.login_attempts += 1
        self.updated_at = datetime.utcnow()

    def lock_account(self) -> None:
        self.is_locked = True
        self.updated_at = datetime.utcnow()

    def reset_login_attempts(self) -> None:
        self.login_attempts = 0
        self.updated_at = datetime.utcnow()

    def update_password(self, new_password: str) -> None:
        self.password = new_password
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f"<User {self.email}>"