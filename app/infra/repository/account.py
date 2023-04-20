from dataclasses import dataclass, field
from typing import Optional

from app.core.models import Account
from app.core.repository.account import IAccountRepository


@dataclass
class InMemoryAccountRepository(IAccountRepository):
    accounts: dict[str, Account] = field(default_factory=dict)

    def create_account(self, account: Account) -> bool:
        self.accounts[account.username] = Account(
            id=len(self.accounts) + 1,
            username=account.username,
            password=account.password,
        )

        return True

    def get_account(self, username: str) -> Optional[Account]:
        return self.accounts.get(username)

    def has_account(self, username: str, password: str) -> bool:
        return (
            username in self.accounts and self.accounts[username].password == password
        )
