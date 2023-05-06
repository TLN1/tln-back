from dataclasses import dataclass, field
from typing import Optional

from app.core.application_context import IApplicationContext


@dataclass
class InMemoryApplicationContext(IApplicationContext):
    active_accounts: dict[str, str] = field(default_factory=dict)

    def is_user_logged_in(self, username: str) -> bool:
        for active_username in self.active_accounts.values():
            if active_username == username:
                return True

        return False

    def get_account(self, token: str) -> Optional[str]:
        return self.active_accounts.get(token)

    def has_account(self, token: str) -> bool:
        return self.get_account(token=token) is not None

    def login_user(self, username: str, token: str) -> None:
        self.active_accounts[token] = username

    def logout_user(self, token: str) -> None:
        del self.active_accounts[token]
