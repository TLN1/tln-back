from dataclasses import dataclass
from typing import Callable, Optional

from app.core.constants import Status
from app.core.models import Account, Company
from app.core.repository.account_repository import IAccountRepository


@dataclass
class AccountService:
    account_repository: IAccountRepository
    hash_function: Callable[[str], str]

    def register(
        self, username: str, password: str
    ) -> tuple[Status, Optional[Account]]:
        if self.account_repository.has_account(username=username):
            return Status.ACCOUNT_ALREADY_EXISTS, None

        account = self.account_repository.create_account(
            username=username, password=self.hash_function(password)
        )

        status = Status.ACCOUNT_REGISTER_ERROR if account is None else Status.OK

        return status, account

    def link_company(self, account: Account, company: Company) -> Status:
        if not self.account_repository.link_company(
            username=account.username, company=company
        ):
            return Status.ERROR_CREATING_COMPANY

        return Status.OK
