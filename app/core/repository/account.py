from typing import Protocol


class IRepositoryAccount(Protocol):
    def create_account(
        self, username: str, password: str, token: str, token_is_valid: bool
    ) -> None:
        pass
