from uuid import uuid4
from app.domain.entities.fee_category import FeeCategory
from app.domain.repositories.fee_category_repository import FeeCategoryRepository

class CreateFeeCategoryUseCase:
    def __init__(self, category_repo: FeeCategoryRepository):
        self.category_repo = category_repo

    def execute(self, name: str, description: str = None) -> FeeCategory:
        category = FeeCategory(
            id=uuid4(),
            name=name,
            description=description
        )
        return self.category_repo.save(category)
