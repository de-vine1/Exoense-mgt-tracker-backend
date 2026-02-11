from uuid import uuid4
from app.domain.entities.category import Category
from app.domain.repositories.category_repository import CategoryRepository

class CreateCategoryUseCase:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    def execute(self, name: str, description: str = None) -> Category:
        category = Category(
            id=uuid4(),
            name=name,
            description=description
        )
        return self.category_repo.save(category)
