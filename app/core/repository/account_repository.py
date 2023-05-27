from typing import Optional, Protocol

from app.core.models import Account, Company


class IAccountRepository(Protocol):
    def create_account(self, username: str, password: str) -> Optional[Account]:
        pass

    def get_account(self, username: str) -> Optional[Account]:
        pass

    def has_account(self, username: str) -> bool:
        pass

    def is_valid(self, username: str, password: str) -> bool:
        pass

    def link_company(self, username: str, company: Company) -> bool:
        pass
