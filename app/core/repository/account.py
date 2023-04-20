from typing import Optional, Protocol

from app.core.models import Account


class IAccountRepository(Protocol):
    def create_account(self, account: Account) -> bool:
        pass

    def get_account(self, username: str) -> Optional[Account]:
        pass

    def has_account(self, username: str, password: str) -> bool:
        pass
