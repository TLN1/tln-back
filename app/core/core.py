from dataclasses import dataclass

from app.core.constants import Status
from app.core.requests import LoginRequest, LogoutRequest, RegisterRequest
from app.core.responses import CoreResponse, ResponseContent, TokenResponse
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

        return self.login(
            request=LoginRequest(username=account.username, password=account.password)
        )

    def login(self, request: LoginRequest) -> CoreResponse:
        status, token = self.account_service.login(
            username=request.username, password=request.password
        )

        token_response = (
            ResponseContent() if token is None else TokenResponse(token=token)
        )
        return CoreResponse(status=status, response_content=token_response)

    def logout(self, request: LogoutRequest) -> CoreResponse:
        status = self.account_service.logout(token=request.token)
        return CoreResponse(status=status)
