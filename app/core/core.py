from dataclasses import dataclass
from typing import Callable

from app.core.application_context import IApplicationContext
from app.core.handlers import AccountRegisterHandler, NoHandler
from app.core.repository.account import IRepositoryAccount
from app.core.request import RequestRegister
from app.core.response import ResponseGeneric


@dataclass
class Core:
    application_context: IApplicationContext
    account_repository: IRepositoryAccount
    token_generator: Callable[[], str]

    def register(self, request: RequestRegister) -> ResponseGeneric:
        handler = AccountRegisterHandler(
            next_handler=NoHandler(),
            account_repository=self.account_repository,
            token_generator=self.token_generator,
            application_context=self.application_context,
            username=request.username,
            password=request.password,
        )
        return handler.handle()
