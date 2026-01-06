from typing import Optional

class SessionRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def create_session(self, user_id: int, token: str, expires_at: str) -> int:
        query = """
        INSERT INTO sessions (user_id, token, created_at, expires_at) 
        VALUES (:user_id, :token, datetime('now'), :expires_at)
        """
        result = self.db_session.execute(query, {"user_id": user_id, "token": token, "expires_at": expires_at})
        self.db_session.commit()
        return result.lastrowid

    def get_session_by_token(self, token: str) -> Optional[dict]:
        query = "SELECT * FROM sessions WHERE token = :token"
        result = self.db_session.execute(query, {"token": token}).fetchone()
        return dict(result) if result else None

    def update_session_expiry(self, session_id: int, expires_at: str) -> None:
        query = "UPDATE sessions SET expires_at = :expires_at WHERE id = :session_id"
        self.db_session.execute(query, {"expires_at": expires_at, "session_id": session_id})
        self.db_session.commit()

    def delete_session(self, session_id: int) -> None:
        query = "DELETE FROM sessions WHERE id = :session_id"
        self.db_session.execute(query, {"session_id": session_id})
        self.db_session.commit()