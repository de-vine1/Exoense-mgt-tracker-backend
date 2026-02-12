from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.infrastructure.database.session import SessionLocal
from app.core.config import settings
from app.core.security import ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login/student")

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

async def get_current_user_data(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None or role is None:
            raise credentials_exception
        return {"id": user_id, "role": role}
    except JWTError:
        raise credentials_exception

class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user_data: dict = Depends(get_current_user_data)):
        if user_data["role"] not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permissions denied. Required roles: {', '.join(self.allowed_roles)}"
            )
        return user_data

# Specific Guards (shortcuts)
get_current_student = RoleChecker(["student"])
get_current_parent = RoleChecker(["parent"])
get_current_admin = RoleChecker(["admin"])
get_current_staff = RoleChecker(["staff", "admin"]) # Staff or higher

def get_student_repo(db: Session = Depends(get_db)):
    from app.infrastructure.repositories.student_repo_impl import StudentRepositoryImpl
    return StudentRepositoryImpl(db)

def get_parent_repo(db: Session = Depends(get_db)):
    from app.infrastructure.repositories.parent_repo_impl import ParentRepositoryImpl
    return ParentRepositoryImpl(db)

def get_staff_repo(db: Session = Depends(get_db)):
    from app.infrastructure.repositories.staff_repo_impl import StaffRepositoryImpl
    return StaffRepositoryImpl(db)

def get_product_repo(db: Session = Depends(get_db)):
    from app.infrastructure.repositories.product_repo_impl import ProductRepositoryImpl
    return ProductRepositoryImpl(db)

def get_wallet_repo(db: Session = Depends(get_db)):
    from app.infrastructure.repositories.wallet_repo_impl import WalletRepositoryImpl
    return WalletRepositoryImpl(db)

def get_transaction_repo(db: Session = Depends(get_db)):
    from app.infrastructure.repositories.transaction_repo_impl import TransactionRepositoryImpl
    return TransactionRepositoryImpl(db)

def get_sale_repo(db: Session = Depends(get_db)):
    from app.infrastructure.repositories.sale_repo_impl import SaleRepositoryImpl
    return SaleRepositoryImpl(db)
