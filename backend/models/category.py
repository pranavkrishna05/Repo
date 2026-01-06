from datetime import datetime
from typing import Optional

class Category:
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    def __init__(self, id: int, name: str, created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None) -> None:
        self.id = id
        self.name = name
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def __repr__(self) -> str:
        return f"<Category {self.name}>"