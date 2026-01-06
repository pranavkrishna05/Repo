from typing import Optional, List, Dict

class ShoppingCartRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_cart_by_user_id(self, user_id: int) -> Optional[dict]:
        query = "SELECT * FROM shopping_carts WHERE user_id = :user_id"
        result = self.db_session.execute(query, {"user_id": user_id}).fetchone()
        return dict(result) if result else None

    def get_cart_by_cart_id(self, cart_id: int) -> Optional[dict]:
        query = "SELECT * FROM shopping_carts WHERE id = :cart_id"
        result = self.db_session.execute(query, {"cart_id": cart_id}).fetchone()
        return dict(result) if result else None

    def create_cart(self, user_id: int, products: List[Dict[str, int]]) -> int:
        query = """
        INSERT INTO shopping_carts (user_id, products, created_at, updated_at) 
        VALUES (:user_id, :products, datetime('now'), datetime('now'))"""
        result = self.db_session.execute(query, {"user_id": user_id, "products": str(products)})
        self.db_session.commit()
        return result.lastrowid

    def add_product_to_cart(self, cart_id: int, product_id: int, quantity: int) -> None:
        cart = self.get_cart_by_cart_id(cart_id)
        if cart:
            products = eval(cart["products"])
            products.append({"product_id": product_id, "quantity": quantity})
            query = """
            UPDATE shopping_carts 
            SET products = :products, updated_at = datetime('now') 
            WHERE id = :cart_id"""
            self.db_session.execute(query, {"products": str(products), "cart_id": cart_id})
            self.db_session.commit()

    def remove_product_from_cart(self, cart_id: int, product_id: int) -> None:
        cart = self.get_cart_by_cart_id(cart_id)
        if cart:
            products = eval(cart["products"])
            products = [p for p in products if p["product_id"] != product_id]
            query = """
            UPDATE shopping_carts 
            SET products = :products, updated_at = datetime('now') 
            WHERE id = :cart_id"""
            self.db_session.execute(query, {"products": str(products), "cart_id": cart_id})
            self.db_session.commit()

    def update_product_quantity(self, cart_id: int, product_id: int, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
        cart = self.get_cart_by_cart_id(cart_id)
        if cart:
            products = eval(cart["products"])
            for product in products:
                if product["product_id"] == product_id:
                    product["quantity"] = quantity
                    break
            query = """
            UPDATE shopping_carts 
            SET products = :products, updated_at = datetime('now') 
            WHERE id = :cart_id"""
            self.db_session.execute(query, {"products": str(products), "cart_id": cart_id})
            self.db_session.commit()