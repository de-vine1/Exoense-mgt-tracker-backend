from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.entities.parent import Parent
from app.domain.repositories.parent_repository import ParentRepository


class ParentRepositoryImpl(ParentRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, parent_id: UUID) -> Optional[Parent]:
        return self.db.query(Parent).filter(Parent.id == parent_id).first()

    def get_by_email(self, email: str) -> Optional[Parent]:
        return self.db.query(Parent).filter(Parent.email == email).first()

    def save(self, parent: Parent) -> Parent:
        self.db.add(parent)
        self.db.commit()
        self.db.refresh(parent)
        return parent
