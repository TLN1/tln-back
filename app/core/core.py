from dataclasses import dataclass
from typing import Callable

from app.core.application_context import IApplicationContext
from app.core.handlers import AccountExistsHandler, AccountRegisterHandler, NoHandler
from app.core.repository.account import IAccountRepository
from app.core.request import RegisterRequest
from app.core.response import CoreResponse


@dataclass
class Core:
    application_context: IApplicationContext
    account_repository: IAccountRepository
    token_generator: Callable[[], str]

    def register(self, request: RegisterRequest) -> CoreResponse:
        handler = AccountExistsHandler(
            account_repository=self.account_repository, username=request.username
        )
        register_handler = AccountRegisterHandler(
            account_repository=self.account_repository,
            token_generator=self.token_generator,
            application_context=self.application_context,
            username=request.username,
            password=request.password,
        )

        handler.set_next(register_handler).set_next(NoHandler())
        return handler.handle()
