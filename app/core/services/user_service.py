from dataclasses import dataclass
from typing import Optional

from app.core.application_context import IApplicationContext
from app.core.constants import Status
from app.core.models import User
from app.core.repository.user_repository import IUserRepository


@dataclass
class UserService:
    user_repository: IUserRepository
    application_context: IApplicationContext

    def create_user(self, username: str) -> tuple[Status, Optional[User]]:
        if not self.application_context.is_user_logged_in(username=username):
            return Status.USER_NOT_LOGGED_IN, None

        user = self.user_repository.create_user(username=username)

        status = Status.USER_SETUP_ERROR if user is None else Status.OK

        return status, user

    def update_user(self, username: str, user: User) -> tuple[Status, Optional[User]]:
        if not self.application_context.is_user_logged_in(username=username):
            return Status.USER_NOT_LOGGED_IN, None

        updated_user = self.user_repository.update_user(username=username, user=user)

        status = Status.USER_SETUP_ERROR if user is None else Status.OK

        return status, updated_user

    def get_user(self, username: str) -> tuple[Status, Optional[User]]:
        if not self.user_repository.has_user(username=username):
            return Status.ACCOUNT_DOES_NOT_EXIST, None

        user = self.user_repository.get_user(username=username)
        return Status.OK, user
