from dataclasses import dataclass
from typing import Callable

from app.core.repository.account import IRepositoryAccount
from app.core.request import RequestRegister
from app.core.response import ResponseRegister


@dataclass
class Core:
    account_repository: IRepositoryAccount

    token_generator: Callable[[], str]

    def register(self, request: RequestRegister) -> ResponseRegister:
        self.account_repository.create_account(
            request.username, request.password, self.token_generator(), True
        )
        return ResponseRegister()
