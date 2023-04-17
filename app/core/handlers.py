from dataclasses import dataclass
from typing import Callable

from app.core.repository.account import IRepositoryAccount
from app.core.response import ResponseGeneric

@dataclass
class IHandle:
    def handle(self) -> ResponseGeneric:
        pass


@dataclass
class AccountRegisterHandler(IHandle):
    next_handler: IHandle
    account_repository: IRepositoryAccount
    token_generator: Callable[[], str]
    username: str
    password: str

    def handle(self) -> ResponseGeneric:
        self.account_repository.create_account(username=self.username,
                                               password=self.password,
                                               token=self.token_generator(),
                                               token_is_valid=True)  # TODO: return boolean
        return ResponseGeneric()


class NoHandler(IHandle):
    def handle(self) -> ResponseGeneric:
        return ResponseGeneric()
