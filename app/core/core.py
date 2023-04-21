from dataclasses import dataclass
from typing import Callable

from app.core.application_context import IApplicationContext
from app.core.handlers import (
    AccountDoesNotExistHandler,
    AccountExistsHandler,
    AccountRegisterHandler,
    LoginHandler,
    LogoutHandler,
    NoHandler,
    UserLoggedInHandler,
)
from app.core.repository.account import IAccountRepository
from app.core.requests import LoginRequest, LogoutRequest, RegisterRequest
from app.core.responses import CoreResponse


@dataclass
class Core:
    application_context: IApplicationContext
    account_repository: IAccountRepository
    token_generator: Callable[[], str]

    def register(self, request: RegisterRequest) -> CoreResponse:
        handler = AccountDoesNotExistHandler(
            account_repository=self.account_repository,
            username=request.username,
            password=request.password,
        )
        register_handler = AccountRegisterHandler(
            account_repository=self.account_repository,
            username=request.username,
            password=request.password,
        )
        login_handler = LoginHandler(
            application_context=self.application_context,
            token_generator=self.token_generator,
            username=request.username,
            password=request.password,
        )

        handler.set_next(register_handler).set_next(login_handler).set_next(NoHandler())
        return handler.handle()

    def login(self, request: LoginRequest) -> CoreResponse:
        handler = AccountExistsHandler(
            account_repository=self.account_repository,
            username=request.username,
            password=request.password,
        )
        login_handler = LoginHandler(
            application_context=self.application_context,
            token_generator=self.token_generator,
            username=request.username,
            password=request.password,
        )

        handler.set_next(login_handler).set_next(NoHandler())
        return handler.handle()

    def logout(self, request: LogoutRequest) -> CoreResponse:
        handler = UserLoggedInHandler(
            application_context=self.application_context, token=request.token
        )
        logout_handler = LogoutHandler(
            application_context=self.application_context, token=request.token
        )

        handler.set_next(logout_handler).set_next(NoHandler())
        return handler.handle()
