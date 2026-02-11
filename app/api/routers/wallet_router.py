from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from app.application.dto.wallet_dto import WalletResponse, WalletFund
from app.application.services.wallet import (
    FundWalletUseCase,
    GetWalletsUseCase,
    GetWalletByOwnerUseCase
)
from app.infrastructure.repositories.wallet_repo_impl import WalletRepositoryImpl
from app.infrastructure.repositories.transaction_repo_impl import TransactionRepositoryImpl
from app.infrastructure.database.session import get_db
from app.api.deps import get_current_admin, get_current_user_data
from app.domain.exceptions import DomainException
from app.domain.enums.transaction_type import PayerType

router = APIRouter(prefix="/wallets", tags=["wallets"])

# --- Dependency Providers ---

def get_wallet_repo(db: Session = Depends(get_db)) -> WalletRepositoryImpl:
    return WalletRepositoryImpl(db)

def get_transaction_repo(db: Session = Depends(get_db)) -> TransactionRepositoryImpl:
    return TransactionRepositoryImpl(db)

def get_fund_wallet_use_case(
    w_repo: WalletRepositoryImpl = Depends(get_wallet_repo),
    t_repo: TransactionRepositoryImpl = Depends(get_transaction_repo)
) -> FundWalletUseCase:
    return FundWalletUseCase(w_repo, t_repo)

def get_get_wallets_use_case(w_repo: WalletRepositoryImpl = Depends(get_wallet_repo)) -> GetWalletsUseCase:
    return GetWalletsUseCase(w_repo)

def get_get_wallet_by_owner_use_case(w_repo: WalletRepositoryImpl = Depends(get_wallet_repo)) -> GetWalletByOwnerUseCase:
    return GetWalletByOwnerUseCase(w_repo)

# --- Routes ---

@router.get("/", response_model=List[WalletResponse])
def get_wallets(
    use_case: GetWalletsUseCase = Depends(get_get_wallets_use_case),
    current_admin=Depends(get_current_admin)
):
    """List all wallets (Admin only)"""
    return use_case.execute()

@router.get("/me", response_model=WalletResponse)
def get_my_wallet(
    use_case: GetWalletByOwnerUseCase = Depends(get_get_wallet_by_owner_use_case),
    current_user=Depends(get_current_user_data)
):
    """Get current user's wallet (Student or Parent)"""
    try:
        payer_id = UUID(current_user["id"])
        payer_type = PayerType.STUDENT if current_user["role"] == "student" else PayerType.PARENT
        return use_case.execute(payer_id, payer_type)
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID in token")

@router.post("/fund", status_code=status.HTTP_200_OK)
def fund_wallet(
    fund_in: WalletFund, 
    use_case: FundWalletUseCase = Depends(get_fund_wallet_use_case),
    current_user=Depends(get_current_user_data)
):
    """Fund a wallet. (In a real app, this would be restricted or integrated with a payment gateway verify callback)"""
    # For now, we allow admins to fund any wallet, or users to fund their own.
    if current_user["role"] != "admin" and str(current_user["id"]) != str(fund_in.payer_id):
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only fund your own wallet"
        )
        
    try:
        success = use_case.execute(fund_in.payer_id, fund_in.payer_type, fund_in.amount)
        return {"status": "success", "message": "Wallet funded successfully"}
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
