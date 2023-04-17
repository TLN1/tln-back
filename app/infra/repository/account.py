from dataclasses import dataclass, field

from app.core.models import Account
from app.core.repository.account import IRepositoryAccount


@dataclass
class InMemoryRepositoryAccount(IRepositoryAccount):
    accounts: list[Account] = field(default_factory=list)

    def create_account(self, username: str, password: str) -> None:
        self.accounts.append(Account(len(self.accounts) + 1, username, password))

    def get_account(self, username: str) -> Account:
        for account in self.accounts:
            if account.username == username:
                return account
        raise RuntimeError("Account not found")
