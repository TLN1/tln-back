from dataclasses import dataclass
from typing import Callable

from app.core.handlers import AccountRegisterHandler, NoHandler
from app.core.repository.account import IRepositoryAccount
from app.core.request import RequestRegister
from app.core.response import ResponseRegister, ResponseGeneric


@dataclass
class Core:
    account_repository: IRepositoryAccount

    token_generator: Callable[[], str]

    def register(self, request: RequestRegister) -> ResponseGeneric:
        handler = AccountRegisterHandler(next_handler=NoHandler(),
                                         account_repository=self.account_repository,
                                         token_generator=self.token_generator,
                                         username=request.username,
                                         password=request.password)
        return handler.handle()
