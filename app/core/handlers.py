from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import Callable, Optional, Protocol

from app.core.application_context import IApplicationContext
from app.core.repository.account import IRepositoryAccount
from app.core.response import CoreResponse


class IHandle(Protocol):
    def handle(self) -> CoreResponse:
        pass

    def set_next(self, handler: IHandle) -> IHandle:
        pass


class BaseHandler(ABC, IHandle):
    _next_handler: Optional[IHandle] = None

    def set_next(self, handler: IHandle) -> IHandle:
        self._next_handler = handler
        return handler

    def handle(self) -> CoreResponse:
        if self._next_handler:
            return self._next_handler.handle()
        return CoreResponse()


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
        self.application_context.log_user(
            self.account_repository.get_account(self.username), token
        )
        # TODO: return token
        return CoreResponse()


class NoHandler(BaseHandler):
    def handle(self) -> CoreResponse:
        return CoreResponse()
