from dataclasses import dataclass, field
from typing import Optional

from app.core.application_context import IApplicationContext
from app.core.models import Account


@dataclass
class InMemoryApplicationContext(IApplicationContext):
    active_accounts: dict[str, Account] = field(default_factory=dict)

    def is_user_logged_in(self, username: str) -> bool:
        for account in self.active_accounts.values():
            if account.username == username:
                return True

        return False

    def get_account(self, token: str) -> Optional[Account]:
        return self.active_accounts.get(token)

    def login_user(self, account: Account, token: str) -> None:
        self.active_accounts[token] = account

    def logout_user(self, token: str) -> None:
        del self.active_accounts[token]
