from dataclasses import dataclass

from app.core.constants import Status
from app.core.requests import LoginRequest, LogoutRequest, RegisterRequest
from app.core.responses import CoreResponse, TokenResponse
from app.core.services.account_service import AccountService


@dataclass
class Core:
    account_service: AccountService

    def register(self, request: RegisterRequest) -> CoreResponse:
        # handler = AccountDoesNotExistHandler(
        #     account_repository=self.account_repository,
        #     username=request.username,
        #     password=request.password,
        # )
        # register_handler = AccountRegisterHandler(
        #     account_repository=self.account_repository,
        #     username=request.username,
        #     password=request.password,
        # )
        # login_handler = LoginHandler(
        #     application_context=self.application_context,
        #     token_generator=self.token_generator,
        #     username=request.username,
        #     password=request.password,
        # )
        #
        # handler.set_next(register_handler).set_next(login_handler).set_next(NoHandler())
        # return handler.handle()
        status, account = self.account_service.register(
            username=request.username, password=request.password
        )
        if status != Status.OK or account is None:
            return CoreResponse(status=status)

        status, token = self.account_service.login(
            username=account.username, password=account.password
        )
        if status != Status.OK or token is None:
            return CoreResponse(status=status)

        return CoreResponse(status=status, response_content=TokenResponse(token=token))

    def login(self, request: LoginRequest) -> CoreResponse:
        # handler = AccountExistsHandler(
        #     account_repository=self.account_repository,
        #     username=request.username,
        #     password=request.password,
        # )
        # login_handler = LoginHandler(
        #     application_context=self.application_context,
        #     token_generator=self.token_generator,
        #     username=request.username,
        #     password=request.password,
        # )
        #
        # handler.set_next(login_handler).set_next(NoHandler())
        # return handler.handle()
        status, token = self.account_service.login(
            username=request.username, password=request.password
        )
        if status != Status.OK or token is None:
            return CoreResponse(status=status)

        return CoreResponse(status=status, response_content=TokenResponse(token=token))

    def logout(self, request: LogoutRequest) -> CoreResponse:
        # handler = UserLoggedInHandler(
        #     application_context=self.application_context, token=request.token
        # )
        # logout_handler = LogoutHandler(
        #     application_context=self.application_context, token=request.token
        # )
        #
        # handler.set_next(logout_handler).set_next(NoHandler())
        # return handler.handle()
        status = self.account_service.logout(token=request.token)
        return CoreResponse(status=status)
