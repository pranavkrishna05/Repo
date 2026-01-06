from datetime import datetime
from typing import List

class ShoppingCart:
    id: int
    user_id: int
    product_ids: List[int]
    created_at: datetime
    updated_at: datetime

    def __init__(self, id: int, user_id: int, product_ids: List[int], created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None) -> None:
        self.id = id
        self.user_id = user_id
        self.product_ids = product_ids
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def append_product(self, product_id: int) -> None:
        self.product_ids.append(product_id)
        self.updated_at = datetime.utcnow()

    def remove_product(self, product_id: int) -> None:
        self.product_ids.remove(product_id)
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f"<ShoppingCart {self.id} for User {self.user_id}>"