from dataclasses import dataclass

from app.core.constants import Status
from app.core.requests import (
    GetUserRequest,
    LoginRequest,
    LogoutRequest,
    RegisterRequest,
    SetupUserRequest,
)
from app.core.responses import CoreResponse, TokenResponse, UserResponse
from app.core.services.account_service import AccountService
from app.core.services.user_service import UserService


@dataclass
class Core:
    account_service: AccountService
    user_service: UserService

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

        status, _ = self.user_service.create_user(username=request.username)

        if status != Status.OK:
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

    def get_user(self, request: GetUserRequest) -> CoreResponse:
        status, user = self.user_service.get_user(username=request.username)
        if status != Status.OK or user is None:
            return CoreResponse(status=status)

        return CoreResponse(status=status, response_content=UserResponse(user=user))

    def update_user(self, request: SetupUserRequest) -> CoreResponse:
        status, user = self.user_service.update_user(
            username=request.username, user=request.user
        )
        if status != Status.OK or user is None:
            return CoreResponse(status=status)

        return CoreResponse(status=status, response_content=UserResponse(user=user))
