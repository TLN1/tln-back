from dataclasses import dataclass

from app.core.constants import Status
from app.core.requests import LoginRequest, LogoutRequest, RegisterRequest
from app.core.responses import CoreResponse, TokenResponse
from app.core.services.account_service import AccountService


@dataclass
class Core:
    account_service: AccountService

    def register(self, request: RegisterRequest) -> CoreResponse:
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
        status, token = self.account_service.login(
            username=request.username, password=request.password
        )
        if status != Status.OK or token is None:
            return CoreResponse(status=status)

        return CoreResponse(status=status, response_content=TokenResponse(token=token))

    def logout(self, request: LogoutRequest) -> CoreResponse:
        status = self.account_service.logout(token=request.token)
        return CoreResponse(status=status)
