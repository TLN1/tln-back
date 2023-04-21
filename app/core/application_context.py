from typing import Optional, Protocol

from app.core.models import Account


class IApplicationContext(Protocol):
    def is_user_logged_in(self, username: str) -> bool:
        pass

    def get_account(self, token: str) -> Optional[Account]:
        pass

    def login_user(self, account: Account, token: str) -> None:
        pass

    def logout_user(self, token: str) -> None:
        pass
