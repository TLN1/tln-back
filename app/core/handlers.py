from dataclasses import dataclass
from typing import Callable, Protocol

from app.core.application_context import IApplicationContext
from app.core.repository.account import IRepositoryAccount
from app.core.response import ResponseGeneric


@dataclass
class IHandle(Protocol):
    def handle(self) -> ResponseGeneric:
        pass


@dataclass
class AccountRegisterHandler(IHandle):
    next_handler: IHandle
    account_repository: IRepositoryAccount
    application_context: IApplicationContext
    token_generator: Callable[[], str]
    username: str
    password: str

    def handle(self) -> ResponseGeneric:
        token = self.token_generator()
        self.account_repository.create_account(
            username=self.username, password=self.password
        )  # TODO: return boolean
        self.application_context.log_user(
            self.account_repository.get_account(self.username), token
        )
        # TODO: return token
        return ResponseGeneric()


class NoHandler(IHandle):
    def handle(self) -> ResponseGeneric:
        return ResponseGeneric()
