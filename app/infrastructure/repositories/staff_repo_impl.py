from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.entities.staff import Staff
from app.domain.repositories.staff_repository import StaffRepository

class StaffRepositoryImpl(StaffRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, staff_id: UUID) -> Optional[Staff]:
        return self.db.query(Staff).filter(Staff.id == staff_id).first()

    def get_by_email(self, email: str) -> Optional[Staff]:
        return self.db.query(Staff).filter(Staff.email == email).first()

    def save(self, staff: Staff) -> Staff:
        self.db.add(staff)
        self.db.commit()
        self.db.refresh(staff)
        return staff

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Staff]:
        return self.db.query(Staff).offset(skip).limit(limit).all()

    def delete(self, staff_id: UUID) -> bool:
        staff = self.get_by_id(staff_id)
        if staff:
            self.db.delete(staff)
            self.db.commit()
            return True
        return False
