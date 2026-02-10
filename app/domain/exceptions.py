class DomainException(Exception):
    pass

class UserNotFoundException(DomainException):
    def __init__(self, user_id: str):
        self.message = f"User with id {user_id} not found"
        super().__init__(self.message)

class WalletNotFoundException(DomainException):
    def __init__(self, user_id: str):
        self.message = f"Wallet for user {user_id} not found"
        super().__init__(self.message)
