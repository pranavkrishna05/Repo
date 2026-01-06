from typing import Optional
import logging

from backend.models.product import Product
from backend.models.category import Category
from backend.repositories.products.product_repository import ProductRepository
from backend.repositories.products.category_repository import CategoryRepository

class ProductService:
    def __init__(self, product_repository: ProductRepository, category_repository: CategoryRepository):
        self.product_repository = product_repository
        self.category_repository = category_repository
        self.logger = logging.getLogger(__name__)

    def add_product(self, name: str, price: float, description: str, category_id: Optional[int]) -> int:
        existing_product = self.product_repository.get_product_by_name(name)
        if existing_product:
            self.logger.warning("Product with name %s already exists", name)
            raise ValueError(f"Product with name {name} already exists")

        product_id = self.product_repository.create_product(name, price, description, category_id)
        self.logger.info("Product created with name: %s", name)
        return product_id

    def update_product(self, product_id: int, name: Optional[str], price: Optional[float], description: Optional[str], category_id: Optional[int]) -> None:
        if price is not None and not isinstance(price, (int, float)):
            raise ValueError("Price must be a numeric value")
        self.product_repository.update_product(product_id, name, price, description, category_id)
        self.logger.info("Product updated with id: %s", product_id)

    def delete_product(self, product_id: int) -> None:
        self.product_repository.delete_product(product_id)
        self.logger.info("Product deleted with id: %s", product_id)

    def add_category(self, name: str) -> int:
        category_id = self.category_repository.create_category(name)
        self.logger.info("Category created with name: %s", name)
        return category_id