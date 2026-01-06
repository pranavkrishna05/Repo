from typing import Optional, List
import logging

from backend.models.shopping_cart import ShoppingCart
from backend.repositories.carts.shopping_cart_repository import ShoppingCartRepository

class ShoppingCartService:
    def __init__(self, shopping_cart_repository: ShoppingCartRepository):
        self.shopping_cart_repository = shopping_cart_repository
        self.logger = logging.getLogger(__name__)

    def get_or_create_cart(self, user_id: int) -> ShoppingCart:
        cart = self.shopping_cart_repository.get_cart_by_user_id(user_id)
        if cart is None:
            cart_id = self.shopping_cart_repository.create_cart(user_id, [])
            cart = self.shopping_cart_repository.get_cart_by_cart_id(cart_id)
        return ShoppingCart(**cart)

    def add_product_to_cart(self, user_id: int, product_id: int, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
        cart = self.get_or_create_cart(user_id)
        self.shopping_cart_repository.add_product_to_cart(cart.id, product_id, quantity)
        self.logger.info("Added product %s with quantity %s to cart %s", product_id, quantity, cart.id)

    def remove_product_from_cart(self, user_id: int, product_id: int) -> None:
        cart = self.shopping_cart_repository.get_cart_by_user_id(user_id)
        if cart:
            self.shopping_cart_repository.remove_product_from_cart(cart['id'], product_id)
            self.logger.info("Removed product %s from cart %s", product_id, cart['id'])

    def update_product_quantity(self, user_id: int, product_id: int, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
        cart = self.shopping_cart_repository.get_cart_by_user_id(user_id)
        if cart:
            self.shopping_cart_repository.update_product_quantity(cart['id'], product_id, quantity)
            self.logger.info("Updated product %s quantity to %s in cart %s", product_id, quantity, cart['id'])

    def save_cart(self, user_id: int) -> None:
        cart = self.get_or_create_cart(user_id)
        self.logger.info("Saved cart %s for user %s", cart.id, user_id)

    def retrieve_cart(self, user_id: int) -> ShoppingCart:
        cart = self.shopping_cart_repository.get_cart_by_user_id(user_id)
        if cart:
            self.logger.info("Retrieved cart %s for user %s", cart['id'], user_id)
            return ShoppingCart(**cart)
        else:
            raise ValueError("No cart found for the user")