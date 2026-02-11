from enum import Enum

class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"

class TransactionStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"

class PaymentMethod(str, Enum):
    CARD = "card"
    BANK_TRANSFER = "bank_transfer"
    WALLET = "wallet"

class Gateway(str, Enum):
    FLUTTERWAVE = "flutterwave"
    PAYSTACK = "paystack"

class PayerType(str, Enum):
    STUDENT = "student"
    PARENT = "parent"