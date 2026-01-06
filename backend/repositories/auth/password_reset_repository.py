from typing import Optional

class PasswordResetRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def create_password_reset(self, user_id: int, token: str, expires_at: str) -> int:
        query = """
        INSERT INTO password_resets (user_id, token, created_at, expires_at) 
        VALUES (:user_id, :token, datetime('now'), :expires_at)
        """
        result = self.db_session.execute(query, {"user_id": user_id, "token": token, "expires_at": expires_at})
        self.db_session.commit()
        return result.lastrowid

    def get_password_reset_by_token(self, token: str) -> Optional[dict]:
        query = "SELECT * FROM password_resets WHERE token = :token"
        result = self.db_session.execute(query, {"token": token}).fetchone()
        return dict(result) if result else None

    def delete_password_reset(self, password_reset_id: int) -> None:
        query = "DELETE FROM password_resets WHERE id = :password_reset_id"
        self.db_session.execute(query, {"password_reset_id": password_reset_id})
        self.db_session.commit()