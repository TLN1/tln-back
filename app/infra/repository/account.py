from dataclasses import dataclass, field

from app.core.models import Account
from app.core.repository.account import IRepositoryAccount


@dataclass
class InMemoryRepositoryAccount(IRepositoryAccount):
    accounts: list[Account] = field(default_factory=list)

    def create_account(
        self, username: str, password: str, token: str, token_is_valid: bool
    ) -> None:
        self.accounts.append(Account(username, password, token, token_is_valid))
