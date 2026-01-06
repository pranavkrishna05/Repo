from typing import Optional, List

class ShoppingCartRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_cart_by_user_id(self, user_id: int) -> Optional[dict]:
        query = "SELECT * FROM shopping_carts WHERE user_id = :user_id"
        result = self.db_session.execute(query, {"user_id": user_id}).fetchone()
        return dict(result) if result else None

    def create_cart(self, user_id: int, product_ids: List[int]) -> int:
        query = """
        INSERT INTO shopping_carts (user_id, product_ids, created_at, updated_at) 
        VALUES (:user_id, :product_ids, datetime('now'), datetime('now'))"""
        result = self.db_session.execute(query, {"user_id": user_id, "product_ids": ','.join(map(str, product_ids))})
        self.db_session.commit()
        return result.lastrowid

    def add_product_to_cart(self, cart_id: int, product_id: int) -> None:
        query = """
        UPDATE shopping_carts 
        SET product_ids = product_ids || :product_id, updated_at = datetime('now') 
        WHERE id = :cart_id"""
        self.db_session.execute(query, {"product_id": f",{product_id}", "cart_id": cart_id})
        self.db_session.commit()

    def remove_product_from_cart(self, cart_id: int, product_id: int) -> None:
        cart = self.get_cart_by_cart_id(cart_id)
        if cart:
            product_ids = cart.get('product_ids', '').split(',')
            if str(product_id) in product_ids:
                product_ids.remove(str(product_id))
                updated_product_ids = ','.join(product_ids)
                query = """
                UPDATE shopping_carts 
                SET product_ids = :product_ids, updated_at = datetime('now') 
                WHERE id = :cart_id"""
                self.db_session.execute(query, {"product_ids": updated_product_ids, "cart_id": cart_id})
                self.db_session.commit()

    def get_cart_by_cart_id(self, cart_id: int) -> Optional[dict]:
        query = "SELECT * FROM shopping_carts WHERE id = :cart_id"
        result = self.db_session.execute(query, {"cart_id": cart_id}).fetchone()
        return dict(result) if result else None