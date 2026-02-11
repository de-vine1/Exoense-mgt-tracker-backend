from decimal import Decimal
from uuid import uuid4, UUID
from app.domain.entities.product import Product
from app.domain.repositories.product_repository import ProductRepository

class CreateProductUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def execute(self, name: str, amount: Decimal, category_id: UUID) -> Product:
        product = Product(
            id=uuid4(),
            name=name,
            amount=amount,
            category_id=category_id
        )
        return self.product_repo.save(product)
