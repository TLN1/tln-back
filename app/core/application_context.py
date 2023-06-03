from typing import Optional, Protocol

from app.core.models import Account


class IApplicationContext(Protocol):
    def is_user_logged_in(self, username: str) -> bool:
        pass

    def get_account(self, token: str) -> Optional[str]:
        pass

    def login_user(self, username: str, token: str) -> None:
        pass

    def authenticate_user(self, username: str, password: str) -> Account:
        pass

    def create_access_token(self, account: Account) -> str:
        pass

    async def get_current_user(self, token: str | None) -> Account:
        pass

    def logout_user(self, token: str) -> None:
        pass
