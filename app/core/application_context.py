from typing import Optional, Protocol


class IApplicationContext(Protocol):
    def is_user_logged_in(self, username: str) -> bool:
        pass

    def get_account(self, token: str) -> Optional[str]:
        pass

    def login_user(self, username: str, token: str) -> None:
        pass

    def logout_user(self, token: str) -> None:
        pass
