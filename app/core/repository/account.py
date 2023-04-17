from typing import Protocol

from app.core.models import Account


class IRepositoryAccount(Protocol):
    def create_account(self, username: str, password: str) -> None:
        pass

    def get_account(self, username: str) -> Account:
        pass
