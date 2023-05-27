from dataclasses import dataclass
from typing import Callable, Optional

from app.core.application_context import IApplicationContext
from app.core.constants import Status
from app.core.models import Account, Company
from app.core.repository.account_repository import IAccountRepository


@dataclass
class AccountService:
    account_repository: IAccountRepository
    application_context: IApplicationContext
    token_generator: Callable[[], str]

    def get_account(self, token: str) -> tuple[Status, Optional[Account]]:
        username = self.application_context.get_account(token=token)

        if username is None or not self.application_context.is_user_logged_in(
            username=username
        ):
            return Status.USER_NOT_LOGGED_IN, None

        account = self.account_repository.get_account(username=username)
        if account is None:
            return Status.ACCOUNT_DOES_NOT_EXIST, None

        return Status.OK, account

    def register(
        self, username: str, password: str
    ) -> tuple[Status, Optional[Account]]:
        if self.account_repository.has_account(username=username):
            return Status.ACCOUNT_ALREADY_EXISTS, None

        account = self.account_repository.create_account(
            username=username, password=password
        )
        status = Status.ACCOUNT_REGISTER_ERROR if account is None else Status.OK

        return status, account

    def login(self, username: str, password: str) -> tuple[Status, Optional[str]]:
        if not self.account_repository.is_valid(username=username, password=password):
            return Status.ACCOUNT_DOES_NOT_EXIST, None

        if self.application_context.is_user_logged_in(username=username):
            return Status.USER_ALREADY_LOGGED_IN, None

        token = self.token_generator()
        self.application_context.login_user(username=username, token=token)

        return Status.OK, token

    def logout(self, token: str) -> Status:
        username = self.application_context.get_account(token=token)
        if username is None or not self.application_context.is_user_logged_in(
            username=username
        ):
            return Status.USER_NOT_LOGGED_IN

        self.application_context.logout_user(token=token)
        return Status.OK

    def link_company(self, token: str, company: Company) -> Status:
        username = self.application_context.get_account(token=token)

        if username is None or not self.application_context.is_user_logged_in(
            username=username
        ):
            return Status.USER_NOT_LOGGED_IN

        if not self.account_repository.link_company(username=username, company=company):
            return Status.ERROR_CREATING_COMPANY

        return Status.OK
