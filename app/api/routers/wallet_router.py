from typing import List, Any, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import get_wallet_repo, get_transaction_repo, get_current_admin
from app.application.dto.wallet_dto import WalletRead
from app.application.dto.transaction_dto import WalletTransactionRead
from app.application.services.wallets.create_wallet import create_wallet_service
from app.application.services.wallets.manage_transaction import deposit_service, withdraw_service
from app.domain.repositories.wallet_repository import WalletRepository
from app.domain.repositories.transaction_repository import TransactionRepository

router = APIRouter()

@router.post("/{student_id}", response_model=WalletRead, status_code=status.HTTP_201_CREATED)
def initialize_wallet(
    student_id: UUID,
    code: str,
    repo: WalletRepository = Depends(get_wallet_repo),
    current_admin: Any = Depends(get_current_admin)
) -> Any:
    """
    Initialize a wallet for a student.
    """
    return create_wallet_service(repo, student_id, code)

@router.get("/student/{student_id}", response_model=WalletRead)
def get_student_wallet(
    student_id: UUID,
    repo: WalletRepository = Depends(get_wallet_repo)
) -> Any:
    """
    Get wallet by student ID.
    """
    wallet = repo.get_by_student_id(student_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet

@router.post("/{wallet_id}/deposit", response_model=WalletTransactionRead)
def deposit_funds(
    wallet_id: UUID,
    amount: float,
    transaction_id: str,
    external_id: Optional[str] = None,
    wallet_repo: WalletRepository = Depends(get_wallet_repo),
    transaction_repo: TransactionRepository = Depends(get_transaction_repo),
    current_admin: Any = Depends(get_current_admin)
) -> Any:
    """
    Deposit funds into a wallet.
    """
    transaction = deposit_service(wallet_repo, transaction_repo, wallet_id, amount, transaction_id, external_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return transaction

@router.get("/{wallet_id}/transactions", response_model=List[WalletTransactionRead])
def get_wallet_transactions(
    wallet_id: UUID,
    skip: int = 0,
    limit: int = 100,
    repo: TransactionRepository = Depends(get_transaction_repo)
) -> Any:
    """
    Retrieve transaction history for a wallet.
    """
    return repo.get_by_wallet_id(wallet_id, skip=skip, limit=limit)
