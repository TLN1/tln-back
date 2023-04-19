from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Protocol

from app.core.application_context import IApplicationContext
from app.core.repository.account import IRepositoryAccount
from app.core.response import CoreResponse, RegisterResponse


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
class AccountRegisterHandler(BaseHandler):
    account_repository: IRepositoryAccount
    application_context: IApplicationContext
    token_generator: Callable[[], str]
    username: str
    password: str

    def handle(self) -> CoreResponse:
        token = self.token_generator()
        self.account_repository.create_account(
            username=self.username, password=self.password
        )  # TODO: return boolean
        account = self.account_repository.get_account(self.username)
        self.application_context.log_user(account, token)
        return CoreResponse(response_content=RegisterResponse(token=token))
        # return super().handle()
