from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from app.application.dto.student_dto import StudentCreate, StudentResponse
from app.api.deps import get_current_student

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/", response_model=StudentResponse)
def register_student(student_in: StudentCreate):
    # This would call RegisterStudentUseCase
    return {"id": "uuid", "reg_number": student_in.reg_number, "firstname": student_in.firstname, "lastname": student_in.lastname, "email": student_in.email, "is_active": True, "is_link_confirmed": False, "created_at": "2024-01-01"}

@router.post("/confirm-link")
def confirm_parent_link(confirm: bool, current_student: dict = Depends(get_current_student)):
    # Uses the current_student from the guard (JWT token role: student)
    return {"status": "confirmed" if confirm else "rejected"}

@router.get("/wallet")
def get_student_wallet(current_student: dict = Depends(get_current_student)):
    # Pulls balance from WalletRepository using current_student['id']
    return {"balance": 0.0, "payer_id": current_student['id'], "payer_type": "student"}
