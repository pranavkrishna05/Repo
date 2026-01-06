from typing import Optional

class UserRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_user_by_id(self, user_id: int) -> Optional[dict]:
        query = "SELECT * FROM users WHERE id = :user_id"
        result = self.db_session.execute(query, {"user_id": user_id}).fetchone()
        return dict(result) if result else None

    def get_user_by_email(self, email: str) -> Optional[dict]:
        query = "SELECT * FROM users WHERE email = :email"
        result = self.db_session.execute(query, {"email": email}).fetchone()
        return dict(result) if result else None

    def create_user(self, email: str, password: str) -> int:
        query = "INSERT INTO users (email, password, created_at, updated_at) VALUES (:email, :password, datetime('now'), datetime('now'))"
        result = self.db_session.execute(query, {"email": email, "password": password})
        self.db_session.commit()
        return result.lastrowid

    def update_user_password(self, user_id: int, new_password: str) -> None:
        query = "UPDATE users SET password = :new_password, updated_at = datetime('now') WHERE id = :user_id"
        self.db_session.execute(query, {"new_password": new_password, "user_id": user_id})
        self.db_session.commit()