from fastapi import APIRouter, Depends
from uuid import UUID
from app.application.dto.parent_dto import ParentCreate, ParentResponse
from app.api.deps import get_current_parent

router = APIRouter(prefix="/parents", tags=["parents"])

@router.post("/", response_model=ParentResponse)
def register_parent(parent_in: ParentCreate):
    # This would call RegisterParentUseCase
    return {"id": "uuid", "firstname": parent_in.firstname, "lastname": parent_in.lastname, "email": parent_in.email, "is_active": True, "created_at": "2024-01-01"}

@router.post("/invite-student")
def invite_student(student_reg_number: str, current_parent: dict = Depends(get_current_parent)):
    # This would call InviteStudentUseCase using current_parent['id']
    return {"status": "invitation_sent", "by_parent": current_parent['id']}
