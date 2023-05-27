from typing import Optional, Protocol

from app.core.models import User


class IUserRepository(Protocol):
    def create_user(self, username: str) -> Optional[User]:
        pass

    def update_user(self, username: str, user: User) -> Optional[User]:
        pass

    def get_user(self, username: str) -> User:
        pass

    def has_user(self, username: str) -> bool:
        pass
