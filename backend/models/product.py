from datetime import datetime
from typing import Optional

class Product:
    id: int
    name: str
    price: float
    description: str
    created_at: datetime
    updated_at: datetime
    category_id: Optional[int]

    def __init__(self, id: int, name: str, price: float, description: str, created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None, category_id: Optional[int] = None) -> None:
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.category_id = category_id

    def update_product(self, name: Optional[str], price: Optional[float], description: Optional[str], category_id: Optional[int]) -> None:
        if name:
            self.name = name
        if price:
            self.price = price
        if description:
            self.description = description
        self.category_id = category_id
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f"<Product {self.name}>"