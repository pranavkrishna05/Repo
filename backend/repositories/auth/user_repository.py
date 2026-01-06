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
        query = "INSERT INTO users (email, password, login_attempts, is_locked, created_at, updated_at, first_name, last_name, preferences) VALUES (:email, :password, 0, 0, datetime('now'), datetime('now'), NULL, NULL, NULL)"
        result = self.db_session.execute(query, {"email": email, "password": password})
        self.db_session.commit()
        return result.lastrowid

    def update_user_password(self, user_id: int, new_password: str) -> None:
        query = "UPDATE users SET password = :new_password, updated_at = datetime('now') WHERE id = :user_id"
        self.db_session.execute(query, {"new_password": new_password, "user_id": user_id})
        self.db_session.commit()

    def update_user_profile(self, user_id: int, first_name: Optional[str], last_name: Optional[str], preferences: Optional[str]) -> None:
        query = """
        UPDATE users 
        SET first_name = :first_name, last_name = :last_name, preferences = :preferences, updated_at = datetime('now') 
        WHERE id = :user_id
        """
        self.db_session.execute(query, {"first_name": first_name, "last_name": last_name, "preferences": preferences, "user_id": user_id})
        self.db_session.commit()

    def update_user_login_attempts(self, user_id: int, login_attempts: int) -> None:
        query = "UPDATE users SET login_attempts = :login_attempts, updated_at = datetime('now') WHERE id = :user_id"
        self.db_session.execute(query, {"login_attempts": login_attempts, "user_id": user_id})
        self.db_session.commit()

    def lock_user_account(self, user_id: int) -> None:
        query = "UPDATE users SET is_locked = 1, updated_at = datetime('now') WHERE id = :user_id"
        self.db_session.execute(query, {"user_id": user_id})
        self.db_session.commit()