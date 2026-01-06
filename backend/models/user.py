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
    first_name: Optional[str]
    last_name: Optional[str]
    preferences: Optional[str]

    def __init__(self, id: int, email: str, password: str, login_attempts: int = 0, is_locked: bool = False, created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None, first_name: Optional[str] = None, last_name: Optional[str] = None, preferences: Optional[str] = None) -> None:
        self.id = id
        self.email = email
        self.password = password
        self.login_attempts = login_attempts
        self.is_locked = is_locked
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.first_name = first_name
        self.last_name = last_name
        self.preferences = preferences

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

    def update_profile(self, first_name: Optional[str], last_name: Optional[str], preferences: Optional[str]) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.preferences = preferences
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f"<User {self.email}>"