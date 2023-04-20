from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Protocol

from app.core.application_context import IApplicationContext
from app.core.constants import Message, Status
from app.core.models import Account
from app.core.repository.account import IAccountRepository
from app.core.responses import CoreResponse, TokenResponse


class IHandle(Protocol):
    def handle(self) -> CoreResponse:
        pass

    def set_next(self, handler: IHandle) -> IHandle:
        pass


class NoHandler(IHandle):
    def handle(self) -> CoreResponse:
        return CoreResponse()

    def set_next(self, handler: IHandle) -> IHandle:
        return handler


class BaseHandler(ABC, IHandle):
    _next_handler: IHandle = NoHandler()

    def set_next(self, handler: IHandle) -> IHandle:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self) -> CoreResponse:
        return self._next_handler.handle()


@dataclass
class AccountDoesNotExistHandler(BaseHandler):
    account_repository: IAccountRepository
    username: str
    password: str

    def handle(self) -> CoreResponse:
        if self.account_repository.has_account(
            username=self.username, password=self.password
        ):
            return CoreResponse(
                status=Status.ACCOUNT_ALREADY_EXISTS,
                message=Message.ACCOUNT_ALREADY_EXISTS,
            )

        return super().handle()


@dataclass
class AccountExistsHandler(BaseHandler):
    account_repository: IAccountRepository
    username: str
    password: str

    def handle(self) -> CoreResponse:
        if not self.account_repository.has_account(
            username=self.username, password=self.password
        ):
            return CoreResponse(
                status=Status.ACCOUNT_DOES_NOT_EXIST,
                message=Message.ACCOUNT_DOES_NOT_EXIST,
            )

        return super().handle()


@dataclass
class AccountRegisterHandler(BaseHandler):
    account_repository: IAccountRepository
    username: str
    password: str

    def handle(self) -> CoreResponse:
        account = Account(username=self.username, password=self.password)

        if not self.account_repository.create_account(account=account):
            return CoreResponse(
                status=Status.ACCOUNT_REGISTER_ERROR,
                message=Message.ACCOUNT_REGISTER_ERROR,
            )

        return super().handle()


@dataclass
class LoginHandler(BaseHandler):
    application_context: IApplicationContext
    token_generator: Callable[[], str]
    username: str
    password: str

    def handle(self) -> CoreResponse:
        if self.application_context.is_user_logged_in(self.username):
            return CoreResponse(
                status=Status.USER_ALREADY_LOGGED_IN,
                message=Message.USER_ALREADY_LOGGED_IN,
            )

        token = self.token_generator()
        self.application_context.login_user(
            account=Account(username=self.username, password=self.password), token=token
        )

        return CoreResponse(response_content=TokenResponse(token=token))


@dataclass
class UserLoggedInHandler(BaseHandler):
    application_context: IApplicationContext
    token: str

    def handle(self) -> CoreResponse:
        not_logged_in_response = CoreResponse(
            status=Status.USER_NOT_LOGGED_IN,
            message=Message.USER_NOT_LOGGED_IN,
        )
        account = self.application_context.get_account(token=self.token)
        if account is None:
            return not_logged_in_response

        if not self.application_context.is_user_logged_in(username=account.username):
            return not_logged_in_response

        return super().handle()


@dataclass
class LogoutHandler(BaseHandler):
    application_context: IApplicationContext
    token: str

    def handle(self) -> CoreResponse:
        self.application_context.logout_user(token=self.token)
        return super().handle()
