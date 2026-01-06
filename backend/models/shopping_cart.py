from datetime import datetime
from typing import List, Dict

class ShoppingCart:
    id: int
    user_id: int
    products: List[Dict[str, int]]  # List of dicts with 'product_id' and 'quantity'
    created_at: datetime
    updated_at: datetime

    def __init__(self, id: int, user_id: int, products: List[Dict[str, int]], created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None) -> None:
        self.id = id
        self.user_id = user_id
        self.products = products
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def append_product(self, product_id: int, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
        self.products.append({"product_id": product_id, "quantity": quantity})
        self.updated_at = datetime.utcnow()

    def remove_product(self, product_id: int) -> None:
        self.products = [p for p in self.products if p["product_id"] != product_id]
        self.updated_at = datetime.utcnow()

    def update_product_quantity(self, product_id: int, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
        for product in self.products:
            if product["product_id"] == product_id:
                product["quantity"] = quantity
                break
        self.updated_at = datetime.utcnow()

    def calculate_total_price(self, product_prices: Dict[int, float]) -> float:
        return sum(product_prices[product["product_id"]] * product["quantity"] for product in self.products)

    def __repr__(self) -> str:
        return f"<ShoppingCart {self.id} for User {self.user_id}>"