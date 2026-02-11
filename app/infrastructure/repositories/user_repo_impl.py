from typing import Optional
from sqlalchemy.orm import Session
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.models.user_model import UserModel

class UserRepositoryImpl(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: str) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_entity(model) if model else None

    def get_by_email(self, email: str) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_entity(model) if model else None

    def save(self, user: User) -> User:
        # Implementation logic here (simplified for placeholder)
        pass

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            hashed_password=model.hashed_password,
            is_active=model.is_active,
            created_at=model.created_at
        )
