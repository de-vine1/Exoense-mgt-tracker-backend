from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.entities.admin import Admin
from app.domain.repositories.admin_repository import AdminRepository


class AdminRepositoryImpl(AdminRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, admin_id: UUID) -> Optional[Admin]:
        return self.db.query(Admin).filter(Admin.id == admin_id).first()

    def get_all(self) -> List[Admin]:
        return self.db.query(Admin).all()

    def get_by_username(self, username: str) -> Optional[Admin]:
        return self.db.query(Admin).filter(Admin.username == username).first()

    def get_by_email(self, email: str) -> Optional[Admin]:
        return self.db.query(Admin).filter(Admin.email == email).first()

    def save(self, admin: Admin) -> Admin:
        self.db.add(admin)
        self.db.commit()
        self.db.refresh(admin)
        return admin

    def delete(self, admin_id: UUID) -> bool:
        admin = self.get_by_id(admin_id)
        if admin:
            self.db.delete(admin)
            self.db.commit()
            return True
        return False

