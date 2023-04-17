from dataclasses import dataclass, field
from typing import Protocol

from app.core.models import Account
from app.core.repository.account import IRepositoryAccount


class IApplicationContext(Protocol):
    def is_user_logged_in(self, username: str) -> bool:
        pass

    def get_account(self, token: str) -> Account:
        pass

    def log_user(self, account: Account, token: str) -> None:
        pass


@dataclass
class InMemoryApplicationContext(IApplicationContext):
    account_repository: IRepositoryAccount
    active_accounts: dict[str, Account] = field(default_factory=dict)

    def is_user_logged_in(self, username: str) -> bool:
        for account in self.active_accounts.values():
            if account.username == username:
                return True
        return False

    def get_account(self, token: str) -> Account:
        # use username as token for now
        return self.account_repository.get_account(token)

    def log_user(self, account: Account, token: str) -> None:
        self.active_accounts[token] = account
