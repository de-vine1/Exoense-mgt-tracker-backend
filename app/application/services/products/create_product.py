from app.domain.entities.product import Product
from app.application.dto.product_dto import ProductCreate
from app.domain.repositories.product_repository import ProductRepository

def create_product_service(repo: ProductRepository, product_data: ProductCreate) -> Product:
    """
    Service to create a new product record.
    """
    new_product = Product(
        name=product_data.name,
        code=product_data.code,
        measure_unit=product_data.measure_unit,
        image=product_data.image,
        price=product_data.price
    )
    
    return repo.save(new_product)
