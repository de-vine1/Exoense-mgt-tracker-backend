from uuid import UUID
from datetime import datetime
from typing import Optional
from app.domain.entities.wallet import Wallet
from app.domain.entities.transaction import WalletTransaction
from app.domain.repositories.wallet_repository import WalletRepository
from app.domain.repositories.transaction_repository import TransactionRepository
from app.domain.enums.transaction_type import TransactionStatus

def deposit_service(
    wallet_repo: WalletRepository, 
    transaction_repo: TransactionRepository,
    wallet_id: UUID, 
    amount: float, 
    transaction_id: str,
    external_transaction_id: Optional[str] = None
) -> Optional[WalletTransaction]:
    """
    Handle depositing funds into a wallet.
    Updates the wallet balance and records a transaction.
    """
    wallet = wallet_repo.get_by_id(wallet_id)
    if not wallet:
        return None
    
    # Update balance (Simple for now, should be encrypted/decrypted)
    current_balance = float(wallet.balance)
    new_balance = current_balance + amount
    wallet.balance = str(new_balance)
    wallet_repo.save(wallet)
    
    # Record transaction
    transaction = WalletTransaction(
        wallet_id=wallet_id,
        amount=amount,
        transaction_id=transaction_id,
        external_transaction_id=external_transaction_id,
        transaction_date=datetime.now(),
        status=TransactionStatus.SUCCESS
    )
    
    return transaction_repo.save(transaction)

def withdraw_service(
    wallet_repo: WalletRepository, 
    transaction_repo: TransactionRepository,
    wallet_id: UUID, 
    amount: float, 
    transaction_id: str
) -> Optional[WalletTransaction]:
    """
    Handle withdrawing funds from a wallet.
    Checks for sufficient balance before proceeding.
    """
    wallet = wallet_repo.get_by_id(wallet_id)
    if not wallet:
        return None
    
    current_balance = float(wallet.balance)
    if current_balance < amount:
        # Insufficient funds
        transaction = WalletTransaction(
            wallet_id=wallet_id,
            amount=amount,
            transaction_id=transaction_id,
            transaction_date=datetime.now(),
            status=TransactionStatus.FAILED
        )
        return transaction_repo.save(transaction)
    
    # Update balance
    new_balance = current_balance - amount
    wallet.balance = str(new_balance)
    wallet_repo.save(wallet)
    
    # Record transaction
    transaction = WalletTransaction(
        wallet_id=wallet_id,
        amount=-amount, # Using negative for withdrawal
        transaction_id=transaction_id,
        transaction_date=datetime.now(),
        status=TransactionStatus.SUCCESS
    )
    
    return transaction_repo.save(transaction)
