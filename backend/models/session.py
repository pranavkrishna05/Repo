from datetime import datetime, timedelta

class Session:
    id: int
    user_id: int
    token: str
    created_at: datetime
    expires_at: datetime

    def __init__(self, id: int, user_id: int, token: str, created_at: Optional[datetime] = None, expires_at: Optional[datetime] = None) -> None:
        self.id = id
        self.user_id = user_id
        self.token = token
        self.created_at = created_at or datetime.utcnow()
        self.expires_at = expires_at or self.created_at + timedelta(hours=1)

    def extend_session(self, additional_time: timedelta) -> None:
        self.expires_at += additional_time

    def is_active(self) -> bool:
        return datetime.utcnow() < self.expires_at

    def __repr__(self) -> str:
        return f"<Session {self.token} for user {self.user_id}>"