from typing import Optional

class ProductRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_product_by_id(self, product_id: int) -> Optional[dict]:
        query = "SELECT * FROM products WHERE id = :product_id"
        result = self.db_session.execute(query, {"product_id": product_id}).fetchone()
        return dict(result) if result else None

    def get_product_by_name(self, name: str) -> Optional[dict]:
        query = "SELECT * FROM products WHERE name = :name"
        result = self.db_session.execute(query, {"name": name}).fetchone()
        return dict(result) if result else None

    def create_product(self, name: str, price: float, description: str, category_id: Optional[int]) -> int:
        query = """
        INSERT INTO products (name, price, description, category_id, created_at, updated_at) 
        VALUES (:name, :price, :description, :category_id, datetime('now'), datetime('now'))"""
        result = self.db_session.execute(query, {"name": name, "price": price, "description": description, "category_id": category_id})
        self.db_session.commit()
        return result.lastrowid

    def update_product(self, product_id: int, name: Optional[str], price: Optional[float], description: Optional[str], category_id: Optional[int]) -> None:
        query = """
        UPDATE products 
        SET name = :name, price = :price, description = :description, category_id = :category_id, updated_at = datetime('now') 
        WHERE id = :product_id"""
        self.db_session.execute(query, {"name": name, "price": price, "description": description, "category_id": category_id, "product_id": product_id})
        self.db_session.commit()