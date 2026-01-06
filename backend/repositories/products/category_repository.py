from typing import Optional

class CategoryRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_category_by_id(self, category_id: int) -> Optional[dict]:
        query = "SELECT * FROM categories WHERE id = :category_id"
        result = self.db_session.execute(query, {"category_id": category_id}).fetchone()
        return dict(result) if result else None

    def create_category(self, name: str) -> int:
        query = """
        INSERT INTO categories (name, created_at, updated_at) 
        VALUES (:name, datetime('now'), datetime('now'))"""
        result = self.db_session.execute(query, {"name": name})
        self.db_session.commit()
        return result.lastrowid