from enum import Enum

class WalletStatus(str, Enum):
    ACTIVE = "active"
    LOCKED = "locked"
    INACTIVE = "inactive"