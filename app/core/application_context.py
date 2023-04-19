from dataclasses import dataclass, field
from typing import Optional, Protocol

from app.core.models import Account
from app.core.repository.account import IAccountRepository


class IApplicationContext(Protocol):
    def is_user_logged_in(self, username: str) -> bool:
        pass

    def get_account(self, token: str) -> Optional[Account]:
        pass

    def login_user(self, account: Account, token: str) -> None:
        pass

    def logout_user(self, token: str) -> None:
        pass


@dataclass
class InMemoryApplicationContext(IApplicationContext):
    account_repository: IAccountRepository
    active_accounts: dict[str, Account] = field(default_factory=dict)

    def is_user_logged_in(self, username: str) -> bool:
        for account in self.active_accounts.values():
            if account.username == username:
                return True
        return False

    def get_account(self, token: str) -> Account:
        return self.active_accounts[token]

    def login_user(self, account: Account, token: str) -> None:
        self.active_accounts[token] = account

    def logout_user(self, token: str) -> None:
        del self.active_accounts[token]
